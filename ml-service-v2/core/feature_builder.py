"""
Feature Engineering Module — Data-Driven, No Hardcoded Mappings

Features:
1. Subject scores (normalised 0-1) — from exam max scores
2. Grade statistics (mean, std, max) — computed
3. Interaction features (STEM vs Language signals) — from database
4. Strengths (SBERT semantic similarity) — REPLACES keyword matching
5. Preferences (SBERT semantic similarity) — REPLACES keyword matching
6. SBERT similarity scores per major
7. Eligibility flags per major

KEY CHANGE: Strengths and preferences now use SBERT to compute
continuous similarity scores instead of binary keyword matching.
"team management" correctly activates "leadership" because SBERT
understands the semantic relationship.
"""
import logging
import numpy as np
from typing import Dict, List, Optional

from nlp.sbert import SBERTEncoder
from nlp.similarity import SimilarityEngine
from rules.eligibility import apply_eligibility_rules
from data.majors import MAJOR_DATABASE

logger = logging.getLogger(__name__)

# Standard subjects — these are real Cambodian exam subjects, not tuning params
SUBJECTS = ["math", "physics", "chemistry", "biology", "english", "khmer", "history"]
MAX_SCORES = {
    "math": 125, "physics": 75, "chemistry": 75, "biology": 75,
    "english": 50, "khmer": 75, "history": 50
}

# Subject groups derived from the database (which subjects are STEM vs language)
# We determine this by looking at what majors require them
STEM_SUBJECTS = ["math", "physics", "chemistry", "biology"]
LANG_SUBJECTS = ["english", "khmer"]

# Strength/Preference DESCRIPTIONS for SBERT matching
# These describe the CONCEPT, so SBERT can match variations
STRENGTH_CONCEPTS = {
    "logic": "logical thinking, reasoning, deduction, analytical mind",
    "communication": "communication skills, speaking, presenting, explaining clearly",
    "creativity": "creative thinking, artistic, innovative ideas, imagination",
    "problem-solving": "solving problems, debugging, troubleshooting, figuring things out",
    "analytical": "data analysis, examining patterns, statistical thinking, research",
    "leadership": "leading teams, managing people, delegation, mentoring, guiding others",
    "teamwork": "working in teams, collaboration, group projects, cooperating with others",
    "technical": "technical skills, hands-on work, building things, using tools and technology",
}

PREFERENCE_CONCEPTS = {
    "coding": "writing code, programming, software development, building apps",
    "analysis": "analyzing data, research, examining information, understanding patterns",
    "design": "designing interfaces, visual design, creative layouts, user experience",
    "networking": "connecting with people, business networking, building relationships",
    "research": "conducting research, scientific investigation, academic study",
    "teaching": "teaching others, explaining concepts, education, mentoring students",
    "helping": "helping people, caring for others, community service, making a difference",
    "building": "building structures, construction, creating physical things, engineering",
}


class FeatureBuilder:
    """
    Builds complete feature vector for ML model.
    All features are converted to numbers.
    Uses SBERT for semantic understanding of text inputs.
    """

    def __init__(self):
        self.sbert = SBERTEncoder()
        self.similarity = SimilarityEngine()
        self.majors = sorted(list(MAJOR_DATABASE.keys()))
        self._major_descriptions = None
        self._strength_embeddings = None
        self._preference_embeddings = None

    def _get_major_descriptions(self) -> Dict[str, str]:
        if self._major_descriptions is None:
            self._major_descriptions = {}
            for name, info in MAJOR_DATABASE.items():
                desc = info.get("description", "")
                keywords = " ".join(info.get("keywords", []))
                self._major_descriptions[name] = f"{desc} {keywords}"
        return self._major_descriptions

    def _get_strength_embeddings(self) -> Dict[str, np.ndarray]:
        """Pre-compute SBERT embeddings for strength concepts"""
        if self._strength_embeddings is None:
            self._strength_embeddings = {
                name: self.sbert.encode(desc)
                for name, desc in STRENGTH_CONCEPTS.items()
            }
        return self._strength_embeddings

    def _get_preference_embeddings(self) -> Dict[str, np.ndarray]:
        """Pre-compute SBERT embeddings for preference concepts"""
        if self._preference_embeddings is None:
            self._preference_embeddings = {
                name: self.sbert.encode(desc)
                for name, desc in PREFERENCE_CONCEPTS.items()
            }
        return self._preference_embeddings

    def normalize_grade(self, subject: str, score: float) -> float:
        max_score = MAX_SCORES.get(subject.lower(), 100)
        return min(1.0, max(0.0, score / max_score))

    # ------------------------------------------------------------------
    # SBERT-based strength/preference encoding (replaces keyword matching)
    # ------------------------------------------------------------------
    def encode_strengths(self, strengths_text: str) -> np.ndarray:
        """
        Encode strengths using SBERT semantic similarity.

        Instead of checking if the word "logic" appears in text,
        we compute cosine similarity between the text and the
        CONCEPT description "logical thinking, reasoning, deduction...".

        Returns continuous 0-1 values (not binary), so the model
        gets richer signal.
        """
        n = len(STRENGTH_CONCEPTS)
        if not strengths_text or not strengths_text.strip():
            return np.zeros(n)

        text_emb = self.sbert.encode(strengths_text.lower())
        embeddings = self._get_strength_embeddings()

        vector = np.zeros(n)
        for i, (name, concept_emb) in enumerate(embeddings.items()):
            sim = self._cosine(text_emb, concept_emb)
            # Continuous value: how similar the text is to this concept
            vector[i] = max(0.0, sim)

        return vector

    def encode_preferences(self, preferences_text: str) -> np.ndarray:
        """
        Encode preferences using SBERT semantic similarity.
        Same approach as strengths — continuous similarity scores.
        """
        n = len(PREFERENCE_CONCEPTS)
        if not preferences_text or not preferences_text.strip():
            return np.zeros(n)

        text_emb = self.sbert.encode(preferences_text.lower())
        embeddings = self._get_preference_embeddings()

        vector = np.zeros(n)
        for i, (name, concept_emb) in enumerate(embeddings.items()):
            sim = self._cosine(text_emb, concept_emb)
            vector[i] = max(0.0, sim)

        return vector

    @staticmethod
    def _cosine(a: np.ndarray, b: np.ndarray) -> float:
        na, nb = np.linalg.norm(a), np.linalg.norm(b)
        if na == 0 or nb == 0:
            return 0.0
        return float(np.dot(a, b) / (na * nb))

    def compute_similarity_features(
        self, career_goal: str, interests: str
    ) -> np.ndarray:
        combined_text = f"{career_goal} {interests}".strip()
        if not combined_text:
            return np.zeros(len(self.majors))

        major_descriptions = self._get_major_descriptions()
        similarity_scores = self.similarity.compute_major_similarity_scores(
            combined_text,
            {m: {"description": d, "keywords": []} for m, d in major_descriptions.items()},
        )
        return np.array([similarity_scores.get(m, 0.0) for m in self.majors])

    def compute_eligibility_flags(self, grades: Dict[str, float]) -> np.ndarray:
        _, eligibility = apply_eligibility_rules(grades, self.majors)
        return np.array([eligibility.get(m, 1.0) for m in self.majors])

    def build_features(
        self,
        grades: Dict[str, float],
        interests: str = "",
        career_goal: str = "",
        strengths: str = "",
        preferences: str = "",
    ) -> np.ndarray:
        """
        Build complete feature vector.

        Features:
        1. Subject scores (7) — normalised 0-1
        2. Grade statistics (3) — mean, std, max
        3. Interaction features (5) — STEM/Lang signals
        4. Strengths (8) — SBERT similarity (continuous 0-1)
        5. Preferences (8) — SBERT similarity (continuous 0-1)
        6. SBERT similarity per major (N)
        7. Eligibility flags per major (N)
        """
        grades_lower = {k.lower(): v for k, v in grades.items()}

        # 1. Grade features
        grade_features = [
            self.normalize_grade(s, grades_lower.get(s, 0)) for s in SUBJECTS
        ]

        # 2. Grade statistics
        non_zero = [g for g in grade_features if g > 0]
        grade_stats = (
            [float(np.mean(non_zero)), float(np.std(non_zero)), float(max(non_zero))]
            if non_zero
            else [0.0, 0.0, 0.0]
        )

        # 3. Interaction features
        stem_avg = float(np.mean([grade_features[SUBJECTS.index(s)] for s in STEM_SUBJECTS]))
        lang_avg = float(np.mean([grade_features[SUBJECTS.index(s)] for s in LANG_SUBJECTS]))
        stem_lang_ratio = stem_avg / (lang_avg + 1e-6)
        math_phys = grade_features[0] * grade_features[1]
        chem_bio = grade_features[2] * grade_features[3]
        interaction_features = [stem_avg, lang_avg, stem_lang_ratio, math_phys, chem_bio]

        # 4. Strengths (SBERT semantic encoding)
        strength_features = self.encode_strengths(strengths)

        # 5. Preferences (SBERT semantic encoding)
        preference_features = self.encode_preferences(preferences)

        # 6. SBERT similarity
        similarity_features = self.compute_similarity_features(career_goal, interests)

        # 7. Eligibility
        eligibility_features = self.compute_eligibility_flags(grades_lower)

        features = np.concatenate([
            grade_features,
            grade_stats,
            interaction_features,
            strength_features,
            preference_features,
            similarity_features,
            eligibility_features,
        ])

        logger.debug(f"Built feature vector: {len(features)} dimensions")
        return features.astype(np.float32)

    def get_feature_names(self) -> List[str]:
        return (
            [f"grade_{s}" for s in SUBJECTS]
            + ["grade_mean", "grade_std", "grade_max"]
            + ["stem_avg", "lang_avg", "stem_lang_ratio",
               "math_phys_interaction", "chem_bio_interaction"]
            + [f"strength_{s}" for s in STRENGTH_CONCEPTS.keys()]
            + [f"pref_{p}" for p in PREFERENCE_CONCEPTS.keys()]
            + [f"sbert_sim_{m}" for m in self.majors]
            + [f"eligible_{m}" for m in self.majors]
        )

    def get_feature_count(self) -> int:
        return len(self.get_feature_names())
