"""NLP Module - Text preprocessing and embedding generation"""
from .preprocess import clean_text, TextPreprocessor
from .sbert import SBERTEncoder
from .similarity import SimilarityEngine

__all__ = ['clean_text', 'TextPreprocessor', 'SBERTEncoder', 'SimilarityEngine']
