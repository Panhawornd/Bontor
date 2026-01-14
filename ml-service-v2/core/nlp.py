"""
NLP Processing Module
- Sentence Transformer for semantic similarity
- Zero-Shot Classification for domain detection
"""
import logging
from typing import List, Dict
from sentence_transformers import SentenceTransformer, util
from transformers import pipeline
import torch

logger = logging.getLogger(__name__)

class NLPService:
    """Singleton NLP service for text processing"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        logger.info("Initializing NLP Service...")
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        
        # Load Sentence Transformer
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        if self.device == 'cuda':
            self.embedder = self.embedder.to('cuda')
        
        # Load Zero-Shot Classifier
        self.classifier = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli",
            device=0 if self.device == 'cuda' else -1
        )
        
        self._initialized = True
        logger.info("NLP Service ready")
    
    def get_similarity(self, text1: str, text2: str) -> float:
        """Calculate semantic similarity between two texts"""
        try:
            emb1 = self.embedder.encode(text1, convert_to_tensor=True)
            emb2 = self.embedder.encode(text2, convert_to_tensor=True)
            return float(util.cos_sim(emb1, emb2)[0][0].item())
        except Exception as e:
            logger.error(f"Similarity calculation failed: {e}")
            return 0.0
    
    def classify_domain(self, text: str, candidates: List[str]) -> Dict[str, float]:
        """Classify text into predefined domains using zero-shot"""
        try:
            result = self.classifier(text, candidate_labels=candidates, multi_label=True)
            return dict(zip(result['labels'], result['scores']))
        except Exception as e:
            logger.error(f"Classification failed: {e}")
            return {}
    
    def embed_text(self, text: str):
        """Get embedding vector for text"""
        return self.embedder.encode(text, convert_to_tensor=True)
