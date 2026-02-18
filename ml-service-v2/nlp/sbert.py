"""
SBERT Embedding Module
Model: all-MiniLM-L6-v2 (DO NOT retrain - load once, reuse)

Includes optional domain fine-tuning capability for education recommendations.
"""
import logging
import threading
from typing import List, Optional, Dict, Union, Tuple
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

    # ------------------------------------------------------------------
    # Domain Fine-Tuning (Education Recommendations)
    # ------------------------------------------------------------------
    def fine_tune_on_domain(
        self,
        training_pairs: Optional[List[Tuple[str, str]]] = None,
        epochs: int = 3,
        batch_size: int = 16,
        output_path: Optional[str] = None,
    ) -> bool:
        """
        Fine-tune SBERT on domain-specific education recommendation pairs.

        Uses contrastive learning: pairs of (student_interest, major_description)
        that should be semantically close. This improves similarity scores
        for education-specific vocabulary.

        Args:
            training_pairs: List of (anchor, positive) text pairs.
                            If None, uses built-in education domain pairs.
            epochs: Training epochs (default: 3, keep low to avoid overfitting)
            batch_size: Training batch size
            output_path: Path to save fine-tuned model (optional)

        Returns:
            True if fine-tuning succeeded
        """
        if self.model is None:
            logger.error("No base model loaded – cannot fine-tune")
            return False

        try:
            from sentence_transformers import InputExample, losses
            from torch.utils.data import DataLoader

            if training_pairs is None:
                training_pairs = _get_education_domain_pairs()

            logger.info(
                f"Fine-tuning SBERT on {len(training_pairs)} domain pairs "
                f"({epochs} epochs)…"
            )

            # Build InputExamples
            examples = [
                InputExample(texts=[a, b]) for a, b in training_pairs
            ]
            dataloader = DataLoader(examples, shuffle=True, batch_size=batch_size)
            loss = losses.MultipleNegativesRankingLoss(self.model)

            self.model.fit(
                train_objectives=[(dataloader, loss)],
                epochs=epochs,
                warmup_steps=int(len(dataloader) * 0.1),
                show_progress_bar=True,
            )

            if output_path:
                self.model.save(output_path)
                logger.info(f"Fine-tuned model saved to {output_path}")

            # Invalidate embedding cache
            global _embedding_cache
            _embedding_cache.clear()
            logger.info("Embedding cache cleared after fine-tuning")

            return True

        except ImportError as e:
            logger.error(f"Fine-tuning dependencies missing: {e}")
            return False
        except Exception as e:
            logger.error(f"Fine-tuning failed: {e}")
            return False


def _get_education_domain_pairs() -> List[Tuple[str, str]]:
    """
    Built-in education domain training pairs for contrastive learning.
    Each pair consists of (student_interest_text, major_description).
    """
    return [
        # Software Engineering
        ("I love coding and building apps", "software development programming system architecture"),
        ("I want to be a developer", "software engineering backend frontend full stack"),
        ("programming python javascript", "coding algorithms data structures software"),
        ("building websites and mobile apps", "web development mobile development software engineering"),
        ("I enjoy solving coding challenges", "programming problem solving algorithm design"),

        # Medicine
        ("I want to help sick people", "medicine medical treatment health diseases"),
        ("I love biology and anatomy", "human health diseases medical treatment surgery"),
        ("becoming a doctor or surgeon", "medicine physician surgeon medical specialist"),
        ("healthcare and saving lives", "medical healthcare patient care treatment"),

        # Civil Engineering
        ("I want to build bridges and roads", "civil engineering infrastructure construction structures"),
        ("construction of buildings", "civil engineering structural design building construction"),
        ("designing large scale infrastructure", "transportation engineering public works bridges roads"),

        # Data Science
        ("analyzing data and finding patterns", "data science analytics statistics machine learning"),
        ("machine learning artificial intelligence", "data science ML algorithms predictive modeling"),
        ("big data and statistical analysis", "data science data mining statistical computing"),

        # Business
        ("running my own company", "business administration management entrepreneurship"),
        ("marketing and finance", "business management financial analysis marketing strategy"),
        ("becoming a CEO or manager", "business administration leadership organizational management"),

        # Psychology
        ("understanding human behavior", "psychology mental processes behavior cognition"),
        ("helping people with mental health", "psychology counseling therapy mental health"),
        ("why people think and act the way they do", "cognitive psychology behavioral analysis"),

        # Architecture
        ("designing beautiful buildings", "architecture building design structural aesthetics"),
        ("urban planning and spatial design", "architecture urban planning construction design"),

        # Law
        ("justice and legal rights", "law jurisprudence legal practice court justice"),
        ("becoming a lawyer", "law legal attorney advocate litigation"),

        # Electrical Engineering
        ("circuits and electronics", "electrical engineering circuit design power systems electronics"),
        ("power systems and signals", "electrical engineering electromagnetism control systems"),

        # Cybersecurity
        ("protecting systems from hackers", "cybersecurity network security ethical hacking encryption"),
        ("digital security and encryption", "cybersecurity information security privacy protection"),

        # Education
        ("teaching students in a classroom", "education teaching pedagogy curriculum development"),
        ("becoming a teacher or professor", "education learning classroom instruction mentoring"),

        # Finance
        ("investing money and banking", "finance investment banking financial analysis"),
        ("stock market and financial planning", "finance financial markets portfolio management"),

        # Graphic Design
        ("creating logos and posters", "graphic design visual communication branding"),
        ("visual art and digital design", "graphic design illustration typography layout"),
    ]


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
