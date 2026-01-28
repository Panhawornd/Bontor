"""ML Module - Random Forest training and prediction"""
from .train_rf import train_random_forest
from .predict import MLPredictor

__all__ = ['train_random_forest', 'MLPredictor']
