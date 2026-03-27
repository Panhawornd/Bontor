"""
Random Forest Training Script — Purely Data-Driven from CSV

This version removes synthetic data generation and profile auto-generation.
It relies entirely on students_dataset.csv for training.
"""
import logging
import joblib
import numpy as np
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Any

# Ensure project root is in path
ROOT_DIR = Path(__file__).parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_score,
    recall_score,
)
from sklearn.preprocessing import StandardScaler

from core.feature_builder import FeatureBuilder
from data.grade_loader import get_real_students_augmented

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Paths
MODEL_DIR = Path(__file__).parent / "models"
MODEL_PATH = MODEL_DIR / "random_forest_major.pkl"
FEATURES_PATH = MODEL_DIR / "feature_names.pkl"
SCALER_PATH = MODEL_DIR / "feature_scaler.pkl"
TRAINING_META_PATH = MODEL_DIR / "training_meta.pkl"

class ModelTrainer:
    def __init__(self, majors_db: Dict, n_estimators: int = 1000, max_depth: int = 30):
        self.majors_db = majors_db
        self.majors_list = sorted(list(majors_db.keys()))
        self.scaler = StandardScaler()
        self.model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            min_samples_leaf=4,
            class_weight="balanced",
            random_state=42,
            n_jobs=-1,
        )
        self.fb = FeatureBuilder()

    def load_data(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Load training data ONLY from students_dataset.csv.
        Uses FeatureBuilder to ensure features match inference logic.
        """
        logger.info("Loading training data from students_dataset.csv…")
        # Use n_copies=1 as the dataset is already large (55k)
        real_students = get_real_students_augmented(n_copies=1)
        
        X: List[np.ndarray] = []
        y: List[str] = []
        
        for i, student in enumerate(real_students):
            major = student.get("major")
            if not major or major not in self.majors_db:
                continue
                
            interest = student.get("interest", "")
            grades = student.get("grades", {})
            
            # Map 'interest' from CSV to all text fields as it encodes the student's soul
            features = self.fb.build_features(
                grades=grades,
                interests=interest,
                career_goal=interest,
                strengths=interest,
                preferences=interest
            )
            
            X.append(features)
            y.append(major)
            
            if (i + 1) % 10000 == 0:
                logger.info(f"Processed {i + 1} students…")
                
        logger.info(f"Final training set: {len(X)} samples, {len(set(y))} majors")
        return np.array(X, dtype=np.float32), np.array(y)

    def train(self, tune_hyperparams: bool = True):
        logger.info("Starting training process…")
        X, y = self.load_data()

        if len(X) == 0:
            logger.error("No data found. Aborting.")
            return None, {}

        # Feature Scaling
        self.scaler.fit(X)
        X_scaled = self.scaler.transform(X)

        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42, stratify=y
        )

        best_params = {
            "n_estimators": self.model.n_estimators,
            "max_depth": self.model.max_depth,
            "min_samples_leaf": self.model.min_samples_leaf,
        }
        tuning_cv_accuracy = None

        if tune_hyperparams:
            logger.info("Running hyperparameter tuning (GridSearchCV)…")
            param_grid = {
                "n_estimators": [500, 1000],
                "max_depth": [25, 35],
                "min_samples_leaf": [3, 5],
            }
            tuner = GridSearchCV(
                estimator=RandomForestClassifier(
                    class_weight="balanced",
                    random_state=42,
                    n_jobs=-1,
                ),
                param_grid=param_grid,
                cv=3,
                scoring="accuracy",
                n_jobs=-1,
                refit=True,
            )
            tuner.fit(X_train, y_train)
            self.model = tuner.best_estimator_
            best_params = tuner.best_params_
            tuning_cv_accuracy = float(tuner.best_score_)
            logger.info(f"Best tuning accuracy: {tuning_cv_accuracy:.4f} with {best_params}")
        else:
            self.model.fit(X_train, y_train)

        # Evaluation
        y_pred = self.model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        
        y_train_pred = self.model.predict(X_train)
        train_acc = accuracy_score(y_train, y_train_pred)
        
        precision_weighted = precision_score(y_test, y_pred, average="weighted", zero_division=0)
        recall_weighted = recall_score(y_test, y_pred, average="weighted", zero_division=0)
        precision_macro = precision_score(y_test, y_pred, average="macro", zero_division=0)
        recall_macro = recall_score(y_test, y_pred, average="macro", zero_division=0)
        
        cm = confusion_matrix(y_test, y_pred, labels=self.majors_list)
        class_support = {major: int(np.sum(y_test == major)) for major in self.majors_list}

        logger.info("Running cross-validation…")
        cv_scores = cross_val_score(self.model, X_scaled, y, cv=5, scoring="accuracy", n_jobs=-1)
        
        report_dict = classification_report(y_test, y_pred, output_dict=True)
        
        logger.info(f"Train Accuracy: {train_acc:.4f}")
        logger.info(f"Test Accuracy: {acc:.4f}")
        logger.info(f"CV Accuracy: {cv_scores.mean():.4f}")

        # Save model and meta
        if not MODEL_DIR.exists():
            MODEL_DIR.mkdir(parents=True)

        joblib.dump(self.model, MODEL_PATH)
        joblib.dump(self.scaler, SCALER_PATH)
        
        feature_names = self.fb.get_feature_names()
        joblib.dump(feature_names, FEATURES_PATH)

        tuning_cv_best = tuning_cv_accuracy if tuning_cv_accuracy else 0.0
        
        training_meta = {
            "n_samples": len(y),
            "n_features": X.shape[1],
            "n_classes": len(self.majors_list),
            "classes": self.majors_list,
            "train_accuracy": float(train_acc),
            "test_accuracy": acc,
            "test_precision_weighted": float(precision_weighted),
            "test_recall_weighted": float(recall_weighted),
            "test_precision_macro": float(precision_macro),
            "test_recall_macro": float(recall_macro),
            "cv_accuracy_mean": float(cv_scores.mean()),
            "cv_accuracy_std": float(cv_scores.std()),
            "tuning_enabled": bool(tune_hyperparams),
            "tuning_best_params": best_params,
            "tuning_best_cv_accuracy": tuning_cv_best,
            "feature_names": feature_names,
            "confusion_matrix": cm.tolist(),
            "test_samples_per_class": class_support,
            "test_total_samples": int(len(y_test)),
            "report": report_dict
        }
        joblib.dump(training_meta, TRAINING_META_PATH)

        return self.model, training_meta

def train_random_forest(majors_database: Dict, **kwargs) -> Tuple:
    n_estimators = kwargs.get("n_estimators", 1000)
    max_depth = kwargs.get("max_depth", 30)
    tune_hyperparams = kwargs.get("tune_hyperparams", True)

    trainer = ModelTrainer(
        majors_database,
        n_estimators=n_estimators,
        max_depth=max_depth,
    )
    return trainer.train(tune_hyperparams=tune_hyperparams)
