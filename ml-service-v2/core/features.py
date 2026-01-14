"""
Feature Engineering Module
Combines grades, NLP features, and user preferences
"""
import numpy as np
from typing import Dict, List

from .nlp import NLPService

class FeatureEngine:
    """Transforms raw input into ML-ready features"""
    
    def __init__(self):
        self.nlp = NLPService()
        self.subjects = ["math", "physics", "chemistry", "biology", "english", "khmer", "history"]
        self.max_scores = {
            "math": 125, "physics": 75, "chemistry": 75, "biology": 75,
            "english": 50, "khmer": 75, "history": 50
        }
    
    def build_features(
        self,
        grades: Dict[str, float],
        interests: str,
        career_goals: str = ""
    ) -> np.ndarray:
        """
        Build simple feature vector from user input (grade-based only for now)
        
        Returns:
            Feature vector with normalized grades
        """
        # 1. Grade Features (normalized)
        grade_features = []
        for subject in self.subjects:
            score = grades.get(subject, 0)
            max_score = self.max_scores.get(subject, 100)
            grade_features.append(score / max_score)
        
        # 2. Grade Statistics
        grade_values = [grades.get(s, 0) for s in self.subjects]
        grade_stats = [
            np.mean(grade_values) if grade_values else 0,
            np.std(grade_values) if grade_values else 0,
            max(grade_values) if grade_values else 0,
        ]
        
        # 3. NLP Domain Classification
        # We classify the interest against all known majors to get a "semantic score"
        from data.majors import MAJOR_DATABASE
        major_names = sorted(list(MAJOR_DATABASE.keys())) # Sorted for stable indexing
        
        combined_text = f"{interests} {career_goals}".strip()
        if combined_text:
            nlp_scores = self.nlp.classify_domain(combined_text, major_names)
            # Ensure scores are in the same order as major_names
            nlp_features = [nlp_scores.get(m, 0) for m in major_names]
        else:
            nlp_features = [0.0] * len(major_names)
        
        # 4. Combine all features
        # Total: 7 (grades) + 3 (stats) + 16 (nlp) = 26 features
        features = np.concatenate([
            grade_features,
            grade_stats,
            nlp_features
        ])
        
        return features
