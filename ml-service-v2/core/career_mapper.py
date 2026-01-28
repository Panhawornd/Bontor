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
        top_major: Dict,
        grades: Dict[str, float]
    ) -> List[Dict]:
        """
        Identify skill gaps based on top major requirements (University Fundamentals)
        """
        gaps = []
        max_scores = {
            "math": 125, "physics": 75, "chemistry": 75, "biology": 75,
            "english": 50, "khmer": 75, "history": 50
        }
        
        major_name = top_major.get('major', 'General')
        required_subjects = top_major.get('required_subjects', [])
        
        # 1. Subject-based Fundamentals (Academic)
        for subject in required_subjects:
            if subject in grades:
                score = grades[subject]
                max_score = max_scores.get(subject.lower(), 100)
                percentage = (score / max_score) * 100
                
                if percentage < 80:
                    gaps.append({
                        "skill": f"Academic: {subject.capitalize()} Mastery",
                        "current_level": f"{round(percentage, 1)}%",
                        "importance": "High",
                        "suggestions": [
                            f"Focus on {subject} topics required for {major_name} university entry",
                            f"Strengthen your foundation in {subject} through intensive practice",
                            f"Aim for at least 80% proficiency to follow {major_name} lectures effectively"
                        ]
                    })
        
        # 2. Major-Specific Technical/Soft Fundamentals
        major_fundamentals = {
            "Software": ["Computational Thinking", "Algorithm Logic", "Modular Programming"],
            "Data Science": ["Statistical Reasoning", "Data Interpretation", "Quantitative Analysis"],
            "Cybersecurity": ["Threat Modeling", "Encryption Logic", "Network Defense Basics"],
            "Networking": ["Protocol Architectures", "Signal Transmission", "Network Topology Design"],
            "Chemical": ["Mass and Energy Balance", "Chemical Thermodynamics", "Process Design Basics"],
            "Engineering": ["Vector Calculus", "Problem Solving Logic", "Technical Sketching"],
            "Medicine": ["Life Science Ethics", "Analytical Observation", "Complex Systems Thinking"],
            "Dentistry": ["Digital Oral Imaging", "Manual Dexterity Basics", "Oral Anatomy Fundamentals"],
            "Pharmacy": ["Chemical Bonding Basics", "Molecular Logic", "Precision Measurement"],
            "Finance": ["Investment Analysis", "Risk Quantitative Modeling", "Asset Valuation"],
            "Business": ["Market Logic", "Strategic Planning", "Financial Literacy"],
            "Law": ["Logical Persuasion", "Constitutional Literacy", "Verbal Reasoning"],
            "International": ["Global Perspectives", "Political Theory", "Cross-Cultural Communication"],
            "Design": ["Visual Hierarchy", "Color Theory", "compositional Logic"],
            "Architecture": ["Spatial Composition", "Structural Aesthetics", "Architectural Sketching"],
            "Psychology": ["Ethical Observation", "Human Development Theory", "Social Patterns"],
            "Education": ["Pedagogical Theory", "Classroom Management Logic", "Educational Psychology Basics"]
        }
        
        # Find matching category
        specific_skills = []
        for category, skills in major_fundamentals.items():
            if category.lower() in major_name.lower():
                specific_skills = skills
                break
        
        # Default skills if no category matches
        if not specific_skills:
            specific_skills = ["Critical Thinking", "Academic Research", "Technical Writing"]
            
        for skill in specific_skills:
            gaps.append({
                "skill": f"Fundamental: {skill}",
                "current_level": "To Be Developed",
                "importance": "Medium",
                "suggestions": [
                    f"Begin learning {skill} foundations for your {major_name} degree",
                    f"Explore introductory resources for {skill} online",
                    f"Join student groups focused on {skill}"
                ]
            })
            
        return gaps[:6]  # Limit to top 6 gaps
