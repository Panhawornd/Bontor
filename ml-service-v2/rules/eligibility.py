"""
Rule-Based Eligibility Filtering (Subject-Aware)
RULES OVERRIDE ML - as per requirements

Apply academic rules BEFORE ML predictions are used:
- Math threshold → exclude Engineering/CS
- Khmer Literature threshold → penalize social science
- History threshold → penalize humanities
- English threshold → exclude international programs
"""
import logging
from typing import List, Dict, Tuple, Set

logger = logging.getLogger(__name__)

# Subject thresholds (percentage-based, 0-100 scale)
SUBJECT_THRESHOLDS = {
    "math": 50,         # Minimum for STEM majors
    "physics": 45,      # Minimum for engineering
    "chemistry": 45,    # Minimum for chemistry-related
    "biology": 45,      # Minimum for life sciences
    "english": 50,      # Minimum for international programs
    "khmer": 45,        # Minimum for social sciences
    "history": 40,      # Minimum for humanities
}

# Maximum scores for normalization
MAX_SCORES = {
    "math": 125,
    "physics": 75,
    "chemistry": 75,
    "biology": 75,
    "english": 50,
    "khmer": 75,
    "history": 50
}

# Major categories for rule application
ENGINEERING_MAJORS = {
    "Software Engineering", "Civil Engineering", "Electrical Engineering",
    "Mechanical Engineering", "Chemical Engineering", "Data Science",
    "Cybersecurity", "Telecommunication and Networking", "Architecture"
}

STEM_MAJORS = ENGINEERING_MAJORS | {
    "Medicine", "Pharmacy", "Dentistry"
}

INTERNATIONAL_MAJORS = {
    "International Relations", "Business Administration", "Business Management",
    "Finance", "Law"
}

SOCIAL_SCIENCE_MAJORS = {
    "Psychology", "International Relations", "Law", "Education"
}

HUMANITIES_MAJORS = {
    "Education", "International Relations", "Law", "Graphic Design"
}


class EligibilityRules:
    """
    Subject-aware eligibility rules for major filtering
    RULES OVERRIDE ML - apply BEFORE ML predictions
    """
    
    def __init__(self):
        self.thresholds = SUBJECT_THRESHOLDS.copy()
        self.max_scores = MAX_SCORES.copy()
    
    def normalize_grade(self, subject: str, score: float) -> float:
        """Convert raw score to percentage (0-100)"""
        max_score = self.max_scores.get(subject.lower(), 100)
        return (score / max_score) * 100
    
    def check_math_eligibility(self, grades: Dict[str, float]) -> Tuple[bool, Set[str]]:
        """
        Check Math threshold
        If Math < threshold → exclude Engineering / CS majors
        
        Returns:
            (is_eligible, excluded_majors)
        """
        math_score = grades.get("math", 0)
        math_pct = self.normalize_grade("math", math_score)
        
        if math_pct < self.thresholds["math"]:
            logger.info(f"Math ({math_pct:.1f}%) below threshold - excluding engineering majors")
            return False, ENGINEERING_MAJORS.copy()
        
        return True, set()
    
    def check_english_eligibility(self, grades: Dict[str, float]) -> Tuple[bool, Set[str]]:
        """
        Check English threshold
        If English < threshold → exclude international programs
        
        Returns:
            (is_eligible, excluded_majors)
        """
        english_score = grades.get("english", 0)
        english_pct = self.normalize_grade("english", english_score)
        
        if english_pct < self.thresholds["english"]:
            logger.info(f"English ({english_pct:.1f}%) below threshold - excluding international majors")
            return False, INTERNATIONAL_MAJORS.copy()
        
        return True, set()
    
    def check_khmer_eligibility(self, grades: Dict[str, float]) -> Dict[str, float]:
        """
        Check Khmer Literature threshold
        If Khmer < threshold → penalize social science majors
        
        Returns:
            Dict of major penalties (multiply factor, 1.0 = no penalty)
        """
        khmer_score = grades.get("khmer", 0)
        khmer_pct = self.normalize_grade("khmer", khmer_score)
        
        penalties = {}
        
        if khmer_pct < self.thresholds["khmer"]:
            logger.info(f"Khmer ({khmer_pct:.1f}%) below threshold - penalizing social sciences")
            for major in SOCIAL_SCIENCE_MAJORS:
                penalties[major] = 0.6  # 40% penalty
        
        return penalties
    
    def check_history_eligibility(self, grades: Dict[str, float]) -> Dict[str, float]:
        """
        Check History threshold
        If History < threshold → penalize humanities majors
        
        Returns:
            Dict of major penalties (multiply factor)
        """
        history_score = grades.get("history", 0)
        history_pct = self.normalize_grade("history", history_score)
        
        penalties = {}
        
        if history_pct < self.thresholds["history"]:
            logger.info(f"History ({history_pct:.1f}%) below threshold - penalizing humanities")
            for major in HUMANITIES_MAJORS:
                penalties[major] = 0.7  # 30% penalty
        
        return penalties
    
    def check_science_requirements(self, grades: Dict[str, float], major: str) -> float:
        """
        Check science subject requirements for specific majors
        
        Returns:
            Penalty multiplier (1.0 = eligible, <1.0 = penalized, 0 = excluded)
        """
        # Medicine, Pharmacy, Dentistry require Biology + Chemistry
        medical_majors = {"Medicine", "Pharmacy", "Dentistry"}
        
        if major in medical_majors:
            biology_pct = self.normalize_grade("biology", grades.get("biology", 0))
            chemistry_pct = self.normalize_grade("chemistry", grades.get("chemistry", 0))
            
            if biology_pct < 50 or chemistry_pct < 50:
                return 0.3  # Severe penalty
            elif biology_pct < 70 or chemistry_pct < 70:
                return 0.7  # Moderate penalty
        
        # Chemical Engineering requires Chemistry
        if major == "Chemical Engineering":
            chemistry_pct = self.normalize_grade("chemistry", grades.get("chemistry", 0))
            if chemistry_pct < 50:
                return 0.4
        
        # Engineering majors require Physics
        if major in ENGINEERING_MAJORS - {"Software Engineering", "Data Science", "Cybersecurity"}:
            physics_pct = self.normalize_grade("physics", grades.get("physics", 0))
            if physics_pct < 45:
                return 0.5
        
        return 1.0
    
    def get_eligible_majors(
        self,
        grades: Dict[str, float],
        all_majors: List[str]
    ) -> Tuple[List[str], Dict[str, float]]:
        """
        Get list of eligible majors and eligibility flags/penalties
        
        Args:
            grades: Dict of subject → raw score
            all_majors: List of all available majors
            
        Returns:
            (eligible_majors, eligibility_flags)
            eligibility_flags: Dict of major → penalty multiplier
        """
        # Normalize grades to lowercase keys
        grades_lower = {k.lower(): v for k, v in grades.items()}
        
        # Apply exclusion rules
        excluded = set()
        
        _, math_excluded = self.check_math_eligibility(grades_lower)
        excluded.update(math_excluded)
        
        _, english_excluded = self.check_english_eligibility(grades_lower)
        excluded.update(english_excluded)
        
        # Apply penalty rules
        penalties = {}
        
        khmer_penalties = self.check_khmer_eligibility(grades_lower)
        penalties.update(khmer_penalties)
        
        history_penalties = self.check_history_eligibility(grades_lower)
        for major, penalty in history_penalties.items():
            if major in penalties:
                penalties[major] *= penalty  # Compound penalties
            else:
                penalties[major] = penalty
        
        # Check science requirements for each major
        for major in all_majors:
            science_penalty = self.check_science_requirements(grades_lower, major)
            if science_penalty < 1.0:
                if major in penalties:
                    penalties[major] *= science_penalty
                else:
                    penalties[major] = science_penalty
        
        # Build eligibility flags (1.0 for excluded = 0)
        eligibility_flags = {}
        eligible_majors = []
        
        for major in all_majors:
            if major in excluded:
                eligibility_flags[major] = 0.0
            elif major in penalties:
                eligibility_flags[major] = penalties[major]
                eligible_majors.append(major)  # Still eligible but penalized
            else:
                eligibility_flags[major] = 1.0
                eligible_majors.append(major)
        
        return eligible_majors, eligibility_flags
    
    def filter_predictions(
        self,
        predictions: List[Dict],
        grades: Dict[str, float]
    ) -> List[Dict]:
        """
        Filter ML predictions using eligibility rules
        RULES OVERRIDE ML
        
        Args:
            predictions: ML model predictions [{major, probability, ...}]
            grades: User grades
            
        Returns:
            Filtered predictions with rules applied
        """
        all_majors = [p['major'] for p in predictions]
        eligible_majors, eligibility_flags = self.get_eligible_majors(grades, all_majors)
        
        filtered = []
        for pred in predictions:
            # Make a shallow copy to avoid mutating caller's data
            pred_copy = dict(pred)
            major = pred_copy['major']
            flag = eligibility_flags.get(major, 1.0)
            
            if flag == 0.0:
                # Excluded by rules - skip entirely
                continue
            
            # Apply penalty to probability
            pred_copy['probability'] *= flag
            pred_copy['rule_applied'] = flag < 1.0
            filtered.append(pred_copy)
        
        # Re-sort by probability
        filtered.sort(key=lambda x: x['probability'], reverse=True)
        
        return filtered


def apply_eligibility_rules(
    grades: Dict[str, float],
    all_majors: List[str]
) -> Tuple[List[str], Dict[str, float]]:
    """
    Convenience function to apply eligibility rules
    
    Args:
        grades: User grades (subject → score)
        all_majors: All available majors
        
    Returns:
        (eligible_majors, eligibility_flags)
    """
    rules = EligibilityRules()
    return rules.get_eligible_majors(grades, all_majors)
