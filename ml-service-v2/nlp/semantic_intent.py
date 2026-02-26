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
        SemanticIntentDetector._major_embeddings = {}

        for major_name, info in MAJOR_DATABASE.items():
            # Build a rich text representation from the database
            from nlp.preprocess import clean_text
            major_text = f"{info.get('description', '')} {' '.join(info.get('keywords', []))} {' '.join(info.get('career_paths', []))} {' '.join(info.get('fundamental_skills', {}).keys())} {' '.join(info.get('required_subjects', []))}"
            clean_profile = clean_text(major_text)
            embedding = enc.encode(clean_profile)
            SemanticIntentDetector._major_embeddings[major_name] = embedding

        # Negative anchors
        neg_embs = [enc.encode(p) for p in SemanticIntentDetector._NEGATIVE_ANCHORS]
        SemanticIntentDetector._negative_embedding = np.mean(neg_embs, axis=0)
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
    def detect_intent(self, text: str, threshold: float = 0.25) -> Dict[str, float]:
        """
        Pure SBERT intent detection.

        Returns {major_name: similarity_score} for every major whose
        similarity exceeds `threshold`.

        The score IS the boost — higher similarity means stronger match.
        We scale it to a 1-6 range to keep downstream compatibility,
        but the ranking is 100% determined by SBERT.
        """
        if not text or not text.strip():
            return {}

        enc = SemanticIntentDetector._encoder
        from nlp.preprocess import clean_text
        user_emb = enc.encode(clean_text(text))

        # Check negative sentiment
        neg_sim = self._cosine(user_emb, SemanticIntentDetector._negative_embedding)
        is_negative = neg_sim > 0.55

        boosts: Dict[str, float] = {}
        for major_name, major_emb in SemanticIntentDetector._major_embeddings.items():
            sim = self._cosine(user_emb, major_emb)

            if sim < threshold:
                continue

            if is_negative:
                # Penalise instead of boost
                boosts[major_name] = max(0.1, 1.0 - sim)
            else:
                # Scale similarity (0.35-1.0) → boost (1.0-6.0)
                # Linear map: threshold → 1.0, perfect → 6.0
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
        Detect negative intent for each major using SBERT.

        Builds per-major negative phrases dynamically from the database
        and checks if user text is semantically similar.

        Returns {major: penalty_factor} where < 1.0 means penalised.
        """
        if not text or not text.strip():
            return {}

        enc = SemanticIntentDetector._encoder
        user_emb = enc.encode(text.lower())

        # First check if text has any negative sentiment at all
        neg_sim = self._cosine(user_emb, SemanticIntentDetector._negative_embedding)
        if neg_sim < 0.25:
            # No detectable negative sentiment
            return {}

        penalties: Dict[str, float] = {}

        for major_name, major_emb in SemanticIntentDetector._major_embeddings.items():
            # Create a negative version: "I don't want [major description]"
            info = MAJOR_DATABASE.get(major_name, {})
            desc = info.get("description", major_name)
            neg_text = f"I don't want {desc} I hate {major_name}"
            neg_emb = enc.encode(neg_text.lower())

            sim_to_negative = self._cosine(user_emb, neg_emb)

            if sim_to_negative > 0.50:
                # Strong negative match → heavy penalty
                # Similarity 0.50→0.5 penalty, 0.80→0.05 penalty
                penalty = max(0.05, 1.0 - sim_to_negative)
                penalties[major_name] = penalty

        if penalties:
            logger.info(f"Exclusion penalties: {penalties}")

        return penalties

    def extract_keywords(self, text: str) -> List[str]:
        """Minimal keyword extraction (kept for compatibility)"""
        if not text:
            return []
        words = set(text.lower().split())
        # Return any words that appear in major keywords (from database)
        all_keywords = set()
        for info in MAJOR_DATABASE.values():
            all_keywords.update(k.lower() for k in info.get("keywords", []))
        return [w for w in words if w in all_keywords]


# Singleton
_detector_instance = None


def get_semantic_detector() -> SemanticIntentDetector:
    global _detector_instance
    if _detector_instance is None:
        _detector_instance = SemanticIntentDetector()
    return _detector_instance
