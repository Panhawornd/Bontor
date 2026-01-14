"""
Robust training script for ML Service v2
- Handles missing subjects (sets to 0)
- Improved feature weighting
- Better generalization
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
from pathlib import Path
from data.majors import MAJOR_DATABASE

# Standard list of majors
majors = sorted(list(MAJOR_DATABASE.keys()))
num_majors = len(majors)
subjects = ["math", "physics", "chemistry", "biology", "english", "khmer", "history"]
max_scores = {"math": 125, "physics": 75, "chemistry": 75, "biology": 75,
             "english": 50, "khmer": 75, "history": 50}

def generate_training_data(n_samples=5000):
    """Generate synthetic training data matching FeatureEngine output"""
    data = []
    
    for _ in range(n_samples):
        # Random major
        major = np.random.choice(majors)
        major_info = MAJOR_DATABASE[major]
        required = major_info.get("required_subjects", [])
        
        # 1. Generate realistic grades
        grades = {}
        for sub in subjects:
            # Check if this is a "primary" subject for this major
            is_required = sub in required
            
            if is_required:
                # Higher score for required subjects
                score = np.random.normal(0.85 * max_scores[sub], 0.1 * max_scores[sub])
            else:
                # Random average score
                score = np.random.normal(0.65 * max_scores[sub], 0.15 * max_scores[sub])
            
            grades[sub] = np.clip(score, 0, max_scores[sub])
            
            # Randomly drop some non-required subjects
            if not is_required and np.random.random() < 0.3:
                grades[sub] = 0.0

        # 2. Normalize features like FeatureEngine
        grade_features = [grades[s] / max_scores[s] for s in subjects]
        
        grade_values = [v for v in grades.values() if v > 0]
        grade_stats = [
            np.mean(grade_values) if grade_values else 0,
            np.std(grade_values) if grade_values else 0,
            max(grade_values) if grade_values else 0,
        ]
        
        # 3. Simulate NLP scores
        nlp_features = np.random.uniform(0.01, 0.03, len(majors)) # Very low noise
        try:
            major_idx = majors.index(major)
            nlp_features[major_idx] = np.random.uniform(0.50, 0.90) # Very strong signal
            
            # Similar majors noise
            if "Engineering" in major or major in ["Medicine", "Pharmacy", "Dentistry"]:
                for idx, m in enumerate(majors):
                    if (("Engineering" in m and "Engineering" in major) or 
                        (m in ["Medicine", "Pharmacy", "Dentistry"] and major in ["Medicine", "Pharmacy", "Dentistry"])) and idx != major_idx:
                        nlp_features[idx] = np.random.uniform(0.05, 0.15)
        except:
            pass
            
        features = grade_features + grade_stats + list(nlp_features)
        
        data.append({
            'features': features,
            'major': major
        })
    
    return pd.DataFrame(data)

def train_model():
    """Train the major classifier"""
    print("Generating robust training data...")
    df = generate_training_data(20000) # Significantly more data for high-precision
    
    # Prepare data
    X = np.array(df['features'].tolist())
    y = df['major'].values
    
    print(f"Training with {len(X)} samples, {X.shape[1]} features")
    
    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42, stratify=y)
    
    # Train model (using more trees for high-class count)
    print("\nTraining Deep Random Forest...")
    model = RandomForestClassifier(
        n_estimators=1000,
        max_depth=20,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)
    
    # Evaluate
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    
    print(f"\nTraining accuracy: {train_score:.2%}")
    print(f"Test accuracy: {test_score:.2%}")
    
    # Save model
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    
    model_path = models_dir / "major_classifier.pkl"
    joblib.dump(model, model_path)
    print(f"\n✓ Model saved to {model_path}")
    
    return model

if __name__ == "__main__":
    train_model()
