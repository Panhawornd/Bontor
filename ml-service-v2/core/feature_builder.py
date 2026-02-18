"""
Complete Feature Engineering Module
Builds structured feature vector for ML model

Features include:
1. Subject scores (normalized 0-1)
2. Encoded strengths (numeric)
3. Encoded preferences (numeric)
4. SBERT similarity scores
5. Rule-based eligibility flags

ML ONLY SEES NUMBERS
"""
import logging
import re
import numpy as np
from typing import Dict, List, Optional

from nlp.preprocess import clean_text
from nlp.sbert import SBERTEncoder
from nlp.similarity import SimilarityEngine
from rules.eligibility import apply_eligibility_rules
from data.majors import MAJOR_DATABASE

logger = logging.getLogger(__name__)

# Standard subjects
SUBJECTS = ["math", "physics", "chemistry", "biology", "english", "khmer", "history"]
MAX_SCORES = {
    "math": 125, "physics": 75, "chemistry": 75, "biology": 75,
    "english": 50, "khmer": 75, "history": 50
}

# Interaction feature subject groups
STEM_SUBJECTS = ["math", "physics", "chemistry", "biology"]
LANG_SUBJECTS = ["english", "khmer"]

# Strength/Preference encoding
STRENGTHS_MAP = {
    "logic": 0, "communication": 1, "creativity": 2, "problem-solving": 3,
    "analytical": 4, "leadership": 5, "teamwork": 6, "technical": 7
}

PREFERENCES_MAP = {
    "coding": 0, "analysis": 1, "design": 2, "networking": 3,
    "research": 4, "teaching": 5, "helping": 6, "building": 7
}


class FeatureBuilder:
    """
    Builds complete feature vector for ML model
    All features are converted to numbers
    """
    
    def __init__(self):
        self.sbert = SBERTEncoder()
        self.similarity = SimilarityEngine()
        self.majors = sorted(list(MAJOR_DATABASE.keys()))
        self._major_descriptions = None
    
    def _get_major_descriptions(self) -> Dict[str, str]:
        """Get major descriptions for similarity computation"""
        if self._major_descriptions is None:
            self._major_descriptions = {}
            for name, info in MAJOR_DATABASE.items():
                desc = info.get('description', '')
                keywords = ' '.join(info.get('keywords', []))
                self._major_descriptions[name] = f"{desc} {keywords}"
        return self._major_descriptions
    
    def normalize_grade(self, subject: str, score: float) -> float:
        """Normalize grade to 0-1 range"""
        max_score = MAX_SCORES.get(subject.lower(), 100)
        return min(1.0, max(0.0, score / max_score))
    
    def encode_strengths(self, strengths_text: str) -> np.ndarray:
        """
        Encode strengths into fixed-size numeric vector
        
        Args:
            strengths_text: Comma-separated strengths
            
        Returns:
            8-dimensional binary vector
        """
        vector = np.zeros(len(STRENGTHS_MAP))
        
        if not strengths_text:
            return vector
        
        text_lower = strengths_text.lower()
        # Tokenize into words for word-boundary matching
        words = set(re.findall(r'\b\w+\b', text_lower))
        
        for strength, idx in STRENGTHS_MAP.items():
            # Check if strength is in words set or matches with word boundary regex
            strength_pattern = re.compile(r'\b' + re.escape(strength) + r'\b')
            if strength in words or strength_pattern.search(text_lower):
                vector[idx] = 1.0
        
        return vector
    
    def encode_preferences(self, preferences_text: str) -> np.ndarray:
        """
        Encode preferences into fixed-size numeric vector
        
        Args:
            preferences_text: Comma-separated preferences
            
        Returns:
            8-dimensional binary vector
        """
        vector = np.zeros(len(PREFERENCES_MAP))
        
        if not preferences_text:
            return vector
        
        text_lower = preferences_text.lower()
        # Tokenize into words for word-boundary matching
        words = set(re.findall(r'\b\w+\b', text_lower))
        
        for pref, idx in PREFERENCES_MAP.items():
            # Check if preference is in words set or matches with word boundary regex
            pref_pattern = re.compile(r'\b' + re.escape(pref) + r'\b')
            if pref in words or pref_pattern.search(text_lower):
                vector[idx] = 1.0
        
        return vector
    
    def compute_similarity_features(
        self,
        career_goal: str,
        interests: str
    ) -> np.ndarray:
        """
        Compute SBERT similarity scores for all majors
        
        Args:
            career_goal: Student's career goal text
            interests: Student's interests text
            
        Returns:
            N-dimensional vector (one score per major)
        """
        # Combine text for richer representation
        combined_text = f"{career_goal} {interests}".strip()
        
        if not combined_text:
            return np.zeros(len(self.majors))
        
        # Compute similarity scores using NLP pipeline
        # NLTK preprocessing happens inside similarity engine
        major_descriptions = self._get_major_descriptions()
        similarity_scores = self.similarity.compute_major_similarity_scores(
            combined_text, {m: {'description': d, 'keywords': []} for m, d in major_descriptions.items()}
        )
        
        # Convert to array in consistent order
        scores = np.array([similarity_scores.get(m, 0.0) for m in self.majors])
        
        return scores
    
    def compute_eligibility_flags(
        self,
        grades: Dict[str, float]
    ) -> np.ndarray:
        """
        Get rule-based eligibility flags for all majors
        
        Args:
            grades: User grades
            
        Returns:
            N-dimensional vector (penalty factor per major, 1.0 = eligible)
        """
        _, eligibility = apply_eligibility_rules(grades, self.majors)
        
        # Convert to array in consistent order
        flags = np.array([eligibility.get(m, 1.0) for m in self.majors])
        
        return flags
    
    def build_features(
        self,
        grades: Dict[str, float],
        interests: str = "",
        career_goal: str = "",
        strengths: str = "",
        preferences: str = ""
    ) -> np.ndarray:
        """
        Build complete feature vector for ML model
        
        Features:
        1. Subject scores (7 features) - normalized 0-1
        2. Grade statistics (3 features) - mean, std, max
        3. Encoded strengths (8 features) - binary
        4. Encoded preferences (8 features) - binary
        5. SBERT similarity scores (N features) - 0-1
        6. Eligibility flags (N features) - 0-1
        
        Args:
            grades: Subject scores
            interests: Interest text
            career_goal: Career goal text
            strengths: Strengths description
            preferences: Preferences description
            
        Returns:
            Numeric feature vector
        """
        # Normalize grade keys to lowercase
        grades_lower = {k.lower(): v for k, v in grades.items()}
        
        # 1. Grade features (normalized 0-1)
        grade_features = []
        for subject in SUBJECTS:
            score = grades_lower.get(subject, 0)
            grade_features.append(self.normalize_grade(subject, score))
        
        # 2. Grade statistics (derived from normalized grade_features)
        non_zero_normalized = [g for g in grade_features if g > 0]
        if non_zero_normalized:
            grade_stats = [
                np.mean(non_zero_normalized),  # mean of normalized values
                np.std(non_zero_normalized),   # std of normalized values
                max(non_zero_normalized)       # max of normalized values
            ]
        else:
            grade_stats = [0.0, 0.0, 0.0]
        
        # 2b. Interaction features (STEM vs Language signals)
        stem_avg = float(np.mean([
            grade_features[SUBJECTS.index(s)] for s in STEM_SUBJECTS
        ]))
        lang_avg = float(np.mean([
            grade_features[SUBJECTS.index(s)] for s in LANG_SUBJECTS
        ]))
        stem_lang_ratio = stem_avg / (lang_avg + 1e-6)
        math_phys = grade_features[0] * grade_features[1]   # math×physics
        chem_bio = grade_features[2] * grade_features[3]     # chemistry×biology
        interaction_features = [
            stem_avg, lang_avg, stem_lang_ratio,
            math_phys, chem_bio,
        ]
        
        # 3. Encode strengths
        strength_features = self.encode_strengths(strengths)
        
        # 4. Encode preferences
        preference_features = self.encode_preferences(preferences)
        
        # 5. SBERT similarity scores
        similarity_features = self.compute_similarity_features(career_goal, interests)
        
        # 6. Eligibility flags
        eligibility_features = self.compute_eligibility_flags(grades_lower)
        
        # Combine all features into single vector
        features = np.concatenate([
            grade_features,         # 7 features
            grade_stats,            # 3 features
            interaction_features,   # 5 features
            strength_features,      # 8 features
            preference_features,    # 8 features
            similarity_features,    # N features (majors count)
            eligibility_features    # N features (majors count)
        ])
        
        logger.debug(f"Built feature vector: {len(features)} dimensions")
        
        return features.astype(np.float32)
    
    def get_feature_names(self) -> List[str]:
        """Get names of all features in order"""
        names = (
            [f"grade_{s}" for s in SUBJECTS] +
            ["grade_mean", "grade_std", "grade_max"] +
            ["stem_avg", "lang_avg", "stem_lang_ratio",
             "math_phys_interaction", "chem_bio_interaction"] +
            [f"strength_{s}" for s in STRENGTHS_MAP.keys()] +
            [f"pref_{p}" for p in PREFERENCES_MAP.keys()] +
            [f"sbert_sim_{m}" for m in self.majors] +
            [f"eligible_{m}" for m in self.majors]
        )
        return names
    
    def get_feature_count(self) -> int:
        """Get total number of features"""
        return len(self.get_feature_names())



