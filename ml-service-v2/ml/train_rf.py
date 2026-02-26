"""
Random Forest Training Script — Database-Driven Profile Generation

KEY CHANGE: Instead of 21 hardcoded PER_MAJOR_PROFILES with manually
assigned mean/std values, profiles are AUTO-GENERATED from MAJOR_DATABASE.

How it works:
1. For each major, look at its required_subjects
   → Required subjects get higher grade distributions
   → Non-required subjects get average distributions
2. For each major, look at its keywords and fundamental_skills
   → Use SBERT to determine which strengths/preferences are relevant
3. Generate synthetic training data from these derived profiles
4. Train the same Random Forest model

The model learns from data that reflects the DATABASE structure,
not from developer assumptions.
"""
import logging
import joblib
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Paths
MODEL_DIR = Path(__file__).parent / "models"
MODEL_PATH = MODEL_DIR / "random_forest_major.pkl"
FEATURES_PATH = MODEL_DIR / "feature_names.pkl"
SCALER_PATH = MODEL_DIR / "feature_scaler.pkl"
TRAINING_META_PATH = MODEL_DIR / "training_meta.pkl"

# Standard subjects & max scores (real Cambodian exam values)
SUBJECTS = ["math", "physics", "chemistry", "biology", "english", "khmer", "history"]
MAX_SCORES = {
    "math": 125, "physics": 75, "chemistry": 75, "biology": 75,
    "english": 50, "khmer": 75, "history": 50,
}

STEM_SUBJECTS = ["math", "physics", "chemistry", "biology"]
LANG_SUBJECTS = ["english", "khmer"]

# Strength/Preference concept descriptions (same as feature_builder)
STRENGTH_CONCEPTS = {
    "logic": "logical thinking, reasoning, deduction, analytical mind",
    "communication": "communication skills, speaking, presenting, explaining clearly",
    "creativity": "creative thinking, artistic, innovative ideas, imagination",
    "problem-solving": "solving problems, debugging, troubleshooting, figuring things out",
    "analytical": "data analysis, examining patterns, statistical thinking, research",
    "leadership": "leading teams, managing people, delegation, mentoring, guiding others",
    "teamwork": "working in teams, collaboration, group projects, cooperating with others",
    "technical": "technical skills, hands-on work, building things, using tools and technology",
}

PREFERENCE_CONCEPTS = {
    "coding": "writing code, programming, software development, building apps",
    "analysis": "analyzing data, research, examining information, understanding patterns",
    "design": "designing interfaces, visual design, creative layouts, user experience",
    "networking": "connecting with people, business networking, building relationships",
    "research": "conducting research, scientific investigation, academic study",
    "teaching": "teaching others, explaining concepts, education, mentoring students",
    "helping": "helping people, caring for others, community service, making a difference",
    "building": "building structures, construction, creating physical things, engineering",
}


def _cosine(a: np.ndarray, b: np.ndarray) -> float:
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    if na == 0 or nb == 0:
        return 0.0
    return float(np.dot(a, b) / (na * nb))


class ProfileGenerator:
    """
    Auto-generates training profiles from MAJOR_DATABASE.

    For each major:
    - Subject distributions derived from required_subjects
    - Strength/preference probabilities derived via SBERT similarity
      between the major's description+keywords and each concept
    """

    def __init__(self, majors_db: Dict):
        self.majors_db = majors_db
        self._sbert = None
        self._profiles: Dict[str, Dict] = {}

    def _get_sbert(self):
        if self._sbert is None:
            from nlp.sbert import SBERTEncoder
            self._sbert = SBERTEncoder()
        return self._sbert

    def generate_profiles(self) -> Dict[str, Dict]:
        """Generate a profile for every major from the database."""
        if self._profiles:
            return self._profiles

        logger.info("Auto-generating training profiles from database…")
        enc = self._get_sbert()

        for major_name, info in self.majors_db.items():
            required = [s.lower() for s in info.get("required_subjects", [])]
            desc = info.get("description", "")
            keywords = " ".join(info.get("keywords", []))
            skills_text = " ".join(info.get("fundamental_skills", {}).keys())
            major_text = f"{desc} {keywords} {skills_text}"

            # --- Subject distributions ---
            subjects = {}
            for s in SUBJECTS:
                if s in required:
                    # Required → high mean, tight std
                    subjects[s] = (0.78, 0.08)
                else:
                    # Not required → average mean, wider std
                    subjects[s] = (0.48, 0.14)

            # --- Strength probabilities via SBERT ---
            major_emb = enc.encode(major_text)
            strengths = {}
            for sname, sdesc in STRENGTH_CONCEPTS.items():
                s_emb = enc.encode(sdesc)
                sim = _cosine(major_emb, s_emb)
                # Convert similarity to probability (0.1 - 0.95)
                prob = max(0.10, min(0.95, sim * 1.5))
                strengths[sname] = prob

            # --- Preference probabilities via SBERT ---
            preferences = {}
            for pname, pdesc in PREFERENCE_CONCEPTS.items():
                p_emb = enc.encode(pdesc)
                sim = _cosine(major_emb, p_emb)
                prob = max(0.05, min(0.95, sim * 1.5))
                preferences[pname] = prob

            self._profiles[major_name] = {
                "subjects": subjects,
                "strengths": strengths,
                "preferences": preferences,
            }

        logger.info(f"Generated {len(self._profiles)} profiles from database")
        return self._profiles


class ModelTrainer:
    def __init__(self, majors_db: Dict, n_estimators: int = 1000, max_depth: int = 30):
        self.majors_db = majors_db
        self.majors_list = sorted(list(majors_db.keys()))
        self.scaler = StandardScaler()
        self.model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            min_samples_leaf=3,
            class_weight="balanced",
            random_state=42,
            n_jobs=-1,
        )
        self.profile_gen = ProfileGenerator(majors_db)

    def generate_smart_data(self, n_samples: int = 50000) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate training data from auto-generated profiles.
        Same feature layout as FeatureBuilder, but profiles are
        derived from the database instead of hardcoded.
        """
        profiles = self.profile_gen.generate_profiles()
        X: List[np.ndarray] = []
        y: List[str] = []
        n_per_major = n_samples // len(self.majors_list)

        logger.info(
            f"Generating training data: {n_samples} samples "
            f"({n_per_major}/major) from {len(profiles)} profiles…"
        )

        for major_name in self.majors_list:
            profile = profiles.get(major_name)
            if profile is None:
                logger.warning(f"No profile for {major_name}, using defaults")
                profile = {
                    "subjects": {s: (0.50, 0.15) for s in SUBJECTS},
                    "strengths": {s: 0.35 for s in STRENGTH_CONCEPTS},
                    "preferences": {p: 0.35 for p in PREFERENCE_CONCEPTS},
                }

            major_info = self.majors_db[major_name]
            required_subjects = [s.lower() for s in major_info.get("required_subjects", [])]

            for _ in range(n_per_major):
                # 1. Subject scores from Gaussian distributions
                grades: Dict[str, float] = {}
                for subject in SUBJECTS:
                    mean, std = profile["subjects"].get(subject, (0.50, 0.15))
                    jittered = mean + np.random.uniform(-0.05, 0.05)
                    normalised = np.clip(np.random.normal(jittered, std), 0.05, 1.0)
                    grades[subject] = normalised * MAX_SCORES[subject]

                # Soft boost for required subjects
                for sub in required_subjects:
                    if sub in grades:
                        boost = np.random.uniform(0.0, 0.15) * MAX_SCORES[sub]
                        grades[sub] = min(grades[sub] + boost, MAX_SCORES[sub])

                # Normalise to 0-1
                grade_features = [grades[s] / MAX_SCORES[s] for s in SUBJECTS]

                # 2. Grade statistics
                non_zero = [g for g in grade_features if g > 0]
                grade_stats = (
                    [float(np.mean(non_zero)), float(np.std(non_zero)), float(max(non_zero))]
                    if non_zero
                    else [0.0, 0.0, 0.0]
                )

                # 2b. Interaction features
                stem_avg = float(np.mean([grade_features[SUBJECTS.index(s)] for s in STEM_SUBJECTS]))
                lang_avg = float(np.mean([grade_features[SUBJECTS.index(s)] for s in LANG_SUBJECTS]))
                stem_lang_ratio = stem_avg / (lang_avg + 1e-6)
                math_phys = grade_features[0] * grade_features[1]
                chem_bio = grade_features[2] * grade_features[3]
                interaction_features = [stem_avg, lang_avg, stem_lang_ratio, math_phys, chem_bio]

                # 3. Strengths (Bernoulli from SBERT-derived probabilities)
                strength_vec = np.zeros(len(STRENGTH_CONCEPTS))
                for i, (sname, _) in enumerate(STRENGTH_CONCEPTS.items()):
                    prob = profile["strengths"].get(sname, 0.35)
                    prob = np.clip(prob + np.random.uniform(-0.10, 0.10), 0.0, 1.0)
                    strength_vec[i] = float(np.random.random() < prob) * np.random.uniform(0.4, 1.0)

                # 4. Preferences (Bernoulli from SBERT-derived probabilities)
                pref_vec = np.zeros(len(PREFERENCE_CONCEPTS))
                for i, (pname, _) in enumerate(PREFERENCE_CONCEPTS.items()):
                    prob = profile["preferences"].get(pname, 0.35)
                    prob = np.clip(prob + np.random.uniform(-0.10, 0.10), 0.0, 1.0)
                    pref_vec[i] = float(np.random.random() < prob) * np.random.uniform(0.4, 1.0)

                # 5. SBERT similarity (overlapping Gaussians)
                sim_scores: List[float] = []
                for m in self.majors_list:
                    if m == major_name:
                        s = np.clip(np.random.normal(0.62, 0.12), 0.0, 1.0)
                    else:
                        s = np.clip(np.random.normal(0.32, 0.12), 0.0, 1.0)
                    sim_scores.append(s)

                # 6. Eligibility (data-driven from required subjects)
                elig_flags: List[float] = []
                for m in self.majors_list:
                    m_info = self.majors_db.get(m, {})
                    m_req = [r.lower() for r in m_info.get("required_subjects", [])]
                    if not m_req:
                        elig_flags.append(1.0)
                        continue
                    req_scores = [grades.get(r, 0) / MAX_SCORES.get(r, 100) for r in m_req]
                    avg_req = np.mean(req_scores)
                    # Sigmoid eligibility (matching rules/eligibility.py)
                    k = 8
                    elig = float(1.0 / (1.0 + np.exp(-k * (avg_req - 0.5))))
                    elig = np.clip(elig + np.random.normal(0, 0.05), 0.0, 1.0)
                    elig_flags.append(elig)

                # Combine
                features = np.concatenate([
                    grade_features,
                    grade_stats,
                    interaction_features,
                    strength_vec,
                    pref_vec,
                    np.array(sim_scores),
                    elig_flags,
                ])
                X.append(features)
                y.append(major_name)

        return np.array(X, dtype=np.float32), np.array(y)

    def train(self, n_samples: int = 50000):
        logger.info("Starting training…")
        X, y = self.generate_smart_data(n_samples)

        # Feature Scaling
        self.scaler.fit(X)
        X_scaled = self.scaler.transform(X)

        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42, stratify=y
        )

        self.model.fit(X_train, y_train)

        y_pred = self.model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)

        logger.info("Running 5-fold cross-validation…")
        cv_scores = cross_val_score(
            self.model, X_scaled, y, cv=5, scoring="accuracy", n_jobs=-1
        )
        logger.info(f"CV Accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")

        report_dict = classification_report(y_test, y_pred, output_dict=True)
        logger.info(f"Classification Report:\n{classification_report(y_test, y_pred)}")
        logger.info(f"Test Accuracy: {acc:.4f}")

        # Save
        if not MODEL_DIR.exists():
            MODEL_DIR.mkdir(parents=True)

        joblib.dump(self.model, MODEL_PATH)
        joblib.dump(self.scaler, SCALER_PATH)

        feature_names = (
            [f"grade_{s}" for s in SUBJECTS]
            + ["grade_mean", "grade_std", "grade_max"]
            + ["stem_avg", "lang_avg", "stem_lang_ratio",
               "math_phys_interaction", "chem_bio_interaction"]
            + [f"strength_{s}" for s in STRENGTH_CONCEPTS.keys()]
            + [f"pref_{s}" for s in PREFERENCE_CONCEPTS.keys()]
            + [f"sim_{m}" for m in self.majors_list]
            + [f"elig_{m}" for m in self.majors_list]
        )
        joblib.dump(feature_names, FEATURES_PATH)

        training_meta = {
            "n_samples": len(y),
            "n_features": X.shape[1],
            "n_classes": len(self.majors_list),
            "classes": self.majors_list,
            "test_accuracy": acc,
            "cv_accuracy_mean": float(cv_scores.mean()),
            "cv_accuracy_std": float(cv_scores.std()),
            "feature_names": feature_names,
        }
        joblib.dump(training_meta, TRAINING_META_PATH)

        logger.info(f"Model saved to {MODEL_PATH}")
        logger.info(f"Scaler saved to {SCALER_PATH}")
        logger.info(f"Training metadata saved to {TRAINING_META_PATH}")

        return self.model, {
            "test_accuracy": acc,
            "cv_accuracy_mean": float(cv_scores.mean()),
            "cv_accuracy_std": float(cv_scores.std()),
            "n_features": X.shape[1],
            "n_classes": len(self.majors_list),
            "per_class_metrics": {
                k: v for k, v in report_dict.items() if isinstance(v, dict)
            },
        }


def train_random_forest(majors_database: Dict, **kwargs) -> Tuple:
    n_estimators = kwargs.get("n_estimators", 1000)
    max_depth = kwargs.get("max_depth", 30)
    n_samples = kwargs.get("n_samples", 50000)

    trainer = ModelTrainer(
        majors_database,
        n_estimators=n_estimators,
        max_depth=max_depth,
    )
    return trainer.train(n_samples=n_samples)
