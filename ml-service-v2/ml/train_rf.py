"""
Random Forest Training Script
Generates Smart Synthetic Data with Per-Major Profiles and Trains Model
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

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
MODEL_DIR = Path(__file__).parent / "models"
MODEL_PATH = MODEL_DIR / "random_forest_major.pkl"
FEATURES_PATH = MODEL_DIR / "feature_names.pkl"
SCALER_PATH = MODEL_DIR / "feature_scaler.pkl"
TRAINING_META_PATH = MODEL_DIR / "training_meta.pkl"

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

# ---------------------------------------------------------------------------
# Per-Major Profiles — each major has its OWN unique distributions
# so the model can distinguish within-category majors
# (e.g., Civil vs Mechanical vs Electrical Engineering)
# ---------------------------------------------------------------------------
PER_MAJOR_PROFILES = {
    # ── CS / Tech ───────────────────────────────────────────────
    "Software Engineering": {
        "subjects": {
            "math": (0.86, 0.07), "physics": (0.58, 0.12),
            "chemistry": (0.40, 0.14), "biology": (0.38, 0.14),
            "english": (0.72, 0.10), "khmer": (0.52, 0.14),
            "history": (0.45, 0.14),
        },
        "strengths": {
            "logic": 0.90, "communication": 0.30, "creativity": 0.50,
            "problem-solving": 0.88, "analytical": 0.80, "leadership": 0.18,
            "teamwork": 0.45, "technical": 0.95,
        },
        "preferences": {
            "coding": 0.95, "analysis": 0.60, "design": 0.30, "networking": 0.25,
            "research": 0.40, "teaching": 0.08, "helping": 0.08, "building": 0.35,
        },
    },
    "Data Science": {
        "subjects": {
            "math": (0.88, 0.06), "physics": (0.55, 0.13),
            "chemistry": (0.42, 0.14), "biology": (0.44, 0.14),
            "english": (0.70, 0.10), "khmer": (0.50, 0.14),
            "history": (0.48, 0.14),
        },
        "strengths": {
            "logic": 0.88, "communication": 0.35, "creativity": 0.40,
            "problem-solving": 0.85, "analytical": 0.92, "leadership": 0.15,
            "teamwork": 0.35, "technical": 0.85,
        },
        "preferences": {
            "coding": 0.85, "analysis": 0.92, "design": 0.15, "networking": 0.20,
            "research": 0.75, "teaching": 0.10, "helping": 0.10, "building": 0.15,
        },
    },
    "Cybersecurity": {
        "subjects": {
            "math": (0.80, 0.08), "physics": (0.62, 0.12),
            "chemistry": (0.42, 0.14), "biology": (0.38, 0.14),
            "english": (0.68, 0.11), "khmer": (0.50, 0.14),
            "history": (0.48, 0.14),
        },
        "strengths": {
            "logic": 0.88, "communication": 0.25, "creativity": 0.55,
            "problem-solving": 0.90, "analytical": 0.82, "leadership": 0.15,
            "teamwork": 0.30, "technical": 0.92,
        },
        "preferences": {
            "coding": 0.80, "analysis": 0.75, "design": 0.12, "networking": 0.70,
            "research": 0.55, "teaching": 0.05, "helping": 0.10, "building": 0.15,
        },
    },
    "Telecommunication and Networking": {
        "subjects": {
            "math": (0.78, 0.09), "physics": (0.72, 0.09),
            "chemistry": (0.42, 0.14), "biology": (0.38, 0.14),
            "english": (0.62, 0.12), "khmer": (0.52, 0.14),
            "history": (0.45, 0.14),
        },
        "strengths": {
            "logic": 0.78, "communication": 0.35, "creativity": 0.35,
            "problem-solving": 0.80, "analytical": 0.72, "leadership": 0.20,
            "teamwork": 0.45, "technical": 0.88,
        },
        "preferences": {
            "coding": 0.65, "analysis": 0.55, "design": 0.18, "networking": 0.92,
            "research": 0.35, "teaching": 0.08, "helping": 0.10, "building": 0.40,
        },
    },
    # ── Traditional Engineering ─────────────────────────────────
    "Civil Engineering": {
        "subjects": {
            "math": (0.75, 0.09), "physics": (0.80, 0.07),
            "chemistry": (0.52, 0.13), "biology": (0.38, 0.14),
            "english": (0.52, 0.13), "khmer": (0.55, 0.13),
            "history": (0.50, 0.13),
        },
        "strengths": {
            "logic": 0.72, "communication": 0.35, "creativity": 0.45,
            "problem-solving": 0.78, "analytical": 0.70, "leadership": 0.35,
            "teamwork": 0.55, "technical": 0.80,
        },
        "preferences": {
            "coding": 0.12, "analysis": 0.50, "design": 0.55, "networking": 0.12,
            "research": 0.30, "teaching": 0.08, "helping": 0.15, "building": 0.92,
        },
    },
    "Mechanical Engineering": {
        "subjects": {
            "math": (0.74, 0.09), "physics": (0.82, 0.07),
            "chemistry": (0.55, 0.12), "biology": (0.36, 0.14),
            "english": (0.50, 0.13), "khmer": (0.52, 0.14),
            "history": (0.45, 0.14),
        },
        "strengths": {
            "logic": 0.75, "communication": 0.28, "creativity": 0.48,
            "problem-solving": 0.82, "analytical": 0.72, "leadership": 0.22,
            "teamwork": 0.50, "technical": 0.85,
        },
        "preferences": {
            "coding": 0.18, "analysis": 0.50, "design": 0.52, "networking": 0.10,
            "research": 0.40, "teaching": 0.08, "helping": 0.12, "building": 0.90,
        },
    },
    "Electrical Engineering": {
        "subjects": {
            "math": (0.78, 0.08), "physics": (0.85, 0.06),
            "chemistry": (0.50, 0.13), "biology": (0.35, 0.14),
            "english": (0.52, 0.13), "khmer": (0.50, 0.14),
            "history": (0.45, 0.14),
        },
        "strengths": {
            "logic": 0.80, "communication": 0.25, "creativity": 0.38,
            "problem-solving": 0.80, "analytical": 0.78, "leadership": 0.18,
            "teamwork": 0.42, "technical": 0.90,
        },
        "preferences": {
            "coding": 0.35, "analysis": 0.60, "design": 0.38, "networking": 0.25,
            "research": 0.45, "teaching": 0.08, "helping": 0.10, "building": 0.82,
        },
    },
    "Chemical Engineering": {
        "subjects": {
            "math": (0.72, 0.09), "physics": (0.68, 0.10),
            "chemistry": (0.85, 0.06), "biology": (0.52, 0.13),
            "english": (0.55, 0.13), "khmer": (0.52, 0.14),
            "history": (0.45, 0.14),
        },
        "strengths": {
            "logic": 0.70, "communication": 0.30, "creativity": 0.35,
            "problem-solving": 0.75, "analytical": 0.75, "leadership": 0.22,
            "teamwork": 0.48, "technical": 0.78,
        },
        "preferences": {
            "coding": 0.12, "analysis": 0.65, "design": 0.30, "networking": 0.10,
            "research": 0.70, "teaching": 0.10, "helping": 0.15, "building": 0.60,
        },
    },
    # ── Medical ─────────────────────────────────────────────────
    "Medicine": {
        "subjects": {
            "math": (0.74, 0.09), "physics": (0.52, 0.13),
            "chemistry": (0.82, 0.07), "biology": (0.90, 0.05),
            "english": (0.68, 0.10), "khmer": (0.60, 0.12),
            "history": (0.50, 0.13),
        },
        "strengths": {
            "logic": 0.55, "communication": 0.75, "creativity": 0.20,
            "problem-solving": 0.70, "analytical": 0.65, "leadership": 0.35,
            "teamwork": 0.65, "technical": 0.40,
        },
        "preferences": {
            "coding": 0.05, "analysis": 0.55, "design": 0.08, "networking": 0.15,
            "research": 0.75, "teaching": 0.22, "helping": 0.95, "building": 0.05,
        },
    },
    "Pharmacy": {
        "subjects": {
            "math": (0.68, 0.10), "physics": (0.48, 0.14),
            "chemistry": (0.88, 0.06), "biology": (0.82, 0.07),
            "english": (0.62, 0.12), "khmer": (0.58, 0.13),
            "history": (0.48, 0.14),
        },
        "strengths": {
            "logic": 0.50, "communication": 0.60, "creativity": 0.20,
            "problem-solving": 0.58, "analytical": 0.65, "leadership": 0.22,
            "teamwork": 0.50, "technical": 0.45,
        },
        "preferences": {
            "coding": 0.05, "analysis": 0.62, "design": 0.08, "networking": 0.12,
            "research": 0.80, "teaching": 0.15, "helping": 0.85, "building": 0.05,
        },
    },
    "Dentistry": {
        "subjects": {
            "math": (0.70, 0.10), "physics": (0.50, 0.13),
            "chemistry": (0.78, 0.08), "biology": (0.85, 0.06),
            "english": (0.62, 0.12), "khmer": (0.58, 0.13),
            "history": (0.48, 0.14),
        },
        "strengths": {
            "logic": 0.48, "communication": 0.65, "creativity": 0.40,
            "problem-solving": 0.60, "analytical": 0.55, "leadership": 0.25,
            "teamwork": 0.55, "technical": 0.55,
        },
        "preferences": {
            "coding": 0.05, "analysis": 0.50, "design": 0.25, "networking": 0.12,
            "research": 0.55, "teaching": 0.18, "helping": 0.88, "building": 0.08,
        },
    },
    # ── Business ────────────────────────────────────────────────
    "Business Administration": {
        "subjects": {
            "math": (0.68, 0.11), "physics": (0.42, 0.14),
            "chemistry": (0.40, 0.14), "biology": (0.38, 0.14),
            "english": (0.78, 0.08), "khmer": (0.62, 0.12),
            "history": (0.58, 0.12),
        },
        "strengths": {
            "logic": 0.55, "communication": 0.85, "creativity": 0.42,
            "problem-solving": 0.55, "analytical": 0.58, "leadership": 0.88,
            "teamwork": 0.80, "technical": 0.20,
        },
        "preferences": {
            "coding": 0.08, "analysis": 0.60, "design": 0.12, "networking": 0.78,
            "research": 0.25, "teaching": 0.18, "helping": 0.35, "building": 0.15,
        },
    },
    "Business Management": {
        "subjects": {
            "math": (0.65, 0.11), "physics": (0.42, 0.14),
            "chemistry": (0.40, 0.14), "biology": (0.38, 0.14),
            "english": (0.75, 0.09), "khmer": (0.60, 0.12),
            "history": (0.55, 0.13),
        },
        "strengths": {
            "logic": 0.52, "communication": 0.82, "creativity": 0.38,
            "problem-solving": 0.58, "analytical": 0.55, "leadership": 0.92,
            "teamwork": 0.85, "technical": 0.18,
        },
        "preferences": {
            "coding": 0.05, "analysis": 0.55, "design": 0.10, "networking": 0.82,
            "research": 0.22, "teaching": 0.22, "helping": 0.40, "building": 0.12,
        },
    },
    "Finance": {
        "subjects": {
            "math": (0.78, 0.08), "physics": (0.45, 0.14),
            "chemistry": (0.40, 0.14), "biology": (0.38, 0.14),
            "english": (0.72, 0.10), "khmer": (0.58, 0.13),
            "history": (0.52, 0.13),
        },
        "strengths": {
            "logic": 0.72, "communication": 0.65, "creativity": 0.28,
            "problem-solving": 0.68, "analytical": 0.85, "leadership": 0.55,
            "teamwork": 0.55, "technical": 0.35,
        },
        "preferences": {
            "coding": 0.18, "analysis": 0.90, "design": 0.08, "networking": 0.55,
            "research": 0.45, "teaching": 0.10, "helping": 0.25, "building": 0.10,
        },
    },
    # ── Humanities / Social ─────────────────────────────────────
    "Psychology": {
        "subjects": {
            "math": (0.48, 0.13), "physics": (0.38, 0.14),
            "chemistry": (0.42, 0.14), "biology": (0.62, 0.11),
            "english": (0.78, 0.08), "khmer": (0.68, 0.10),
            "history": (0.65, 0.11),
        },
        "strengths": {
            "logic": 0.45, "communication": 0.90, "creativity": 0.48,
            "problem-solving": 0.52, "analytical": 0.58, "leadership": 0.35,
            "teamwork": 0.70, "technical": 0.10,
        },
        "preferences": {
            "coding": 0.05, "analysis": 0.55, "design": 0.10, "networking": 0.35,
            "research": 0.75, "teaching": 0.45, "helping": 0.92, "building": 0.05,
        },
    },
    "Education": {
        "subjects": {
            "math": (0.55, 0.13), "physics": (0.42, 0.14),
            "chemistry": (0.42, 0.14), "biology": (0.45, 0.14),
            "english": (0.72, 0.10), "khmer": (0.78, 0.08),
            "history": (0.68, 0.10),
        },
        "strengths": {
            "logic": 0.45, "communication": 0.92, "creativity": 0.62,
            "problem-solving": 0.48, "analytical": 0.45, "leadership": 0.65,
            "teamwork": 0.72, "technical": 0.15,
        },
        "preferences": {
            "coding": 0.05, "analysis": 0.32, "design": 0.18, "networking": 0.30,
            "research": 0.45, "teaching": 0.95, "helping": 0.88, "building": 0.08,
        },
    },
    "International Relations": {
        "subjects": {
            "math": (0.50, 0.13), "physics": (0.38, 0.14),
            "chemistry": (0.38, 0.14), "biology": (0.40, 0.14),
            "english": (0.85, 0.07), "khmer": (0.72, 0.09),
            "history": (0.82, 0.07),
        },
        "strengths": {
            "logic": 0.55, "communication": 0.88, "creativity": 0.42,
            "problem-solving": 0.50, "analytical": 0.62, "leadership": 0.60,
            "teamwork": 0.68, "technical": 0.12,
        },
        "preferences": {
            "coding": 0.05, "analysis": 0.55, "design": 0.08, "networking": 0.72,
            "research": 0.70, "teaching": 0.30, "helping": 0.65, "building": 0.05,
        },
    },
    "Law": {
        "subjects": {
            "math": (0.52, 0.13), "physics": (0.38, 0.14),
            "chemistry": (0.38, 0.14), "biology": (0.40, 0.14),
            "english": (0.82, 0.07), "khmer": (0.78, 0.08),
            "history": (0.80, 0.07),
        },
        "strengths": {
            "logic": 0.75, "communication": 0.90, "creativity": 0.35,
            "problem-solving": 0.55, "analytical": 0.72, "leadership": 0.55,
            "teamwork": 0.52, "technical": 0.10,
        },
        "preferences": {
            "coding": 0.05, "analysis": 0.58, "design": 0.05, "networking": 0.50,
            "research": 0.80, "teaching": 0.25, "helping": 0.72, "building": 0.05,
        },
    },
    # ── Design / Creative ──────────────────────────────────────
    "Architecture": {
        "subjects": {
            "math": (0.72, 0.09), "physics": (0.68, 0.10),
            "chemistry": (0.42, 0.14), "biology": (0.38, 0.14),
            "english": (0.62, 0.12), "khmer": (0.55, 0.13),
            "history": (0.60, 0.12),
        },
        "strengths": {
            "logic": 0.55, "communication": 0.45, "creativity": 0.92,
            "problem-solving": 0.65, "analytical": 0.52, "leadership": 0.30,
            "teamwork": 0.52, "technical": 0.62,
        },
        "preferences": {
            "coding": 0.10, "analysis": 0.30, "design": 0.92, "networking": 0.12,
            "research": 0.30, "teaching": 0.10, "helping": 0.12, "building": 0.88,
        },
    },
    "UX/UI Design": {
        "subjects": {
            "math": (0.58, 0.12), "physics": (0.42, 0.14),
            "chemistry": (0.38, 0.14), "biology": (0.38, 0.14),
            "english": (0.75, 0.09), "khmer": (0.55, 0.13),
            "history": (0.50, 0.13),
        },
        "strengths": {
            "logic": 0.45, "communication": 0.65, "creativity": 0.95,
            "problem-solving": 0.58, "analytical": 0.50, "leadership": 0.22,
            "teamwork": 0.55, "technical": 0.55,
        },
        "preferences": {
            "coding": 0.35, "analysis": 0.35, "design": 0.95, "networking": 0.18,
            "research": 0.40, "teaching": 0.12, "helping": 0.18, "building": 0.45,
        },
    },
    "Graphic Design": {
        "subjects": {
            "math": (0.48, 0.13), "physics": (0.40, 0.14),
            "chemistry": (0.38, 0.14), "biology": (0.38, 0.14),
            "english": (0.70, 0.10), "khmer": (0.58, 0.13),
            "history": (0.58, 0.12),
        },
        "strengths": {
            "logic": 0.30, "communication": 0.58, "creativity": 0.95,
            "problem-solving": 0.42, "analytical": 0.38, "leadership": 0.20,
            "teamwork": 0.48, "technical": 0.42,
        },
        "preferences": {
            "coding": 0.12, "analysis": 0.22, "design": 0.95, "networking": 0.15,
            "research": 0.20, "teaching": 0.12, "helping": 0.15, "building": 0.35,
        },
    },
}

# Default profile for majors not found in PER_MAJOR_PROFILES
_DEFAULT_PROFILE = {
    "subjects": {s: (0.55, 0.15) for s in SUBJECTS},
    "strengths": {s: 0.35 for s in STRENGTHS_MAP},
    "preferences": {p: 0.35 for p in PREFERENCES_MAP},
}


# Interaction feature helpers
STEM_SUBJECTS = ["math", "physics", "chemistry", "biology"]
LANG_SUBJECTS = ["english", "khmer"]


class ModelTrainer:
    def __init__(self, majors_db: Dict, n_estimators: int = 1000,
                 max_depth: int = 30):
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
    
    # ------------------------------------------------------------------
    # Probabilistic Data Generation (replaces hardcoded rules)
    # ------------------------------------------------------------------
    def generate_smart_data(self, n_samples: int = 50000) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate probabilistic synthetic training data using Gaussian
        distributions per major category. Each major's profile defines
        realistic, overlapping distributions for subject scores plus
        Bernoulli probabilities for strengths & preferences.

        Key improvements over hardcoded rules:
        - No label leakage (overlapping distributions)
        - Extensible (add a profile, not an if/elif)
        - Probabilistic (captures natural variance)
        """
        X: List[np.ndarray] = []
        y: List[str] = []
        n_per_major = n_samples // len(self.majors_list)

        logger.info(
            f"Generating probabilistic training data: "
            f"{n_samples} samples ({n_per_major}/major)…"
        )

        for major_name in self.majors_list:
            profile = PER_MAJOR_PROFILES.get(major_name, _DEFAULT_PROFILE)
            major_info = self.majors_db[major_name]
            required_subjects = [s.lower() for s in major_info.get("required_subjects", [])]

            for _ in range(n_per_major):
                # ── 1. Subject scores from Gaussian distributions ──────
                grades: Dict[str, float] = {}
                for subject in SUBJECTS:
                    mean, std = profile["subjects"].get(subject, (0.55, 0.15))
                    # Per-sample jitter to widen coverage
                    jittered_mean = mean + np.random.uniform(-0.05, 0.05)
                    normalised = np.clip(
                        np.random.normal(jittered_mean, std), 0.05, 1.0
                    )
                    grades[subject] = normalised * MAX_SCORES[subject]

                # Slight boost for required subjects (soft, not forced)
                for sub in required_subjects:
                    if sub in grades:
                        boost = np.random.uniform(0.0, 0.15) * MAX_SCORES[sub]
                        grades[sub] = min(grades[sub] + boost, MAX_SCORES[sub])

                # Normalise to 0-1
                grade_features = [grades[s] / MAX_SCORES[s] for s in SUBJECTS]

                # ── 2. Grade statistics (matches feature_builder exactly) ─
                non_zero = [g for g in grade_features if g > 0]
                if non_zero:
                    grade_stats = [
                        float(np.mean(non_zero)),
                        float(np.std(non_zero)),
                        float(max(non_zero)),
                    ]
                else:
                    grade_stats = [0.0, 0.0, 0.0]

                # ── 2b. Interaction features ────────────────────────────
                stem_avg = float(np.mean([
                    grade_features[SUBJECTS.index(s)] for s in STEM_SUBJECTS
                ]))
                lang_avg = float(np.mean([
                    grade_features[SUBJECTS.index(s)] for s in LANG_SUBJECTS
                ]))
                stem_lang_ratio = stem_avg / (lang_avg + 1e-6)
                math_phys = grade_features[0] * grade_features[1]   # math×physics
                chem_bio = grade_features[2] * grade_features[3]    # chemistry×biology
                interaction_features = [
                    stem_avg, lang_avg, stem_lang_ratio,
                    math_phys, chem_bio,
                ]

                # ── 3. Strengths (Bernoulli sampling) ───────────────────
                strength_vec = np.zeros(len(STRENGTHS_MAP))
                for sname, sidx in STRENGTHS_MAP.items():
                    prob = profile["strengths"].get(sname, 0.35)
                    prob = np.clip(prob + np.random.uniform(-0.10, 0.10), 0.0, 1.0)
                    strength_vec[sidx] = 1.0 if np.random.random() < prob else 0.0

                # ── 4. Preferences (Bernoulli sampling) ─────────────────
                pref_vec = np.zeros(len(PREFERENCES_MAP))
                for pname, pidx in PREFERENCES_MAP.items():
                    prob = profile["preferences"].get(pname, 0.35)
                    prob = np.clip(prob + np.random.uniform(-0.10, 0.10), 0.0, 1.0)
                    pref_vec[pidx] = 1.0 if np.random.random() < prob else 0.0

                # ── 5. SBERT similarity (overlapping Gaussians) ─────────
                sim_scores: List[float] = []
                for m in self.majors_list:
                    if m == major_name:
                        s = np.clip(np.random.normal(0.62, 0.12), 0.0, 1.0)
                    else:
                        s = np.clip(np.random.normal(0.32, 0.12), 0.0, 1.0)
                    sim_scores.append(s)

                # ── 6. Eligibility (data-driven from required subjects) ─
                elig_flags: List[float] = []
                for m in self.majors_list:
                    m_info = self.majors_db.get(m, {})
                    m_req = [r.lower() for r in m_info.get("required_subjects", [])]
                    if not m_req:
                        elig_flags.append(1.0)
                        continue
                    # Average normalised score for required subjects
                    req_scores = [
                        grades.get(r, 0) / MAX_SCORES.get(r, 100) for r in m_req
                    ]
                    avg_req = np.mean(req_scores)
                    if avg_req >= 0.50:
                        elig = np.clip(
                            0.5 + avg_req * 0.5 + np.random.normal(0, 0.08),
                            0.0, 1.0,
                        )
                    else:
                        elig = np.clip(
                            0.2 + np.random.normal(0, 0.08), 0.0, 0.6
                        )
                    elig_flags.append(elig)

                # ── Combine ─────────────────────────────────────────────
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
        logger.info("Starting training process...")
        X, y = self.generate_smart_data(n_samples)

        # ── Feature Scaling ─────────────────────────────────────────
        self.scaler.fit(X)
        X_scaled = self.scaler.transform(X)

        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42, stratify=y
        )

        self.model.fit(X_train, y_train)

        y_pred = self.model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)

        # Cross-validation for robust accuracy estimation
        logger.info("Running 5-fold cross-validation...")
        cv_scores = cross_val_score(
            self.model, X_scaled, y, cv=5, scoring="accuracy", n_jobs=-1
        )
        logger.info(
            f"CV Accuracy: {cv_scores.mean():.4f} "
            f"(+/- {cv_scores.std() * 2:.4f})"
        )

        # Per-class classification report
        report_dict = classification_report(y_test, y_pred, output_dict=True)
        logger.info(
            f"Classification Report:\n"
            f"{classification_report(y_test, y_pred)}"
        )

        logger.info(f"Test Accuracy: {acc:.4f}")

        # ── Save artefacts ──────────────────────────────────────────
        if not MODEL_DIR.exists():
            MODEL_DIR.mkdir(parents=True)

        joblib.dump(self.model, MODEL_PATH)
        joblib.dump(self.scaler, SCALER_PATH)

        # Save feature names
        feature_names = (
            [f"grade_{s}" for s in SUBJECTS]
            + ["grade_mean", "grade_std", "grade_max"]
            + ["stem_avg", "lang_avg", "stem_lang_ratio",
               "math_phys_interaction", "chem_bio_interaction"]
            + [f"strength_{i}" for i in range(8)]
            + [f"pref_{i}" for i in range(8)]
            + [f"sim_{m}" for m in self.majors_list]
            + [f"elig_{m}" for m in self.majors_list]
        )
        joblib.dump(feature_names, FEATURES_PATH)

        # Save training metadata for monitoring
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
    """Entry point wrapper – passes through keyword arguments."""
    n_estimators = kwargs.get("n_estimators", 1000)
    max_depth = kwargs.get("max_depth", 30)
    n_samples = kwargs.get("n_samples", 50000)

    trainer = ModelTrainer(
        majors_database,
        n_estimators=n_estimators,
        max_depth=max_depth,
    )
    return trainer.train(n_samples=n_samples)
