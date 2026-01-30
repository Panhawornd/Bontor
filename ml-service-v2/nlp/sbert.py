"""
SBERT Embedding Module
Model: all-MiniLM-L6-v2 (DO NOT retrain - load once, reuse)
"""
import logging
import threading
from typing import List, Optional, Dict, Union
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
    _instance_lock = threading.Lock()
    _model_lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._instance_lock:
                # Double-check pattern
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if SBERTEncoder._model is not None:
            return
        
        with SBERTEncoder._model_lock:
            # Double-check inside lock
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
    
    def encode(self, text: str, convert_to_numpy: bool = True) -> Union[np.ndarray, 'torch.Tensor']:
        """
        Encode single text into embedding vector
        
        Args:
            text: Text to encode (should be cleaned first!)
            convert_to_numpy: Return numpy array vs tensor
            
        Returns:
            Embedding vector (384-dimensional for MiniLM)
        """
        if not text or not text.strip():
            # Return zero vector for empty text - consistent type based on convert_to_numpy
            if convert_to_numpy:
                return np.zeros(384)
            else:
                import torch
                return torch.zeros(384)
        
        try:
            embedding = self.model.encode(
                text,
                convert_to_tensor=not convert_to_numpy,
                convert_to_numpy=convert_to_numpy
            )
            return embedding
            
        except Exception as e:
            logger.error(f"Encoding failed: {e}")
            if convert_to_numpy:
                return np.zeros(384)
            else:
                import torch
                return torch.zeros(384)
    
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
            # Return properly shaped empty array
            return np.zeros((0, 384), dtype=np.float32)
        
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
            # Always request numpy to simplify reconstruction
            valid_embeddings = self.model.encode(
                valid_texts,
                convert_to_tensor=False,
                convert_to_numpy=True,
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
