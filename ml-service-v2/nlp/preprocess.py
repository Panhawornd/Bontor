"""
Text Preprocessing Module using NLTK
NLTK runs BEFORE SBERT - as per requirements
"""
import re
import logging
import threading
from typing import List

logger = logging.getLogger(__name__)

# Initialize NLTK components (lazy load to avoid startup overhead)
_nltk_initialized = False
_stopwords = None
_lemmatizer = None
_nltk_init_lock = threading.Lock()

def _init_nltk():
    """Initialize NLTK components on first use (thread-safe)"""
    global _nltk_initialized, _stopwords, _lemmatizer
    
    if _nltk_initialized:
        return
    
    with _nltk_init_lock:
        # Double-check pattern inside lock
        if _nltk_initialized:
            return
        
        import nltk
        
        # Download required NLTK data quietly
        try:
            nltk.download('punkt', quiet=True)
            nltk.download('punkt_tab', quiet=True)
            nltk.download('stopwords', quiet=True)
            nltk.download('wordnet', quiet=True)
        except Exception as e:
            logger.warning(f"NLTK download warning: {e}")
        
        from nltk.corpus import stopwords
        from nltk.stem import WordNetLemmatizer
        
        _stopwords = set(stopwords.words('english'))
        _lemmatizer = WordNetLemmatizer()
        _nltk_initialized = True
        logger.info("NLTK components initialized")


def clean_text(text: str) -> str:
    """
    Clean text using NLTK preprocessing pipeline:
    1. Lowercase
    2. Tokenize
    3. Remove stopwords
    4. Lemmatize
    5. Return cleaned string
    
    Args:
        text: Raw input text
        
    Returns:
        Cleaned, preprocessed text string
    """
    if not text or not text.strip():
        return ""
    
    # Capture original for fallback
    orig_text = text
    
    _init_nltk()
    
    from nltk.tokenize import word_tokenize
    
    try:
        # Step 1: Lowercase
        text = text.lower()
        
        # Step 2: Remove special characters (keep alphanumeric and spaces)
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)
        
        # Step 3: Tokenize
        tokens = word_tokenize(text)
        
        # Step 4: Remove stopwords
        tokens = [t for t in tokens if t not in _stopwords and len(t) > 1]
        
        # Step 5: Lemmatize
        tokens = [_lemmatizer.lemmatize(t) for t in tokens]
        
        # Step 6: Return cleaned string
        cleaned = ' '.join(tokens)
        return cleaned
        
    except Exception as e:
        logger.error(f"Text cleaning failed: {e}")
        return orig_text.lower()  # Fallback to original text lowercased


class TextPreprocessor:
    """Stateful text preprocessor for batch operations"""
    
    def __init__(self):
        """Initialize preprocessor (lazy NLTK init)"""
        self._initialized = False
    
    def preprocess(self, text: str) -> str:
        """Clean a single text string"""
        if not self._initialized:
            _init_nltk()
            self._initialized = True
        return clean_text(text)
    
    def preprocess_batch(self, texts: List[str]) -> List[str]:
        """Clean multiple texts efficiently"""
        if not self._initialized:
            _init_nltk()
            self._initialized = True
        return [clean_text(t) for t in texts]
    
    def tokenize(self, text: str) -> List[str]:
        """Tokenize text using clean_text preprocessing"""
        # Validate input
        if text is None or not isinstance(text, str) or not text.strip():
            return []
        
        if not self._initialized:
            _init_nltk()
            self._initialized = True
        
        from nltk.tokenize import word_tokenize
        
        # Use clean_text for preprocessing then tokenize
        cleaned = clean_text(text)
        if not cleaned:
            return []
        return word_tokenize(cleaned)
