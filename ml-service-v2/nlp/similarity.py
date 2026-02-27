"""
Similarity Computation Module
Computes cosine similarity between embeddings for:
- Student ↔ Major matching
- Student ↔ Career matching
"""
import logging
from typing import List, Dict, Tuple
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from .preprocess import clean_text
from .sbert import SBERTEncoder, get_cached_embedding

logger = logging.getLogger(__name__)


class SimilarityEngine:
    """
    Compute semantic similarity scores between text embeddings
    Uses cosine similarity as per requirements
    """
    
    def __init__(self):
        self.encoder = SBERTEncoder()
        self.preprocessor_ready = False
    
    def compute_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """
        Compute cosine similarity between two embeddings
        
        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector
            
        Returns:
            Cosine similarity score (0 to 1)
        """
        if embedding1 is None or embedding2 is None:
            return 0.0
        
        # Reshape for sklearn
        e1 = embedding1.reshape(1, -1)
        e2 = embedding2.reshape(1, -1)
        
        similarity = cosine_similarity(e1, e2)[0][0]
        
        # Ensure result is in [0, 1] range
        return float(max(0.0, min(1.0, similarity)))
    
    def compute_major_similarity_scores(
        self,
        student_text: str,
        majors_data: Dict[str, Dict]
    ) -> Dict[str, float]:
        """
        Compute student ↔ major similarity for all majors
        
        Args:
            student_text: Combined interests + career goals
            majors_data: Major database with descriptions
            
        Returns:
            Dict of {major_name: similarity_score}
        """
        if not student_text.strip():
            return {name: 0.0 for name in majors_data.keys()}
        
        # Clean and encode student text
        clean_student = clean_text(student_text)
        student_embedding = self.encoder.encode(clean_student)
        
        # Compute similarity for each major
        scores = {}
        for major_name, major_info in majors_data.items():
            desc = major_info.get('description', '')
            keywords = major_info.get('keywords', [])
            careers = major_info.get('career_paths', [])
            skills_dict = major_info.get('fundamental_skills', {})
            subjects = major_info.get('required_subjects', [])
            
            # Weight skills by importance
            weighted_skills = []
            for skill, s_info in skills_dict.items():
                imp = s_info.get("importance", "medium")
                if imp == "critical":
                    weighted_skills.extend([skill] * 3)
                elif imp == "high":
                    weighted_skills.extend([skill] * 2)
                else:
                    weighted_skills.append(skill)
            
            # Repeat subjects and keywords for stronger signal
            major_text = (
                f"{desc} "
                f"{' '.join(keywords)} {' '.join(keywords)} "
                f"{' '.join(careers)} "
                f"{' '.join(weighted_skills)} "
                f"{' '.join(subjects)} {' '.join(subjects)}"
            )
            
            cache_key = f"major:{major_name}"
            clean_major = clean_text(major_text)
            major_embedding = get_cached_embedding(cache_key, clean_major, self.encoder)
            
            scores[major_name] = self.compute_similarity(student_embedding, major_embedding)
        
        return scores
    
    def compute_career_similarity_scores(
        self,
        student_text: str,
        careers_data: Dict[str, Dict]
    ) -> Dict[str, float]:
        """
        Compute student ↔ career similarity for all careers
        
        Args:
            student_text: Combined interests + career goals
            careers_data: Career database with descriptions
            
        Returns:
            Dict of {career_name: similarity_score}
        """
        if not student_text.strip():
            return {name: 0.0 for name in careers_data.keys()}
        
        # Clean and encode student text
        clean_student = clean_text(student_text)
        student_embedding = self.encoder.encode(clean_student)
        
        # Compute similarity for each career
        scores = {}
        for career_name, career_info in careers_data.items():
            description = career_info.get('description', '')
            skills = ' '.join(career_info.get('required_skills', []))
            
            # Combine description and skills
            career_text = f"{description} {skills}"
            
            cache_key = f"career:{career_name}"
            clean_career = clean_text(career_text)
            career_embedding = get_cached_embedding(cache_key, clean_career, self.encoder)
            
            scores[career_name] = self.compute_similarity(student_embedding, career_embedding)
        
        return scores
