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
    
    def compute_similarity_batch(
        self,
        query_embedding: np.ndarray,
        candidate_embeddings: np.ndarray
    ) -> np.ndarray:
        """
        Compute similarity between query and multiple candidates
        
        Args:
            query_embedding: Query embedding (384,)
            candidate_embeddings: Candidate embeddings (N x 384)
            
        Returns:
            Array of similarity scores (N,)
        """
        if query_embedding is None or len(candidate_embeddings) == 0:
            return np.array([])
        
        query = query_embedding.reshape(1, -1)
        similarities = cosine_similarity(query, candidate_embeddings)[0]
        
        # Clamp to [0, 1]
        return np.clip(similarities, 0.0, 1.0)
    
    def compute_text_similarity(self, text1: str, text2: str) -> float:
        """
        End-to-end similarity: clean text → encode → compare
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Cosine similarity score
        """
        # NLTK preprocessing runs BEFORE SBERT
        clean1 = clean_text(text1)
        clean2 = clean_text(text2)
        
        # Encode with SBERT
        emb1 = self.encoder.encode(clean1)
        emb2 = self.encoder.encode(clean2)
        
        return self.compute_similarity(emb1, emb2)
    
    def rank_by_similarity(
        self,
        query_text: str,
        candidates: Dict[str, str],
        top_k: int = 10
    ) -> List[Tuple[str, float]]:
        """
        Rank candidates by similarity to query
        
        Args:
            query_text: Query text (student career goal)
            candidates: Dict of {name: description}
            top_k: Number of top results to return
            
        Returns:
            List of (name, score) tuples, sorted by score descending
        """
        if not query_text.strip() or not candidates:
            return []
        
        # Clean and encode query
        clean_query = clean_text(query_text)
        query_embedding = self.encoder.encode(clean_query)
        
        # Compute similarities
        results = []
        for name, description in candidates.items():
            # Use cached embeddings for descriptions
            cache_key = f"candidate:{name}"
            clean_desc = clean_text(description)
            candidate_embedding = get_cached_embedding(cache_key, clean_desc, self.encoder)
            
            similarity = self.compute_similarity(query_embedding, candidate_embedding)
            results.append((name, similarity))
        
        # Sort by similarity descending
        results.sort(key=lambda x: x[1], reverse=True)
        
        return results[:top_k]
    
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
            description = major_info.get('description', '')
            keywords = ' '.join(major_info.get('keywords', []))
            
            # Combine description and keywords for richer representation
            major_text = f"{description} {keywords}"
            
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
