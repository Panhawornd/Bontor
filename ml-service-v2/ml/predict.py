"""
ML Prediction Module
Uses trained Random Forest for major prediction

Input: Numeric feature vector only
Output: Probability per major, ranked list
"""
import logging
import threading
import numpy as np
from pathlib import Path
from typing import List, Dict, Optional
import joblib

logger = logging.getLogger(__name__)

# Model paths
MODEL_DIR = Path(__file__).parent / "models"
MODEL_PATH = MODEL_DIR / "random_forest_major.pkl"
FEATURES_PATH = MODEL_DIR / "feature_names.pkl"


class MLPredictor:
    """
    ML Prediction engine using Random Forest
    
    Input: Feature vector (numbers only)
    Output:
        - Probability per major
        - Ranked major list
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                # Double-check pattern
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self.model = None
        self.feature_names = None
        self._load_model()
        self._initialized = True
    
    def _load_model(self):
        """Load trained Random Forest model"""
        # First try the new model path
        if MODEL_PATH.exists():
            try:
                self.model = joblib.load(MODEL_PATH)
                logger.info(f"Loaded Random Forest from {MODEL_PATH}")
                
                if FEATURES_PATH.exists():
                    self.feature_names = joblib.load(FEATURES_PATH)
                    
            except Exception as e:
                logger.error(f"Failed to load new model: {e}")
        
        # Fallback to legacy model path
        if self.model is None:
            legacy_path = Path(__file__).parent.parent / "models" / "major_classifier.pkl"
            if legacy_path.exists():
                try:
                    self.model = joblib.load(legacy_path)
                    logger.info(f"Loaded legacy model from {legacy_path}")
                except Exception as e:
                    logger.error(f"Failed to load legacy model: {e}")
        
        if self.model is None:
            logger.warning("No trained model available - predictions will fail")
    
    def predict(self, features: np.ndarray, strict: bool = False) -> List[Dict]:
        """
        Predict major recommendations from feature vector
        
        Args:
            features: Numeric feature vector (from FeatureBuilder)
            strict: If True, raise ValueError on feature dimension mismatch.
                   If False, auto-pad/truncate and include warning in results.
            
        Returns:
            List of {major, probability, source, warning?} dicts sorted by probability
        """
        if self.model is None:
            logger.error("No model loaded - cannot predict")
            return []
        
        try:
            # Reshape for single prediction
            X = features.reshape(1, -1)
            warning_msg = None
            
            # Handle feature dimension mismatch
            expected_features = self.model.n_features_in_
            if X.shape[1] != expected_features:
                mismatch_msg = f"Feature mismatch: got {X.shape[1]}, expected {expected_features}"
                
                if strict:
                    raise ValueError(mismatch_msg)
                
                logger.warning(mismatch_msg)
                warning_msg = f"feature mismatch: {'padded' if X.shape[1] < expected_features else 'truncated'}"
                
                if X.shape[1] < expected_features:
                    # Pad with zeros
                    padding = np.zeros((1, expected_features - X.shape[1]))
                    X = np.hstack([X, padding])
                else:
                    # Truncate
                    X = X[:, :expected_features]
            
            # Get probabilities
            probabilities = self.model.predict_proba(X)[0]
            classes = self.model.classes_
            
            # Build results
            results = []
            for major, prob in zip(classes, probabilities):
                result = {
                    "major": str(major),
                    "probability": float(prob),
                    "source": "ML-RandomForest"
                }
                if warning_msg:
                    result["warning"] = warning_msg
                results.append(result)
            
            # Sort by probability descending
            results.sort(key=lambda x: x["probability"], reverse=True)
            
            logger.debug(f"Prediction complete: {len(results)} majors ranked")
            return results
            
        except ValueError:
            # Re-raise ValueError (e.g., from strict mode) without suppression
            raise
        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            return []
    
    def predict_with_threshold(
        self,
        features: np.ndarray,
        min_probability: float = 0.01
    ) -> List[Dict]:
        """
        Predict and filter by minimum probability
        
        Args:
            features: Feature vector
            min_probability: Minimum probability to include
            
        Returns:
            Filtered list of recommendations
        """
        all_predictions = self.predict(features)
        return [p for p in all_predictions if p["probability"] >= min_probability]
    
    def get_top_n(self, features: np.ndarray, n: int = 5) -> List[Dict]:
        """
        Get top N major recommendations
        
        Args:
            features: Feature vector
            n: Number of top results
            
        Returns:
            Top N recommendations
        """
        all_predictions = self.predict(features)
        return all_predictions[:n]
    
    def is_ready(self) -> bool:
        """Check if model is loaded and ready"""
        return self.model is not None

