"""
ML model loading and inference helpers
"""
import os
import joblib
from typing import Dict, Any, List, Optional
import numpy as np

class MLModelManager:
    """Manages loading and inference for ML models"""
    
    def __init__(self):
        self.major_model = None
        self.career_model = None
        self.models_loaded = False
        
    def load_models(self) -> bool:
        """Load ML models from files"""
        try:
            model_dir = "models"
            
            # Load major classifier
            major_model_path = os.path.join(model_dir, "major_classifier.joblib")
            if os.path.exists(major_model_path):
                self.major_model = joblib.load(major_model_path)
                print(f"Major model loaded from {major_model_path}")
            else:
                print(f"Major model not found at {major_model_path}")
                return False
            
            # Load career classifier
            career_model_path = os.path.join(model_dir, "career_classifier.joblib")
            if os.path.exists(career_model_path):
                self.career_model = joblib.load(career_model_path)
                print(f"Career model loaded from {career_model_path}")
            else:
                print(f"Career model not found at {career_model_path}")
                return False
            
            self.models_loaded = True
            return True
            
        except Exception as e:
            print(f"Error loading models: {e}")
            return False
    
    def predict_major(self, features: np.ndarray) -> List[Dict[str, Any]]:
        """Predict major recommendations"""
        if not self.models_loaded or self.major_model is None:
            return []
        
        try:
            # Get probabilities for all classes
            probabilities = self.major_model.predict_proba(features)
            classes = self.major_model.classes_
            
            # Create results with probabilities
            results = []
            for i, (class_name, prob) in enumerate(zip(classes, probabilities[0])):
                if prob > 0.05:  # Only include predictions above 5% confidence
                    results.append({
                        "major": class_name,
                        "probability": float(prob),
                        "score": float(prob * 100)  # Convert to percentage
                    })
            
            # Sort by probability
            results.sort(key=lambda x: x["probability"], reverse=True)
            return results[:5]  # Top 5
            
        except Exception as e:
            print(f"Error in major prediction: {e}")
            return []
    
    def predict_career(self, features: np.ndarray) -> List[Dict[str, Any]]:
        """Predict career recommendations"""
        if not self.models_loaded or self.career_model is None:
            return []
        
        try:
            # Get probabilities for all classes
            probabilities = self.career_model.predict_proba(features)
            classes = self.career_model.classes_
            
            # Create results with probabilities
            results = []
            for i, (class_name, prob) in enumerate(zip(classes, probabilities[0])):
                if prob > 0.02:  # Lower threshold for careers (2% confidence)
                    results.append({
                        "career": class_name,
                        "probability": float(prob),
                        "score": float(prob * 100)  # Convert to percentage
                    })
            
            # Sort by probability
            results.sort(key=lambda x: x["probability"], reverse=True)
            return results[:8]  # Top 8
            
        except Exception as e:
            print(f"Error in career prediction: {e}")
            return []
    
    def is_loaded(self) -> bool:
        """Check if models are loaded"""
        return self.models_loaded

# Global model manager instance
model_manager = MLModelManager()