"""
ML Prediction Engine
Random Forest classifier for major recommendations
"""
import joblib
import logging
from pathlib import Path
from typing import List, Dict
import numpy as np

logger = logging.getLogger(__name__)

class MLEngine:
    """Manages ML model loading and prediction"""
    
    def __init__(self, model_dir: str = "models"):
        self.model_dir = Path(model_dir)
        self.model = None
        self.load_model()
    
    def load_model(self):
        """Load trained Random Forest model"""
        model_path = self.model_dir / "major_classifier.pkl"
        
        if model_path.exists():
            try:
                self.model = joblib.load(model_path)
                logger.info("ML model loaded successfully")
            except Exception as e:
                logger.error(f"Failed to load model: {e}")
                self.model = None
        else:
            logger.warning(f"Model not found at {model_path}")
            self.model = None
    
    def predict(self, features: np.ndarray) -> List[Dict[str, any]]:
        """
        Predict major recommendations
        
        Args:
            features: Feature vector from FeatureEngine
            
        Returns:
            List of {major, probability} dicts sorted by probability
        """
        if self.model is None:
            logger.warning("No model available for prediction")
            return []
        
        try:
            # Reshape for single prediction
            X = features.reshape(1, -1)
            logger.info(f"Predicting with feature shape: {X.shape}")
            
            # Get probabilities
            probabilities = self.model.predict_proba(X)[0]
            classes = self.model.classes_
            
            # Build results
            results = []
            for major, prob in zip(classes, probabilities):
                if prob >= 0.0:  # Include all for rule-based boosting 
                    results.append({
                        "major": str(major),
                        "probability": float(prob),
                        "source": "ML-RandomForest"
                    })
            
            # Sort by probability
            results.sort(key=lambda x: x['probability'], reverse=True)
            logger.info(f"Prediction successful, found {len(results)} majors")
            return results
            
        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            return []
