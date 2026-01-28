"""
Random Forest Training Script
Generates "Smart" Synthetic Data and Trains Model
"""
import logging
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, List, Tuple
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
MODEL_DIR = Path(__file__).parent / "models"
MODEL_PATH = MODEL_DIR / "random_forest_major.pkl"
FEATURES_PATH = MODEL_DIR / "feature_names.pkl"

# Standard Subjects & Max Scores
SUBJECTS = ["math", "physics", "chemistry", "biology", "english", "khmer", "history"]
MAX_SCORES = {
    "math": 125, "physics": 75, "chemistry": 75, "biology": 75,
    "english": 50, "khmer": 75, "history": 50
}
STRENGTHS_MAP = {
    "logic": 0, "communication": 1, "creativity": 2, "problem-solving": 3,
    "analytical": 4, "leadership": 5, "teamwork": 6, "technical": 7
}
PREFERENCES_MAP = {
    "coding": 0, "analysis": 1, "design": 2, "networking": 3,
    "research": 4, "teaching": 5, "helping": 6, "building": 7
}

class ModelTrainer:
    def __init__(self, majors_db: Dict):
        self.majors_db = majors_db
        self.majors_list = sorted(list(majors_db.keys()))
        self.model = RandomForestClassifier(
            n_estimators=1000,   # More trees
            max_depth=30,        # Deeper trees
            random_state=42
        )
    
    def generate_smart_data(self, n_samples: int = 50000) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate strict, logic-based synthetic data
        to force the model to learn specific patterns
        """
        X = []
        y = []
        n_per_major = n_samples // len(self.majors_list)
        
        logger.info(f"Generating optimized training data: {n_samples} samples...")
        
        for major_name in self.majors_list:
            major_info = self.majors_db[major_name]
            required_subjects = major_info.get("required_subjects", [])
            desc = major_info.get("description", "").lower()
            
            for _ in range(n_per_major):
                # 1. Subject Scores
                grades = {
                    "math": np.random.uniform(40, 90),
                    "physics": np.random.uniform(30, 60),
                    "chemistry": np.random.uniform(30, 60),
                    "biology": np.random.uniform(30, 60),
                    "english": np.random.uniform(20, 45),
                    "khmer": np.random.uniform(30, 60),
                    "history": np.random.uniform(20, 40)
                }
                
                # FORCE high scores for required subjects
                for sub in required_subjects:
                    sub_key = sub.lower()
                    if sub_key in grades:
                        max_val = MAX_SCORES.get(sub_key, 100)
                        # 80% - 100% score for required subjects
                        grades[sub_key] = np.random.uniform(0.80 * max_val, 1.0 * max_val)

                # --- HARDCODED INTELLIGENCE RULES ---
                # These override random generation to enforce "Common Sense"
                
                if "Software" in major_name or "Computer" in major_name or "Data" in major_name:
                    # CS specific rules
                    grades["math"] = np.random.uniform(100, 125) # Very high math
                    grades["physics"] = np.random.uniform(50, 75)
                
                elif "Medicine" in major_name or "Pharmacy" in major_name:
                    # Med specific rules
                    grades["biology"] = np.random.uniform(60, 75)
                    grades["chemistry"] = np.random.uniform(60, 75)
                    grades["math"] = np.random.uniform(80, 110) # Decent math
                
                elif "Architecture" in major_name or "Design" in major_name:
                    grades["math"] = np.random.uniform(90, 125)
                    grades["physics"] = np.random.uniform(50, 75)
                    # Art skills implicit in strengths
                    
                # Normalize (0-1)
                grade_features = [
                    grades["math"] / 125,
                    grades["physics"] / 75,
                    grades["chemistry"] / 75,
                    grades["biology"] / 75,
                    grades["english"] / 50,
                    grades["khmer"] / 75,
                    grades["history"] / 50
                ]
                
                # 2. Grade Stats
                vals = list(grades.values())
                grade_stats = [
                    np.mean(vals) / 100, 
                    np.std(vals) / 50, 
                    np.max(vals) / 125
                ]
                
                # 3. Strengths & Preferences
                strength_vec = np.zeros(8)
                pref_vec = np.zeros(8)
                
                # Add noise but keep signal strong
                if np.random.random() > 0.1:
                    if "logic" in desc or "math" in desc: strength_vec[0] = 1
                    if "creat" in desc or "design" in desc: strength_vec[2] = 1
                    if "analy" in desc: strength_vec[4] = 1 # analytical
                    
                    if "code" in desc or "soft" in desc: pref_vec[0] = 1 # coding
                    if "help" in desc: pref_vec[6] = 1 # helping
                    if "tech" in desc: strength_vec[7] = 1 # technical
                
                # 4. SBERT Similarity (CRITICAL FEATURE)
                # Force very high similarity for target major
                sim_scores = []
                for m in self.majors_list:
                    if m == major_name:
                        sim_scores.append(np.random.uniform(0.7, 0.99))
                    else:
                        sim_scores.append(np.random.uniform(0.0, 0.2))
                
                # 5. Eligibility (Assume 1.0)
                elig_flags = np.ones(len(self.majors_list))
                
                # Combine
                features = np.concatenate([
                    grade_features,
                    grade_stats,
                    strength_vec,
                    pref_vec,
                    np.array(sim_scores),
                    elig_flags
                ])
                
                X.append(features)
                y.append(major_name)
        
        return np.array(X), np.array(y)

    def train(self):
        logger.info("Starting training process...")
        X, y = self.generate_smart_data()
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        self.model.fit(X_train, y_train)
        
        y_pred = self.model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        
        logger.info(f"Model Accuracy: {acc:.4f}")
        
        # Save
        if not MODEL_DIR.exists():
            MODEL_DIR.mkdir(parents=True)
            
        joblib.dump(self.model, MODEL_PATH)
        
        # Save feature names
        feature_names = (
            [f"grade_{s}" for s in SUBJECTS] +
            ["grade_mean", "grade_std", "grade_max"] +
            [f"strength_{i}" for i in range(8)] +
            [f"pref_{i}" for i in range(8)] +
            [f"sim_{m}" for m in self.majors_list] +
            [f"elig_{m}" for m in self.majors_list]
        )
        joblib.dump(feature_names, FEATURES_PATH)
        logger.info(f"Model saved to {MODEL_PATH}")
        
        return self.model, {"test_accuracy": acc, "n_features": X.shape[1], "n_classes": len(self.majors_list)}

def train_random_forest(majors_database, **kwargs):
    """Entry point wrapper"""
    trainer = ModelTrainer(majors_database)
    return trainer.train()
