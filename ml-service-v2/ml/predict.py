"""
ML Prediction Module
Uses trained Random Forest for major prediction

Input: Numeric feature vector only
Output: Probability per major, ranked list

Includes:
- PredictionMonitor for tracking confidence & metrics
- Confidence threshold filtering
- Feature scaling via saved StandardScaler
"""
import logging
import threading
import time
import numpy as np
from collections import defaultdict
from pathlib import Path
from typing import List, Dict, Optional
import joblib

logger = logging.getLogger(__name__)

# Model paths
MODEL_DIR = Path(__file__).parent / "models"
MODEL_PATH = MODEL_DIR / "random_forest_major.pkl"
FEATURES_PATH = MODEL_DIR / "feature_names.pkl"
SCALER_PATH = MODEL_DIR / "feature_scaler.pkl"
TRAINING_META_PATH = MODEL_DIR / "training_meta.pkl"

# Confidence thresholds
LOW_CONFIDENCE_THRESHOLD = 0.05   # Predictions below this are flagged
MIN_CONFIDENCE_THRESHOLD = 0.01   # Predictions below this are discarded


class PredictionMonitor:
    """
    Tracks prediction metrics for model monitoring.

    Metrics tracked:
    - Total prediction count
    - Low-confidence prediction count & ratio
    - Per-major prediction frequency
    - Average confidence distribution
    - Prediction latency
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialised = False
        return cls._instance

    def __init__(self):
        if self._initialised:
            return
        self.total_predictions = 0
        self.low_confidence_count = 0
        self.major_counts: Dict[str, int] = defaultdict(int)
        self.confidence_sum: Dict[str, float] = defaultdict(float)
        self.latency_samples: List[float] = []
        self._initialised = True

    def record(self, predictions: List[Dict], latency_ms: float):
        """Record a single prediction request's metrics."""
        self.total_predictions += 1
        self.latency_samples.append(latency_ms)
        # Keep only last 1000 latency samples
        if len(self.latency_samples) > 1000:
            self.latency_samples = self.latency_samples[-1000:]

        top = predictions[0] if predictions else None
        if top:
            self.major_counts[top["major"]] += 1
            self.confidence_sum[top["major"]] += top["probability"]

            if top["probability"] < LOW_CONFIDENCE_THRESHOLD:
                self.low_confidence_count += 1
                logger.warning(
                    f"Low-confidence prediction: {top['major']} "
                    f"({top['probability']:.4f})"
                )

    def get_metrics(self) -> Dict:
        """Return current monitoring metrics snapshot."""
        avg_latency = (
            sum(self.latency_samples) / len(self.latency_samples)
            if self.latency_samples else 0.0
        )
        low_ratio = (
            self.low_confidence_count / self.total_predictions
            if self.total_predictions > 0 else 0.0
        )
        avg_confidence = {}
        for major, total_conf in self.confidence_sum.items():
            count = self.major_counts.get(major, 1)
            avg_confidence[major] = round(total_conf / count, 4)

        return {
            "total_predictions": self.total_predictions,
            "low_confidence_count": self.low_confidence_count,
            "low_confidence_ratio": round(low_ratio, 4),
            "avg_latency_ms": round(avg_latency, 2),
            "top_major_frequency": dict(self.major_counts),
            "avg_confidence_by_major": avg_confidence,
        }


class MLPredictor:
    """
    ML Prediction engine using Random Forest

    Input: Feature vector (numbers only)
    Output:
        - Probability per major
        - Ranked major list
        - Confidence metadata

    Includes StandardScaler transform and PredictionMonitor integration.
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
        self.scaler = None
        self.training_meta = None
        self.monitor = PredictionMonitor()
        self._load_model()
        self._initialized = True
    
    def _load_model(self):
        """Load trained Random Forest model, scaler, and metadata."""
        # First try the new model path
        if MODEL_PATH.exists():
            try:
                self.model = joblib.load(MODEL_PATH)
                logger.info(f"Loaded Random Forest from {MODEL_PATH}")
                
                if FEATURES_PATH.exists():
                    self.feature_names = joblib.load(FEATURES_PATH)

                # Load StandardScaler (Feature Scaling improvement)
                if SCALER_PATH.exists():
                    self.scaler = joblib.load(SCALER_PATH)
                    logger.info(f"Loaded feature scaler from {SCALER_PATH}")
                else:
                    logger.warning("No feature scaler found – predictions will use unscaled features")

                # Load training metadata (Model Monitoring improvement)
                if TRAINING_META_PATH.exists():
                    self.training_meta = joblib.load(TRAINING_META_PATH)
                    logger.info(
                        f"Training meta: accuracy={self.training_meta.get('test_accuracy', '?')}, "
                        f"cv={self.training_meta.get('cv_accuracy_mean', '?')}"
                    )
                    
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
            List of {major, probability, source, confidence_level, warning?}
            dicts sorted by probability
        """
        if self.model is None:
            logger.error("No model loaded - cannot predict")
            return []
        
        t_start = time.perf_counter()
        
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

            # Apply feature scaling if scaler is available
            if self.scaler is not None:
                try:
                    X = self.scaler.transform(X)
                except Exception as e:
                    logger.warning(f"Scaler transform failed, using unscaled: {e}")
            
            # Get probabilities
            probabilities = self.model.predict_proba(X)[0]
            classes = self.model.classes_
            
            # Build results with confidence metadata
            results = []
            for major, prob in zip(classes, probabilities):
                # Determine confidence level
                if prob >= 0.15:
                    confidence_level = "high"
                elif prob >= LOW_CONFIDENCE_THRESHOLD:
                    confidence_level = "medium"
                elif prob >= MIN_CONFIDENCE_THRESHOLD:
                    confidence_level = "low"
                else:
                    confidence_level = "very_low"

                # Skip very low confidence predictions
                if prob < MIN_CONFIDENCE_THRESHOLD:
                    continue

                result = {
                    "major": str(major),
                    "probability": float(prob),
                    "source": "ML-RandomForest",
                    "confidence_level": confidence_level,
                }
                if warning_msg:
                    result["warning"] = warning_msg
                results.append(result)
            
            # Sort by probability descending
            results.sort(key=lambda x: x["probability"], reverse=True)

            # Record metrics
            latency_ms = (time.perf_counter() - t_start) * 1000
            self.monitor.record(results, latency_ms)
            
            logger.debug(
                f"Prediction complete: {len(results)} majors ranked "
                f"(top: {results[0]['major'] if results else 'none'} "
                f"@ {(results[0]['probability'] if results else 0):.4f}, "
                f"{latency_ms:.1f}ms)"
            )
            return results
            
        except ValueError:
            # Re-raise ValueError (e.g., from strict mode) without suppression
            raise
        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            return []

    def get_monitor_metrics(self) -> Dict:
        """Return current prediction monitoring metrics."""
        return self.monitor.get_metrics()

