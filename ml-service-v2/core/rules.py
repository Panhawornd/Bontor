"""
Rule-Based Filtering and Enhancement
Validates predictions against academic and domain constraints
"""
import re
from typing import List, Dict
from data.majors import MAJOR_DATABASE

class RuleEngine:
    """Applies rules to filter and enhance ML predictions"""
    
    def __init__(self):
        self.majors_db = MAJOR_DATABASE
    
    def apply_rules(
        self,
        predictions: List[Dict],
        grades: Dict[str, float],
        interests: str
    ) -> List[Dict]:
        """
        Filter and enhance predictions with business rules
        
        Args:
            predictions: ML model predictions
            grades: User grades
            interests: User interests text
            
        Returns:
            Filtered and enhanced predictions
        """
        filtered = []
        
        for pred in predictions:
            major = pred['major']
            
            # Check if major exists in database
            if major not in self.majors_db:
                continue
            
            major_info = self.majors_db[major]
            
            # Rule 1: Check required subjects
            eligible = self._check_eligibility(grades, major_info)
            if not eligible:
                pred['probability'] *= 0.5  # Penalty but don't eliminate
            
            # Rule 2: Boost if interests match keywords
            keyword_match_count = self._check_keyword_match_count(interests, major_info)
            if keyword_match_count >= 1:
                # Hyper-boost to ensure semantic keywords absolutely dominate ML noise
                pred['probability'] *= (1 + (50.0 * keyword_match_count)) 
                pred['source'] += f" + Semantic-HyperBoost({keyword_match_count})"
            
            # Add major details
            pred['description'] = major_info.get('description', '')
            pred['required_subjects'] = major_info.get('required_subjects', [])
            pred['career_paths'] = major_info.get('career_paths', [])
            
            filtered.append(pred)
        
        # Re-normalize probabilities
        total = sum(p['probability'] for p in filtered)
        if total > 0:
            for pred in filtered:
                pred['probability'] /= total
        
        # Re-sort
        filtered.sort(key=lambda x: x['probability'], reverse=True)
        
        # Limit to max 4 and apply high-relevance threshold
        top_recommendations = [p for p in filtered if p['probability'] > 0.05][:4]
        
        # If there's an extremely strong single match (e.g. > 70%), maybe just show that one?
        # For now, stick to top 4 of high quality.
        
        return top_recommendations
    
    def _check_eligibility(self, grades: Dict[str, float], major_info: Dict) -> bool:
        """Check if user meets minimum grade requirements"""
        required_subjects = major_info.get('required_subjects', [])
        
        for subject in required_subjects:
            if subject not in grades or grades[subject] < 50:
                return False
        
        return True
    
    def _check_keyword_match_count(self, interests: str, major_info: Dict) -> int:
        """Count how many keywords match the interests (using whole words only)"""
        keywords = major_info.get('keywords', [])
        interests_lower = interests.lower()
        
        matches = 0
        for kw in keywords:
            # Use regex to find whole word matches only
            # This prevents "logic" from matching "biological"
            pattern = rf"\b{re.escape(kw.lower())}\b"
            if re.search(pattern, interests_lower):
                matches += 1
        return matches
