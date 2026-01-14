"""
University Mapping Module
Maps majors and grades to suitable universities
"""
from typing import List, Dict
from data.universities import UNIVERSITY_DATABASE

class UniversityMapper:
    """Maps recommended majors to suitable universities"""
    
    def __init__(self):
        self.universities_db = UNIVERSITY_DATABASE
    
    def map_universities(
        self,
        majors: List[Dict],
        grades: Dict[str, float]
    ) -> List[Dict]:
        """
        Find suitable universities for recommended majors
        
        Args:
            majors: List of recommended majors
            grades: User grades
            
        Returns:
            List of university recommendations
        """
        universities = []
        seen = set()
        
        # Calculate average grade
        avg_grade = sum(grades.values()) / len(grades) if grades else 0
        
        # Get programs from top majors
        desired_programs = set()
        for major_rec in majors[:5]:  # Top 5 majors
            desired_programs.add(major_rec['major'])
        
        # Find matching universities
        for uni_name, uni_data in self.universities_db.items():
            if uni_name in seen:
                continue
            
            # Check if university offers any desired programs
            offered_programs = set(uni_data['programs'])
            matching_programs = desired_programs.intersection(offered_programs)
            
            if not matching_programs:
                continue
            
            # Check grade eligibility
            min_grade = uni_data['requirements'].get('min_grade', 0)
            
            if avg_grade < min_grade:
                # Still include but flag as "stretch"
                fit = "Stretch"
            elif avg_grade >= min_grade + 10:
                fit = "Safety"
            else:
                fit = "Target"
            
            universities.append({
                "name": uni_name,
                "location": uni_data['location'],
                "matching_programs": list(matching_programs),
                "min_grade_required": min_grade,
                "fit": fit,
                "your_avg_grade": round(avg_grade, 1)
            })
            
            seen.add(uni_name)
            
            if len(universities) >= 10:
                break
        
        # Sort by fit (Target > Safety > Stretch) and grade requirement
        fit_order = {"Target": 1, "Safety": 2, "Stretch": 3}
        universities.sort(key=lambda x: (fit_order.get(x['fit'], 4), -x['min_grade_required']))
        
        return universities[:8]  # Top 8 universities
