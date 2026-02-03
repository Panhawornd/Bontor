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


def clean_text(text: str, return_tokens: bool = False) -> str | List[str]:
    """
    Clean text using NLTK preprocessing pipeline:
    1. Lowercase
    2. Tokenize
    3. Remove stopwords
    4. Lemmatize
    5. Return cleaned string or token list
    
    Args:
        text: Raw input text
        return_tokens: If True, return list of tokens instead of joined string
        
    Returns:
        Cleaned, preprocessed text string or list of tokens
    """
    if not text or not text.strip():
        return [] if return_tokens else ""
    
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
        
        # Step 6: Return tokens or cleaned string
        if return_tokens:
            return tokens
        return ' '.join(tokens)
        
    except Exception as e:
        logger.error(f"Text cleaning failed: {e}")
        # Fallback: run minimal safe preprocessing pipeline
        try:
            # Minimal pipeline: lowercase, clean special chars, tokenize, filter
            fallback_text = orig_text.lower()
            fallback_text = re.sub(r'[^a-zA-Z\s]', ' ', fallback_text)
            fallback_tokens = fallback_text.split()  # Simple split instead of word_tokenize
            # Filter stopwords and single chars (if _stopwords available)
            if _stopwords is not None:
                fallback_tokens = [t for t in fallback_tokens if t not in _stopwords and len(t) > 1]
            # Lemmatize if available
            if _lemmatizer is not None:
                fallback_tokens = [_lemmatizer.lemmatize(t) for t in fallback_tokens]
            # Return based on return_tokens flag
            if return_tokens:
                return fallback_tokens
            return ' '.join(fallback_tokens)
        except Exception as fallback_e:
            logger.error(f"Fallback preprocessing also failed: {fallback_e}")
            # Ultimate fallback: just lowercase and split
            if return_tokens:
                return orig_text.lower().split()
            return orig_text.lower()
