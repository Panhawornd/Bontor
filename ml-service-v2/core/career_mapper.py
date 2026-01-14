"""
Career and Skill Mapping Module
Maps majors to careers and identifies skill gaps
"""
from typing import List, Dict
from data.careers import CAREER_DATABASE

class CareerMapper:
    """Maps majors to relevant careers and skills"""
    
    def __init__(self):
        self.careers_db = CAREER_DATABASE
    
    def map_careers(self, majors: List[Dict]) -> List[Dict]:
        """
        Find relevant careers for recommended majors
        
        Args:
            majors: List of recommended majors
            
        Returns:
            List of career recommendations
        """
        careers = []
        seen = set()
        
        for major_rec in majors[:5]:  # Top 5 majors
            major = major_rec['major']
            career_paths = major_rec.get('career_paths', [])
            
            for career_name in career_paths:
                if career_name in seen:
                    continue
                
                if career_name in self.careers_db:
                    career_info = self.careers_db[career_name]
                    careers.append({
                        "name": career_name,
                        "description": career_info.get("description", ""),
                        "required_skills": career_info.get("required_skills", []),
                        "avg_salary": career_info.get("avg_salary", "Varies"),
                        "related_major": major
                    })
                    seen.add(career_name)
                
                if len(careers) >= 10:
                    break
            
            if len(careers) >= 10:
                break
        
        return careers
    
    def identify_skill_gaps(
        self,
        careers: List[Dict],
        grades: Dict[str, float]
    ) -> List[Dict]:
        """
        Identify skill gaps based on grades and career requirements
        
        Args:
            careers: Recommended careers
            grades: User grades
            
        Returns:
            List of skill gaps with improvement suggestions
        """
        gaps = []
        
        # Analyze grade weaknesses
        weak_subjects = [
            subject for subject, score in grades.items()
            if score < 70
        ]
        
        for subject in weak_subjects:
            gaps.append({
                "skill": subject.capitalize(),
                "current_level": "Needs Improvement",
                "importance": "High",
                "suggestions": [
                    f"Practice {subject} regularly",
                    f"Seek tutoring in {subject}",
                    f"Review {subject} fundamentals"
                ]
            })
        
        # Add career-specific skills
        all_required_skills = set()
        for career in careers[:3]:
            all_required_skills.update(career.get('required_skills', []))
        
        for skill in list(all_required_skills)[:5]:
            if skill not in [g['skill'] for g in gaps]:
                gaps.append({
                    "skill": skill,
                    "current_level": "To Be Developed",
                    "importance": "Medium",
                    "suggestions": [
                        f"Learn {skill} through online courses",
                        f"Practice {skill} projects",
                        f"Join {skill} communities"
                    ]
                })
        
        return gaps[:8]  # Top 8 gaps
