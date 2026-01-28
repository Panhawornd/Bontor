"""
SBERT Embedding Module
Model: all-MiniLM-L6-v2 (DO NOT retrain - load once, reuse)
"""
import logging
from typing import List, Optional, Dict
import numpy as np

logger = logging.getLogger(__name__)


class SBERTEncoder:
    """
    Singleton SBERT encoder using all-MiniLM-L6-v2
    - Loads model once on first use
    - Reuses model for all requests
    - DO NOT retrain
    """
    
    _instance = None
    _model = None
    _device = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if SBERTEncoder._model is not None:
            return
        
        self._load_model()
    
    def _load_model(self):
        """Load SBERT model (all-MiniLM-L6-v2) - DO NOT retrain"""
        try:
            import torch
            from sentence_transformers import SentenceTransformer
            
            # Determine device
            SBERTEncoder._device = 'cuda' if torch.cuda.is_available() else 'cpu'
            logger.info(f"Loading SBERT on device: {SBERTEncoder._device}")
            
            # Load model - all-MiniLM-L6-v2 (HARD CONSTRAINT)
            SBERTEncoder._model = SentenceTransformer('all-MiniLM-L6-v2')
            
            if SBERTEncoder._device == 'cuda':
                SBERTEncoder._model = SBERTEncoder._model.to('cuda')
            
            logger.info("SBERT model (all-MiniLM-L6-v2) loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load SBERT model: {e}")
            raise RuntimeError(f"SBERT model loading failed: {e}")
    
    @property
    def model(self):
        """Get the loaded model"""
        return SBERTEncoder._model
    
    @property
    def device(self):
        """Get the current device"""
        return SBERTEncoder._device
    
    def encode(self, text: str, convert_to_numpy: bool = True) -> np.ndarray:
        """
        Encode single text into embedding vector
        
        Args:
            text: Text to encode (should be cleaned first!)
            convert_to_numpy: Return numpy array vs tensor
            
        Returns:
            Embedding vector (384-dimensional for MiniLM)
        """
        if not text or not text.strip():
            # Return zero vector for empty text
            return np.zeros(384) if convert_to_numpy else None
        
        try:
            embedding = self.model.encode(
                text,
                convert_to_tensor=not convert_to_numpy,
                convert_to_numpy=convert_to_numpy
            )
            return embedding
            
        except Exception as e:
            logger.error(f"Encoding failed: {e}")
            return np.zeros(384) if convert_to_numpy else None
    
    def encode_batch(self, texts: List[str], convert_to_numpy: bool = True) -> np.ndarray:
        """
        Encode multiple texts into embedding matrix
        
        Args:
            texts: List of texts to encode
            convert_to_numpy: Return numpy array vs tensor
            
        Returns:
            Embedding matrix (N x 384)
        """
        if not texts:
            return np.array([])
        
        # Filter empty texts, keep track of indices
        valid_texts = []
        valid_indices = []
        for i, t in enumerate(texts):
            if t and t.strip():
                valid_texts.append(t)
                valid_indices.append(i)
        
        if not valid_texts:
            return np.zeros((len(texts), 384))
        
        try:
            valid_embeddings = self.model.encode(
                valid_texts,
                convert_to_tensor=not convert_to_numpy,
                convert_to_numpy=convert_to_numpy,
                show_progress_bar=False
            )
            
            # Reconstruct full matrix with zeros for empty texts
            result = np.zeros((len(texts), 384))
            for i, idx in enumerate(valid_indices):
                result[idx] = valid_embeddings[i]
            
            return result
            
        except Exception as e:
            logger.error(f"Batch encoding failed: {e}")
            return np.zeros((len(texts), 384))
    
    def get_embedding_dim(self) -> int:
        """Return embedding dimension (384 for MiniLM)"""
        return 384


# Pre-computed embeddings cache (for major/career descriptions)
_embedding_cache: Dict[str, np.ndarray] = {}


def get_cached_embedding(key: str, text: str, encoder: Optional[SBERTEncoder] = None) -> np.ndarray:
    """
    Get embedding from cache or compute and cache it
    
    Args:
        key: Cache key
        text: Text to encode if not cached
        encoder: Optional encoder instance
        
    Returns:
        Embedding vector
    """
    global _embedding_cache
    
    if key in _embedding_cache:
        return _embedding_cache[key]
    
    if encoder is None:
        encoder = SBERTEncoder()
    
    embedding = encoder.encode(text)
    _embedding_cache[key] = embedding
    
    return embedding


def clear_embedding_cache():
    """Clear the embedding cache"""
    global _embedding_cache
    _embedding_cache = {}
