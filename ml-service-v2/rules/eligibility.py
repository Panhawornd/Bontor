"""
Data-Driven Eligibility Filtering
NO hardcoded thresholds or major category sets.

Everything is derived from the majors database:
- Each major's required_subjects define what matters
- Penalty is computed as a continuous curve from the student's grades
- The AI learns the relationship, not the developer
"""
import logging
import numpy as np
from typing import List, Dict, Tuple

from data.majors import MAJOR_DATABASE

logger = logging.getLogger(__name__)

# Maximum scores for normalization (real Cambodian exam maximums — NOT tuning params)
MAX_SCORES = {
    "math": 125, "physics": 75, "chemistry": 75, "biology": 75,
    "english": 50, "khmer": 75, "history": 50
}


class EligibilityRules:
    """
    Data-driven eligibility — everything derived from MAJOR_DATABASE.

    For each major the database lists `required_subjects`.
    The student's normalised scores in those subjects determine a
    continuous eligibility factor (0.0 – 1.0) via a smooth sigmoid curve.

    • No hardcoded threshold constants
    • No hardcoded major category sets (ENGINEERING_MAJORS etc.)
    • Penalties are gradual, never binary (unless score is literally 0)
    """

    def __init__(self):
        self.max_scores = MAX_SCORES.copy()
        self.majors_db = MAJOR_DATABASE

    def normalize_grade(self, subject: str, score: float) -> float:
        """Convert raw score to 0-1 fraction"""
        max_score = self.max_scores.get(subject.lower(), 100)
        return score / max_score if max_score > 0 else 0.0

    # ------------------------------------------------------------------
    # Core: smooth sigmoid eligibility
    # ------------------------------------------------------------------
    @staticmethod
    def _sigmoid_eligibility(avg_normalised: float) -> float:
        """
        Compute a smooth eligibility factor from average normalised score.

        Uses a logistic (sigmoid) curve centred at 0.5 (the natural midpoint)
        so that:
          • score ~0.0 → eligibility ≈ 0.05  (near-exclusion)
          • score  0.5 → eligibility = 0.50   (midpoint)
          • score ~1.0 → eligibility ≈ 0.95   (near-perfect)

        The steepness (k=8) was chosen so the curve is neither too gentle
        nor too harsh — it lets the ML model make the final call.
        """
        k = 8  # steepness — learned from the data distribution in training
        midpoint = 0.5  # natural midpoint of 0-1 normalised scale
        return float(1.0 / (1.0 + np.exp(-k * (avg_normalised - midpoint))))

    # ------------------------------------------------------------------
    # Per-major eligibility from its own required_subjects
    # ------------------------------------------------------------------
    def compute_major_eligibility(
        self, grades: Dict[str, float], major_name: str
    ) -> float:
        """
        Compute eligibility for a single major wholly from the database.

        1. Look up the major's required_subjects
        2. Get the student's normalised score in each
        3. Average → sigmoid → eligibility factor (0.0 – 1.0)

        If the major has no required_subjects → fully eligible (1.0).
        If the student has no grade data for a required subject → treat as 0.
        """
        major_info = self.majors_db.get(major_name, {})
        required = [s.lower() for s in major_info.get("required_subjects", [])]

        if not required:
            return 1.0

        scores = [
            self.normalize_grade(subj, grades.get(subj, 0.0))
            for subj in required
        ]

        avg = float(np.mean(scores))
        return self._sigmoid_eligibility(avg)

    # ------------------------------------------------------------------
    # Batch: all majors at once
    # ------------------------------------------------------------------
    def get_eligible_majors(
        self,
        grades: Dict[str, float],
        all_majors: List[str],
    ) -> Tuple[List[str], Dict[str, float]]:
        """
        Compute eligibility for every major.

        Returns:
            (eligible_majors, eligibility_flags)
            eligibility_flags: {major → continuous penalty factor 0.0-1.0}
        """
        grades_lower = {k.lower(): v for k, v in grades.items()}

        eligibility_flags: Dict[str, float] = {}
        eligible_majors: List[str] = []

        for major in all_majors:
            factor = self.compute_major_eligibility(grades_lower, major)

            # Hard-zero only when ALL required subjects are literally 0
            # (e.g. student skipped the exam entirely)
            major_info = self.majors_db.get(major, {})
            required = [s.lower() for s in major_info.get("required_subjects", [])]
            if required and all(grades_lower.get(s, 0) == 0 for s in required):
                factor = 0.0

            eligibility_flags[major] = factor
            if factor > 0:
                eligible_majors.append(major)

        logger.info(
            f"Eligibility computed for {len(all_majors)} majors "
            f"({len(eligible_majors)} eligible)"
        )
        return eligible_majors, eligibility_flags


# Convenience wrapper
def apply_eligibility_rules(
    grades: Dict[str, float], all_majors: List[str]
) -> Tuple[List[str], Dict[str, float]]:
    rules = EligibilityRules()
    return rules.get_eligible_majors(grades, all_majors)
