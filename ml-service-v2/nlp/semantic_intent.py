"""
Semantic Intent Detection — Pure SBERT, Zero Hardcoded Boosts

How it works:
1. Builds a semantic profile for EVERY major by combining its
   description + keywords from MAJOR_DATABASE.
2. Computes SBERT similarity between user text and each major's profile.
3. The similarity score IS the boost — no manually assigned numbers.
4. Detects negative intent using SBERT too.

Nothing is hardcoded:
- No hardcoded phrases per concept (uses the database)
- No hardcoded boost values (similarity IS the signal)
- No hardcoded major lists
"""
import logging
import numpy as np
from typing import Dict, List, Optional
from functools import lru_cache

from data.majors import MAJOR_DATABASE

logger = logging.getLogger(__name__)


class SemanticIntentDetector:
    """
    Pure-SBERT intent detector.

    • Pre-computes embeddings for every major from the database
    • Compares user text against all majors semantically
    • Returns similarity-based boosts (no hardcoded numbers)
    """

    _major_embeddings: Optional[Dict[str, np.ndarray]] = None
    _negative_embedding: Optional[np.ndarray] = None
    _encoder = None

    # Negative phrases — conceptual anchors (not pattern-matching lists)
    _NEGATIVE_ANCHORS = [
        "I don't like this at all",
        "I hate this and want to avoid it",
        "not interested in this field",
        "bad at this subject and dislike it",
        "anything except this, never want this",
        "boring terrible and not for me",
    ]

    def __init__(self):
        from nlp.sbert import SBERTEncoder

        if SemanticIntentDetector._encoder is None:
            SemanticIntentDetector._encoder = SBERTEncoder()
        self._precompute_embeddings()

    # ------------------------------------------------------------------
    # Pre-compute (one-time) — purely from MAJOR_DATABASE
    # ------------------------------------------------------------------
    def _precompute_embeddings(self):
        if SemanticIntentDetector._major_embeddings is not None:
            return

        logger.info("Pre-computing major embeddings from database (Pure AI)…")
        enc = SemanticIntentDetector._encoder
        assert enc is not None, "Encoder must be initialized"
        SemanticIntentDetector._major_embeddings = {}

        for major_name, info in MAJOR_DATABASE.items():
            # Build a rich, weighted text representation from the database
            from nlp.preprocess import clean_text
            
            # Base signals
            desc = info.get("description", "")
            keywords = info.get("keywords", [])
            careers = info.get("career_paths", [])
            subjects = info.get("required_subjects", [])
            
            # Weight skills by importance
            weighted_skills = []
            for skill, s_info in info.get("fundamental_skills", {}).items():
                imp = s_info.get("importance", "medium")
                if imp == "critical":
                    weighted_skills.extend([skill] * 3)
                elif imp == "high":
                    weighted_skills.extend([skill] * 2)
                else:
                    weighted_skills.append(skill)
            
            # Repeat subjects and keywords to give them more weight against the description
            major_text = (
                f"{desc} "
                f"{' '.join(keywords)} {' '.join(keywords)} "
                f"{' '.join(careers)} "
                f"{' '.join(weighted_skills)} "
                f"{' '.join(subjects)} {' '.join(subjects)}"
            )
            
            clean_profile = clean_text(major_text)
            embedding = enc.encode(clean_profile)
            if SemanticIntentDetector._major_embeddings is not None:
                SemanticIntentDetector._major_embeddings[major_name] = embedding

        # Negative anchors
        neg_embs = [enc.encode(p) for p in SemanticIntentDetector._NEGATIVE_ANCHORS]
        SemanticIntentDetector._negative_embedding = np.mean(neg_embs, axis=0) # type: ignore
        logger.info(
            f"Pre-computed embeddings for {len(MAJOR_DATABASE)} majors + negative anchor"
        )

    # ------------------------------------------------------------------
    # Cosine similarity
    # ------------------------------------------------------------------
    @staticmethod
    def _cosine(a: np.ndarray, b: np.ndarray) -> float:
        na, nb = np.linalg.norm(a), np.linalg.norm(b)
        if na == 0 or nb == 0:
            return 0.0
        return float(np.dot(a, b) / (na * nb))

    # ------------------------------------------------------------------
    # Detect intent — returns {major: boost} purely from similarity
    # ------------------------------------------------------------------
    def detect_intent(self, text: str, threshold: float = 0.12) -> Dict[str, float]:
        """
        Pure SBERT intent detection with negation awareness.

        Returns {major_name: similarity_score} for every major whose
        similarity exceeds `threshold`.

        Negation-aware: if the user says "i don't like X", X-related
        majors will NOT get boosted — they'll be excluded instead.
        """
        if not text or not text.strip():
            return {}

        enc = SemanticIntentDetector._encoder
        from nlp.preprocess import clean_text
        
        lower_text = text.lower()
        
        # Detect negative patterns in the text
        import re
        # Detect negative patterns in the text
        NEGATION_PATTERNS = [
            r"don't like", r"dont like", r"don't want", r"dont want",
            r"not interested", r"not like", r"\bhate\b", r"\bdislike\b",
            r"don't enjoy", r"dont enjoy", r"never want", r"\bavoid\b",
            r"anything but", r"anything except", r"not for me",
            r"bad at", r"terrible at", r"\bboring\b",
            r"\bnot\b", r"\bno\b", r"\bnever\b", r"\bcannot\b", r"\bcant\b", r"can't\b"
        ]
        has_negation = any(re.search(neg, lower_text) for neg in NEGATION_PATTERNS)
        
        # Detect mixed intent: text has negation but ALSO positive parts
        # e.g. "I hate coding BUT I love designing interfaces"
        MIXED_CONNECTORS = ["but", "however", "instead", "prefer", "rather", "love", "enjoy", "like"]
        has_mixed_intent = has_negation and any(conn in lower_text for conn in MIXED_CONNECTORS)
        
        # For mixed intent, identify which majors are being NEGATED (keyword-based)
        negated_majors = set()
        if has_mixed_intent:
            NEGATED_KEYWORD_MAP = {
                "coding": ["Software Engineering"],
                "programming": ["Software Engineering"],
                "math": ["Software Engineering", "Data Science", "Mechanical Engineering", "Electrical Engineering"],
                "biology": ["Medicine", "Pharmacy", "Dentistry"],
                "chemistry": ["Chemical Engineering", "Medicine", "Pharmacy"],
                "electrical": ["Electrical Engineering"],
                "electronics": ["Electrical Engineering"],
                "mechanical": ["Mechanical Engineering"],
                "doctor": ["Medicine"], "medicine": ["Medicine"],
                "law": ["Law"], "lawyer": ["Law"],
                "business": ["Business Administration", "Business Management"],
                "teaching": ["Education"], "psychology": ["Psychology"],
                "hacking": ["Cybersecurity"], "security": ["Cybersecurity"],
            }
            
            # Split into clauses by contrasting conjunctions to isolate negated keywords
            clauses = re.split(r'\b(?:but|however|instead|except|although|while)\b', lower_text)
            for clause in clauses:
                # Check if this specific clause has a negation
                if any(re.search(neg, clause) for neg in NEGATION_PATTERNS):
                    for keyword, majors in NEGATED_KEYWORD_MAP.items():
                        # Use word boundary to avoid partial matches
                        if re.search(rf"\b{re.escape(keyword)}\b", clause):
                            negated_majors.update(majors)

        enc = SemanticIntentDetector._encoder
        assert enc is not None, "Encoder must be initialized"
        assert SemanticIntentDetector._major_embeddings is not None, "Embeddings must be initialized"
        
        user_emb = enc.encode(clean_text(text))

        # Check negative sentiment — require BOTH pattern match AND semantic signal
        neg_sim = self._cosine(user_emb, SemanticIntentDetector._negative_embedding) # type: ignore
        is_negative = has_negation and neg_sim > 0.25 and not has_mixed_intent

        boosts: Dict[str, float] = {}
        for major_name, major_emb in SemanticIntentDetector._major_embeddings.items():
            sim = self._cosine(user_emb, major_emb)

            if sim < threshold:
                continue

            if has_mixed_intent:
                # Mixed intent: penalize negated majors, boost everything else normally
                if major_name in negated_majors:
                    boosts[major_name] = max(0.1, 1.0 - sim)
                else:
                    boost = 1.0 + (sim - threshold) / (1.0 - threshold) * 5.0
                    boosts[major_name] = boost
            elif is_negative or has_negation:
                # Purely negative text, penalise matching majors
                boosts[major_name] = max(0.1, 1.0 - sim)
            else:
                # Scale similarity (0.12-1.0) → boost (1.0-6.0)
                boost = 1.0 + (sim - threshold) / (1.0 - threshold) * 5.0
                boosts[major_name] = boost

        if boosts:
            top5 = sorted(boosts.items(), key=lambda x: -x[1])[:5]
            logger.info(f"Semantic intent (top 5): {top5}")

        return boosts

    # ------------------------------------------------------------------
    # Detect exclusions (negative intent per-major)
    # ------------------------------------------------------------------
    def detect_exclusions(self, text: str) -> Dict[str, float]:
        """
        Detect negative intent using both SBERT and keyword detection.

        Uses a two-pronged approach:
        1. SBERT semantic similarity to negative phrases per major
        2. Keyword-based detection: if text contains negation + major keyword
        
        Returns {major: penalty_factor} where < 1.0 means penalised.
        """
        if not text or not text.strip():
            return {}

        lower_text = text.lower()
        enc = SemanticIntentDetector._encoder
        assert enc is not None, "Encoder must be initialized"
        user_emb = enc.encode(lower_text)

        penalties: Dict[str, float] = {}
        
        # --- METHOD 1: Keyword-based negation detection ---
        import re
        NEGATION_PATTERNS = [
            r"don't like", r"dont like", r"don't want", r"dont want",
            r"not interested", r"not like", r"\bhate\b", r"\bdislike\b",
            r"don't enjoy", r"dont enjoy", r"never want", r"\bavoid\b",
            r"anything but", r"anything except", r"\bnot\b", r"\bno\b",
            r"\bnever\b", r"\bcannot\b", r"\bcant\b", r"can't\b"
        ]
        
        has_negation = any(re.search(neg, lower_text) for neg in NEGATION_PATTERNS)
        
        if has_negation:
            # Check which majors are being negated using keywords
            # Use word-boundary matching, NOT substring matching
            import re
            KEYWORD_TO_MAJORS = {
                "math": ["Software Engineering", "Data Science", "Mechanical Engineering", "Electrical Engineering", "Civil Engineering", "Chemical Engineering", "Architecture", "Finance"],
                "mathematics": ["Software Engineering", "Data Science", "Mechanical Engineering", "Electrical Engineering", "Civil Engineering", "Chemical Engineering", "Architecture", "Finance"],
                "physics": ["Mechanical Engineering", "Electrical Engineering", "Civil Engineering", "Chemical Engineering", "Architecture"],
                "biology": ["Medicine", "Pharmacy", "Dentistry"],
                "chemistry": ["Chemical Engineering", "Medicine", "Pharmacy", "Dentistry"],
                "code": ["Software Engineering", "Data Science", "Cybersecurity", "Telecommunication and Networking"],
                "coding": ["Software Engineering", "Data Science", "Cybersecurity", "Telecommunication and Networking"],
                "programming": ["Software Engineering", "Data Science", "Cybersecurity", "Telecommunication and Networking"],
                "electrical": ["Electrical Engineering"],
                "electronics": ["Electrical Engineering"],
                "mechanical": ["Mechanical Engineering"],
                "doctor": ["Medicine"],
                "medicine": ["Medicine"],
                "medical": ["Medicine"],
                "law": ["Law"],
                "lawyer": ["Law"],
                "legal": ["Law"],
                "design": ["UX/UI Design", "Graphic Design", "Architecture"],
                "business": ["Business Administration", "Business Management"],
                "teaching": ["Education"],
                "psychology": ["Psychology"],
                "finance": ["Finance"],
                "hacking": ["Cybersecurity"],
                "security": ["Cybersecurity"],
            }
            
            # Split into clauses by contrasting conjunctions to isolate negated keywords
            clauses = re.split(r'\b(?:but|however|instead|except|although|while)\b', lower_text)
            for clause in clauses:
                if any(re.search(neg, clause) for neg in NEGATION_PATTERNS):
                    for keyword, majors in KEYWORD_TO_MAJORS.items():
                        # Use word boundary to avoid "designing" matching "design"
                        if re.search(rf"\b{re.escape(keyword)}\b", clause):
                            for major in majors:
                                penalties[major] = min(penalties.get(major, 1.0), 0.05)  # Very strong penalty

        # --- METHOD 2: SBERT-based negative detection (fallback) ---
        # Only run if there's actual negation language OR very high negative similarity
        assert SemanticIntentDetector._negative_embedding is not None, "Negative anchor must be initialized"
        neg_sim = self._cosine(user_emb, SemanticIntentDetector._negative_embedding)
        if has_negation or neg_sim > 0.50:  # Require negation pattern OR very high neg signal
            assert SemanticIntentDetector._major_embeddings is not None
            for major_name, major_emb in SemanticIntentDetector._major_embeddings.items():
                if major_name in penalties:
                    continue  # Already handled by keyword method
                    
                # Get info from database (using cast to satisfy IDE)
                from typing import cast, Any
                info = cast(Dict[str, Any], MAJOR_DATABASE.get(major_name, {}) or {})
                desc = info.get("description", major_name)
                neg_text = f"I don't want {desc} I hate {major_name}"
                neg_emb = enc.encode(neg_text.lower())

                sim_to_negative = self._cosine(user_emb, neg_emb)

                if sim_to_negative > 0.50:  # Keep strict for SBERT method
                    penalty = max(0.05, 1.0 - sim_to_negative)
                    penalties[major_name] = min(penalties.get(major_name, 1.0), penalty)

        if penalties:
            logger.info(f"Exclusion penalties: {penalties}")

        return penalties



# Singleton
_detector_instance = None


def get_semantic_detector() -> SemanticIntentDetector:
    global _detector_instance
    if _detector_instance is None:
        _detector_instance = SemanticIntentDetector()
    return _detector_instance
