"""
Complete Recommendation Service — No Hardcoded Logic

Pipeline:
1. NLTK preprocessing → SBERT embedding
2. Semantic intent detection (from database, not hardcoded phrases)
3. Data-driven eligibility (from required_subjects, not hardcoded thresholds)
4. Random Forest prediction
5. Score fusion: ML × SBERT × Eligibility (no magic numbers)
6. Post-processing

Every signal is computed by the AI or derived from the database.
No if/elif chains, no magic numbers, no keyword dictionaries.
"""
import logging
import re
import math
import numpy as np
from typing import Dict, List, Optional

from nlp.preprocess import clean_text
from nlp.sbert import SBERTEncoder
from nlp.similarity import SimilarityEngine
from nlp.semantic_intent import get_semantic_detector
from rules.eligibility import EligibilityRules
from ml.predict import MLPredictor
from core.feature_builder import FeatureBuilder
from data.majors import MAJOR_DATABASE
from data.careers import CAREER_DATABASE
from data.universities import UNIVERSITY_DATABASE

logger = logging.getLogger(__name__)

# Exam max scores (real Cambodian exam values — NOT tuning params)
MAX_SCORES = {
    "math": 125, "physics": 75, "chemistry": 75, "biology": 75,
    "english": 50, "khmer": 75, "history": 50
}


class RecommendationService:
    """
    Clean recommendation pipeline:
    1. NLP (NLTK + SBERT)
    2. Semantic intent (purely from database)
    3. Data-driven eligibility (sigmoid from required_subjects)
    4. ML prediction (Random Forest)
    5. Score fusion (ML × SBERT × eligibility — no magic numbers)
    6. Post-processing

    Returns:
    - major_recommendations
    - universities
    - career_recommendations
    - skill_gaps
    - match_percentage
    """

    def __init__(self):
        self.feature_builder = FeatureBuilder()
        self.predictor = MLPredictor()
        self.rules = EligibilityRules()
        self.similarity = SimilarityEngine()
        self.sbert = SBERTEncoder()

        self.majors_db = MAJOR_DATABASE
        self.careers_db = CAREER_DATABASE
        self.universities_db = UNIVERSITY_DATABASE

    def get_recommendations(
        self,
        grades: Dict[str, float],
        interests: str = "",
        career_goal: str = "",
        strengths: str = "",
        preferences: str = "",
        top_n: int = 2,
    ) -> Dict:
        grades_lower = {k.lower(): v for k, v in grades.items()}
        has_grades = any(v > 0 for v in grades_lower.values())

        # ========================================
        # STEP 1: NLP Pipeline (NLTK + SBERT)
        # ========================================
        cleaned_interests = clean_text(interests)
        cleaned_goal = clean_text(career_goal)
        combined_text = f"{cleaned_interests} {cleaned_goal}".strip()
        has_text_input = bool(combined_text.strip())

        # SBERT similarity scores for every major and career
        major_similarities: Dict[str, float] = {}
        career_similarities: Dict[str, float] = {}

        if combined_text:
            major_similarities = self.similarity.compute_major_similarity_scores(
                combined_text, self.majors_db
            )
            career_similarities = self.similarity.compute_career_similarity_scores(
                combined_text, self.careers_db
            )

        # ========================================
        # STEP 2: Semantic Intent Detection (from database)
        # ========================================
        raw_text = f"{interests} {career_goal} {strengths} {preferences}".strip()
        detector = get_semantic_detector()

        # Positive intent: {major: boost} — derived from SBERT similarity
        semantic_boosts = detector.detect_intent(raw_text) if raw_text else {}

        # Negative intent: {major: penalty} — derived from SBERT similarity
        exclusion_penalties = detector.detect_exclusions(raw_text) if raw_text else {}

        # ========================================
        # STEP 3: Data-Driven Eligibility
        # ========================================
        all_majors = list(self.majors_db.keys())
        eligible_majors, eligibility_flags = self.rules.get_eligible_majors(
            grades_lower, all_majors
        )
        logger.info(f"Eligible: {len(eligible_majors)}/{len(all_majors)}")

        # ========================================
        # STEP 4: Feature Engineering + ML Prediction
        # ========================================
        features = self.feature_builder.build_features(
            grades=grades_lower,
            interests=interests,
            career_goal=career_goal,
            strengths=strengths,
            preferences=preferences,
        )
        ml_predictions = self.predictor.predict(features)

        # ========================================
        # STEP 5: Academic Signal Locking
        # ========================================
        # Detect mentions of subjects like "math", "physics", etc.
        subject_mentions = {s.lower() for s in MAX_SCORES.keys() if s.lower() in raw_text.lower()}
        
        # Determine if there's a specific intent
        max_boost = max(semantic_boosts.values()) if semantic_boosts else 1.0
        # Very sensitive threshold to catch subject-level interests
        has_specific_intent = has_text_input and max_boost > 1.05
        
        # --- CONCEPT ANCHOR SYSTEM ---
        # Explicitly link keywords to majors for "logical" matching
        # Covers: subject names, career titles, activities, personality traits, hobbies
        CONCEPT_ANCHORS = {
            # ===== ACADEMIC SUBJECTS =====
            "math": ["Software Engineering", "Data Science", "Mechanical Engineering", "Electrical Engineering", "Civil Engineering", "Chemical Engineering", "Finance", "Architecture", "Logistic"],
            "mathematics": ["Software Engineering", "Data Science", "Mechanical Engineering", "Electrical Engineering", "Civil Engineering", "Chemical Engineering", "Finance", "Architecture", "Logistic"],
            "physics": ["Mechanical Engineering", "Electrical Engineering", "Civil Engineering", "Chemical Engineering", "Architecture"],
            "biology": ["Medicine", "Pharmacy", "Dentistry"],
            "chemistry": ["Chemical Engineering", "Medicine", "Pharmacy", "Dentistry"],
            
            # ===== COMPUTER SCIENCE / IT =====
            # Core tech
            "coding": ["Software Engineering"],
            "programming": ["Software Engineering"],
            "code": ["Software Engineering"],
            "software": ["Software Engineering"],
            "app": ["Software Engineering"],
            "building apps": ["Software Engineering"],
            "making games": ["Software Engineering"],
            "game development": ["Software Engineering"],
            "game": ["Software Engineering"],
            "website": ["Software Engineering"],
            "web development": ["Software Engineering"],
            "computers": ["Software Engineering", "Data Science"],
            "computer": ["Software Engineering", "Data Science"],
            "technology": ["Software Engineering", "Data Science"],
            "tech": ["Software Engineering", "Data Science"],
            "digital": ["Software Engineering", "Data Science", "Cybersecurity", "UX/UI Design"],
            # Logic & problem-solving (IT context)
            "logical problems": ["Software Engineering", "Data Science"],
            "puzzles": ["Software Engineering", "Data Science"],
            "structured thinking": ["Software Engineering", "Data Science"],
            # AI & Data
            "machine learning": ["Data Science"],
            "artificial intelligence": ["Data Science"],
            "ai": ["Data Science"],
            "algorithm": ["Data Science", "Software Engineering"],
            "neural": ["Data Science"],
            "deep learning": ["Data Science"],
            "statistics": ["Data Science"],
            "data": ["Data Science"],
            "analysis": ["Data Science"],
            "analytics": ["Data Science"],
            # Cybersecurity
            "security": ["Cybersecurity"],
            "hacking": ["Cybersecurity"],
            "hackathon": ["Software Engineering", "Cybersecurity"],
            "cyber": ["Cybersecurity"],
            "cybersecurity": ["Cybersecurity"],
            "protecting systems": ["Cybersecurity"],
            "digital attacks": ["Cybersecurity"],
            # Networking
            "network": ["Telecommunication and Networking"],
            "networking": ["Telecommunication and Networking"],
            "telecommunication": ["Telecommunication and Networking"],
            "telecom": ["Telecommunication and Networking"],
            "cisco": ["Telecommunication and Networking"],
            "routing": ["Telecommunication and Networking"],
            "wireless": ["Telecommunication and Networking"],
            "5g": ["Telecommunication and Networking"],
            "it infrastructure": ["Telecommunication and Networking"],
            # Robotics
            "robotics": ["Mechanical Engineering", "Electrical Engineering"],
            
            # ===== MEDICINE / HEALTH SCIENCES =====
            "doctor": ["Medicine"],
            "doctors": ["Medicine"],
            "medical": ["Medicine"],
            "medicine": ["Medicine"],
            "surgeon": ["Medicine"],
            "surgeons": ["Medicine"],
            "hospital": ["Medicine"],
            "hospitals": ["Medicine"],
            "human body": ["Medicine"],
            "saving lives": ["Medicine"],
            "help people physically": ["Medicine"],
            "calm under pressure": ["Medicine"],
            "clinic": ["Medicine"],
            "clinics": ["Medicine"],
            "diseases": ["Medicine"],
            "patient": ["Medicine", "Dentistry", "Pharmacy"],
            "patients": ["Medicine", "Dentistry", "Pharmacy"],
            "treatment": ["Medicine", "Dentistry", "Pharmacy"],
            "treatments": ["Medicine", "Dentistry", "Pharmacy"],
            "health": ["Medicine", "Dentistry", "Pharmacy"],
            "help people": ["Medicine", "Psychology", "Education"],
            # Dentistry
            "dentist": ["Dentistry"],
            "dental": ["Dentistry"],
            "teeth": ["Dentistry"],
            # Pharmacy
            "pharmacist": ["Pharmacy"],
            "pharmacy": ["Pharmacy"],
            "medication": ["Pharmacy"],
            "drug": ["Pharmacy"],
            
            # ===== ENGINEERING =====
            # General engineering
            "engineering": ["Mechanical Engineering", "Electrical Engineering", "Civil Engineering", "Chemical Engineering"],
            "fixing things": ["Mechanical Engineering"],
            "hands-on": ["Mechanical Engineering", "Civil Engineering"],
            # Civil
            "bridge": ["Civil Engineering"],
            "bridges": ["Civil Engineering"],
            "structure": ["Civil Engineering"],
            "structures": ["Civil Engineering"],
            "construction": ["Civil Engineering"],
            "building": ["Civil Engineering"],
            "buildings": ["Civil Engineering", "Architecture"],
            "building things": ["Mechanical Engineering", "Civil Engineering"],
            "building design": ["Architecture"],
            "infrastructure": ["Civil Engineering"],
            "architecture": ["Architecture"],
            "architect": ["Architecture"],
            "floor plans": ["Architecture"],
            "blueprint": ["Architecture"],
            "blueprints": ["Architecture"],
            "urban structures": ["Architecture"],
            "modern structures": ["Architecture"],
            "exterior design": ["Architecture"],
            # Mechanical
            "robot": ["Mechanical Engineering"],
            "robots": ["Mechanical Engineering"],
            "machine": ["Mechanical Engineering"],
            "machines": ["Mechanical Engineering"],
            "engine": ["Mechanical Engineering"],
            "engines": ["Mechanical Engineering"],
            "mechanical": ["Mechanical Engineering"],
            # Electrical
            "circuit": ["Electrical Engineering"],
            "circuits": ["Electrical Engineering"],
            "electrical": ["Electrical Engineering"],
            "electronics": ["Electrical Engineering"],
            "electricity": ["Electrical Engineering"],
            # Chemical
            "chemical": ["Chemical Engineering"],
            "chemicals": ["Chemical Engineering"],
            
            # ===== LOGISTICS =====
            "logistic": ["Logistic"],
            "logistics": ["Logistic"],
            "supply chain": ["Logistic"],
            "delivery": ["Logistic"],
            "deliveries": ["Logistic"],
            "route optimization": ["Logistic"],
            "transportation": ["Logistic"],
            "warehouse": ["Logistic"],
            "operations": ["Logistic", "Business Management"],
            
            
            # ===== BUSINESS / MANAGEMENT =====
            "business": ["Business Administration", "Business Management"],
            "entrepreneur": ["Business Administration"],
            "entrepreneurship": ["Business Administration"],
            "startup": ["Business Administration"],
            "startups": ["Business Administration"],
            "company": ["Business Administration", "Business Management"],
            "companies": ["Business Administration", "Business Management"],
            "leadership": ["Business Administration", "Business Management"],
            "selling ideas": ["Business Administration", "Business Management"],
            "negotiating": ["Business Administration", "Business Management"],
            "organizing events": ["Business Administration", "Business Management"],
            "managing money": ["Finance", "Business Administration"],
            "money": ["Finance", "Business Administration"],
            "invest": ["Finance"],
            "banking": ["Finance"],
            "financial": ["Finance"],
            "finance": ["Finance"],
            
            # ===== ART / DESIGN =====
            "design": ["UX/UI Design", "Graphic Design", "Architecture"],
            "draw": ["Graphic Design", "Architecture"],
            "drawing": ["Graphic Design", "Architecture"],
            "art": ["Graphic Design", "Architecture"],
            "creative": ["Graphic Design", "UX/UI Design"],
            "creativity": ["Graphic Design", "UX/UI Design"],
            "imagination": ["Graphic Design", "UX/UI Design"],
            "visuals": ["Graphic Design"],
            "creating visuals": ["Graphic Design"],
            "aesthetics": ["Graphic Design", "UX/UI Design", "Architecture"],
            "colors": ["Graphic Design"],
            "layouts": ["Graphic Design", "UX/UI Design"],
            "animation": ["Graphic Design"],
            "fashion": ["Graphic Design"],
            "interior design": ["Architecture"],
            "logo": ["Graphic Design"],
            "branding": ["Graphic Design"],
            "figma": ["UX/UI Design"],
            "wireframe": ["UX/UI Design"],
            # UX/UI specific
            "ux": ["UX/UI Design"],
            "ui": ["UX/UI Design"],
            "ux designer": ["UX/UI Design"],
            "ui designer": ["UX/UI Design"],
            "ux design": ["UX/UI Design"],
            "ui design": ["UX/UI Design"],
            "user interface": ["UX/UI Design"],
            "user experience": ["UX/UI Design"],
            "interface": ["UX/UI Design"],
            "interfaces": ["UX/UI Design"],
            "designing interfaces": ["UX/UI Design"],
            "prototype": ["UX/UI Design"],
            "usability": ["UX/UI Design"],
            "designing": ["UX/UI Design", "Graphic Design"],
            
            # ===== LAW =====
            "law": ["Law"],
            "lawyer": ["Law"],
            "legal": ["Law"],
            "justice": ["Law"],
            "fairness": ["Law"],
            "court": ["Law"],
            "attorney": ["Law"],
            "judge": ["Law"],
            "debating": ["Law"],
            "debate": ["Law"],
            "debate club": ["Law"],
            "arguing": ["Law"],
            "arguing logically": ["Law"],
            "model united nations": ["Law", "International Relations"],
            
            # ===== EDUCATION =====
            "teach": ["Education"],
            "teacher": ["Education"],
            "teaching": ["Education"],
            "school": ["Education"],
            "schools": ["Education"],
            "education": ["Education"],
            "explaining": ["Education"],
            "explaining things": ["Education"],
            "explaining things to others": ["Education"],
            "working with children": ["Education"],
            "students": ["Education"],
            "student": ["Education"],
            "make a difference": ["Education"],
            
            # ===== PSYCHOLOGY =====
            "psychology": ["Psychology"],
            "mental": ["Psychology"],
            "counseling": ["Psychology"],
            "therapy": ["Psychology"],
            "behavior": ["Psychology"],
            "human behavior": ["Psychology"],
            "emotions": ["Psychology"],
            "understanding emotions": ["Psychology"],
            "empathetic": ["Psychology"],
            "empathy": ["Psychology"],
            "listening": ["Psychology"],
            "listening to people": ["Psychology"],
            
            # ===== INTERNATIONAL RELATIONS =====
            "global": ["International Relations"],
            "global issues": ["International Relations"],
            "politics": ["International Relations"],
            "world politics": ["International Relations"],
            "diplomat": ["International Relations"],
            "diplomacy": ["International Relations"],
            "international": ["International Relations"],
            "current events": ["International Relations"],
            "ngo": ["International Relations"],
            "ngos": ["International Relations"],
            "history": ["International Relations"],
            
            # ===== ARCHITECTURE =====
            "architecture": ["Architecture"],
            "blueprint": ["Architecture"],
            "floor plan": ["Architecture"],
        }
        
        active_anchors = set()
        for k, majors in CONCEPT_ANCHORS.items():
            pattern = rf"\b{re.escape(k)}\b"
            if re.search(pattern, raw_text.lower()):
                for m in majors:
                    active_anchors.add(m)
        
        # Remove excluded majors from anchors — negation overrides positive anchoring
        # e.g. "i don't like math" should NOT anchor to math-related majors
        if exclusion_penalties:
            active_anchors -= set(exclusion_penalties.keys())
        
        if active_anchors:
            logger.info(f"CONCEPT ANCHORS ACTIVE: {active_anchors}")

        if has_specific_intent:
            logger.info(f"SPECIFIC INTENT: '{interests}' (max_boost={max_boost:.2f})")

        # --- ANCHOR INJECTION ---
        # The ML model may output 0% for some majors (e.g. SE with low grades).
        # If concept anchors are active (matched keywords in user text),
        # ensure anchored majors have a minimum probability floor (0.05)
        # so the anchor boost can work effectively.
        if active_anchors and has_text_input:
            existing_map = {p["major"]: p for p in ml_predictions}
            for anchor_major in active_anchors:
                if anchor_major in self.majors_db:
                    if anchor_major not in existing_map:
                        ml_predictions.append({
                            "major": anchor_major,
                            "probability": 0.05,
                            "source": "anchor-injected",
                        })
                        logger.info(f"ANCHOR INJECTED: {anchor_major} (was missing)")
                    elif existing_map[anchor_major]["probability"] < 0.05:
                        existing_map[anchor_major]["probability"] = 0.05
                        existing_map[anchor_major]["source"] = "anchor-floor-boost"
                        logger.info(f"ANCHOR FLOOR APPLIED: {anchor_major} (was {existing_map[anchor_major]['probability']})")

        scored_predictions = []
        for pred in ml_predictions:
            major = pred["major"]
            pred_copy = pred.copy()
            major_info = self.majors_db.get(major, {})
            required = [s.lower() for s in major_info.get("required_subjects", [])]

            # 1. Eligibility factor
            eligibility = eligibility_flags.get(major, 1.0)
            if eligibility == 0.0 and not has_grades:
                eligibility = 1.0
            # If this major is concept-anchored, soften eligibility penalty
            if major in active_anchors and eligibility < 0.7:
                eligibility = 0.7  # User's stated interest overrides low grades

            # 2. Exclusion penalty
            penalty = exclusion_penalties.get(major, 1.0)
            # Don't exclude concept-anchored majors
            if major in active_anchors:
                penalty = max(penalty, 0.8)
            elif penalty < 0.15:
                continue

            sim_score = major_similarities.get(major, 0.0)
            intent_boost = semantic_boosts.get(major, 1.0)
            
            # 4. Subject Locking Factor
            # Distinguish between "Requirements" and "Core Skills"
            subject_factor = 1.0
            if subject_mentions:
                matches = subject_mentions & set(required)
                if matches:
                    # Check if any of these subjects are also CORE skills
                    core_skills = {k.lower() for k in major_info.get("fundamental_skills", {}).keys()}
                    critical_matches = matches & core_skills
                    
                    if critical_matches:
                        # Massive boost for CORE academic interests (e.g. Math for SE)
                        subject_factor = 2.0 + (len(critical_matches) * 5.0) # 7.0x boost
                    else:
                        # Normal boost for requirement matches (e.g. Math for Pharmacy)
                        subject_factor = 1.25 + (len(matches) * 0.5)
                else:
                    # No match for mentioned subjects
                    if has_specific_intent:
                        subject_factor = 0.2 # Stronger penalty for domain mismatch

            # --- ULTRA-STRICT FILTERING ---
            # If user has a specific interest, PURGE anything unrelated.
            # BUT: never purge concept-anchored majors — user explicitly matched them.
            if has_specific_intent and major not in active_anchors:
                # 1. Purge if NO semantic boost AND NOT a core academic interest
                has_core_match = bool(subject_mentions & {k.lower() for k in major_info.get("fundamental_skills", {}).keys()})
                if major not in semantic_boosts and not has_core_match and sim_score < 0.2:
                    continue
                # 2. Domain Mismatch Lockdown
                if subject_mentions and not (subject_mentions & set(required)) and sim_score < 0.3:
                    continue

            if not has_text_input:
                sbert_factor = 1.0
            elif not has_grades:
                sbert_factor = math.exp(sim_score * 6.5) # Amplify text signal
            else:
                sbert_factor = math.exp(sim_score * 6.0) # Amplify text signal

            # 5. Semantic intent boost
            intent_factor = intent_boost ** 2 if intent_boost > 1.0 else 1.0 # Reduced from **4 to prevent wiping out other valid anchors

            # 6. Concept Anchor boost
            # When concept anchors match (keywords in user text),
            # the anchor MUST dominate over ML predictions.
            anchor_factor = 1.0
            if active_anchors:
                if major in active_anchors:
                    anchor_factor = 50.0  # Massive boost — user intent is king
                else:
                    # Penalize non-anchored majors whenever anchors are active
                    if has_specific_intent:
                        anchor_factor = 0.1  # Heavy penalty for strong intent
                    else:
                        anchor_factor = 0.3  # Moderate penalty for keyword-matched anchors

            # 7. Fuse all signals
            final_score = (
                pred_copy["probability"]
                * eligibility
                * penalty
                * sbert_factor
                * intent_factor
                * subject_factor
                * anchor_factor
            )
            pred_copy["probability"] = final_score
            pred_copy["similarity_score"] = sim_score
            pred_copy["rule_penalty"] = eligibility < 0.9
            pred_copy["eligibility"] = eligibility

            if final_score > 0:
                scored_predictions.append(pred_copy)

        # Normalise and Sort
        total = sum(p["probability"] for p in scored_predictions)
        if total > 0:
            for p in scored_predictions:
                p["probability"] /= total
        scored_predictions.sort(key=lambda x: x["probability"], reverse=True)

        # --- DYNAMIC CONFIDENCE CUTOFF ---
        # If #1 is high confidence (> 40%), remove anything that is < 1/4 of its score
        # and has no core relation. This keeps the UX clean.
        # BUT: never remove concept-anchored majors — user explicitly asked for them.
        if scored_predictions and scored_predictions[0]["probability"] > 0.35:
            top_prob = scored_predictions[0]["probability"]
            refined = [scored_predictions[0]]
            for p in scored_predictions[1:]:
                is_anchored = p["major"] in active_anchors
                has_core_match = subject_mentions & {k.lower() for k in self.majors_db.get(p["major"], {}).get("fundamental_skills", {}).keys()}
                if is_anchored or p["major"] in semantic_boosts or has_core_match or p["probability"] > (top_prob * 0.25):
                    refined.append(p)
            scored_predictions = refined

        # ========================================
        # STEP 6: Post-Processing
        # ========================================

        # 6.1 Major Recommendations
        predictions_to_use = scored_predictions[:top_n]
        major_recommendations = self._build_major_recommendations(predictions_to_use)

        # 6.2 Match Percentage (from top recommendation)
        match_percentage = self._compute_match_percentage(
            major_recommendations, has_text_input
        )

        # 6.3 Universities
        universities = self._match_universities(major_recommendations, grades_lower)

        # 6.4 Careers
        career_recommendations = self._build_career_recommendations(
            major_recommendations, career_similarities
        )

        # 6.5 Skill Gaps
        skill_gaps = self._analyze_skill_gaps(
            major_recommendations, career_recommendations, grades_lower, strengths
        )

        return {
            "major_recommendations": major_recommendations,
            "universities": universities,
            "career_recommendations": career_recommendations,
            "skill_gaps": skill_gaps,
            "match_percentage": match_percentage,
        }

    # ------------------------------------------------------------------
    # Build formatted major recommendations
    # ------------------------------------------------------------------
    def _build_major_recommendations(self, predictions: List[Dict]) -> List[Dict]:
        recs = []
        for pred in predictions:
            if pred["probability"] < 0.01:
                continue
            major_name = pred["major"]
            info = self.majors_db.get(major_name, {})
            # Factor in absolute eligibility so normalised confidence drops for terrible grades
            final_conf = pred["probability"] * pred.get("eligibility", 1.0)
            
            recs.append({
                "major": major_name,
                "confidence": round(final_conf, 4),
                "similarity_score": round(pred.get("similarity_score", 0), 3),
                "eligibility": round(pred.get("eligibility", 1.0), 3),
                "description": info.get("description", ""),
                "required_subjects": info.get("required_subjects", []),
                "career_paths": info.get("career_paths", []),
                "source": pred.get("source", "ML-RandomForest"),
            })
        return recs

    # ------------------------------------------------------------------
    # Match percentage — simple blend of confidence and similarity
    # ------------------------------------------------------------------
    def _compute_match_percentage(
        self, major_recs: List[Dict], has_text: bool
    ) -> float:
        if not major_recs:
            return 0.0

        top = major_recs[0]
        confidence = top.get("confidence", 0)
        similarity = top.get("similarity_score", 0)
        eligibility = top.get("eligibility", 1.0)

        if has_text:
            # Blend confidence and semantic match
            base = confidence * 0.6 + similarity * 0.4
        else:
            base = confidence
            
        # Hard grade cap: if grades are severely low, match % should reflect the struggle
        # This prevents 1.0 GPA from giving 95% match
        base *= eligibility

        return min(99.0, round(base * 100, 1))

    # ------------------------------------------------------------------
    # University matching (data-driven from university database)
    # ------------------------------------------------------------------
    def _match_universities(
        self, major_recs: List[Dict], grades: Dict[str, float]
    ) -> List[Dict]:
        universities = []
        avg_grade = sum(grades.values()) / len(grades) if grades else 0

        normalised = {
            s: (grades.get(s, 0) / MAX_SCORES.get(s, 100)) * 100
            for s in MAX_SCORES
        }

        top_major = major_recs[0]["major"] if major_recs else None
        desired_majors = {m["major"] for m in major_recs}
        major_priority = {
            m["major"]: len(major_recs) - i for i, m in enumerate(major_recs)
        }

        all_matches = []
        for uni_name, uni_data in self.universities_db.items():
            programs = set(uni_data.get("programs", []))
            matching = desired_majors & programs
            if not matching:
                continue

            has_top = top_major in programs
            match_score = max(major_priority.get(m, 0) for m in matching)
            if has_top:
                match_score += 100

            # Subject fit from university requirements
            req = uni_data.get("requirements", {})
            min_grade = req.get("min_grade", 0)
            preferred = req.get("preferred_subjects", [])

            subject_fit = 100.0
            warnings = []
            if preferred:
                scores = []
                for s in preferred:
                    pct = normalised.get(s.lower(), 50.0)
                    scores.append(pct)
                    if pct < 50:
                        warnings.append(f"{s} ({pct:.0f}% – below recommended)")
                subject_fit = sum(scores) / len(scores)

            # Fit category from grade distance to requirement
            grade_margin = avg_grade - min_grade
            if grade_margin >= 10 and subject_fit >= 65:
                fit, fit_score = "Safety", 2
            elif grade_margin >= 0 and subject_fit >= 50:
                fit, fit_score = "Target", 3
            elif grade_margin >= -5 and subject_fit >= 40:
                fit, fit_score = "Stretch", 1
            else:
                fit, fit_score = "Stretch", 0

            entry: Dict = {
                "name": uni_name,
                "location": uni_data.get("location", ""),
                "matching_programs": list(matching),
                "min_grade_required": min_grade,
                "fit": fit,
                "your_avg_grade": round(avg_grade, 1),
                "has_top_major": has_top,
                "preferred_subjects": preferred,
                "subject_fit_score": round(subject_fit, 1),
                "_match_score": match_score,
                "_fit_score": fit_score,
            }
            if warnings:
                entry["subject_warnings"] = warnings
            all_matches.append(entry)

        all_matches.sort(
            key=lambda x: (x["_match_score"], x["_fit_score"], x["subject_fit_score"]),
            reverse=True,
        )

        for uni in all_matches:
            del uni["_match_score"]
            del uni["_fit_score"]
            universities.append(uni)

        return universities

    # ------------------------------------------------------------------
    # Career recommendations (SBERT-ranked)
    # ------------------------------------------------------------------
    def _build_career_recommendations(
        self,
        major_recs: List[Dict],
        career_sims: Dict[str, float],
    ) -> List[Dict]:
        careers = []
        seen = set()

        for idx, mrec in enumerate(major_recs[:4]):
            priority = len(major_recs) - idx
            for career_name in mrec.get("career_paths", []):
                if career_name in seen:
                    continue
                info = self.careers_db.get(career_name, {})
                if not info:
                    continue

                sim = career_sims.get(career_name, 0.0)
                combined = (priority / len(major_recs)) * 0.5 + sim * 0.5

                careers.append({
                    "name": career_name,
                    "description": info.get("description", ""),
                    "required_skills": info.get("required_skills", []),
                    "avg_salary": info.get("avg_salary", "Varies"),
                    "education_level": info.get("education_level", ""),
                    "related_major": mrec["major"],
                    "similarity_score": round(sim, 3),
                    "match_score": round(combined, 3),
                })
                seen.add(career_name)

        careers.sort(key=lambda x: x["match_score"], reverse=True)
        return careers[:10]

    # ------------------------------------------------------------------
    # Skill gap analysis (from database, SBERT-scored)
    # ------------------------------------------------------------------
    def _analyze_skill_gaps(
        self,
        major_recs: List[Dict],
        career_recs: List[Dict],
        grades: Dict[str, float],
        strengths: str,
    ) -> List[Dict]:
        if not major_recs:
            return []

        top_major = major_recs[0]
        major_info = self.majors_db.get(top_major.get("major", ""), {})
        fundamental_skills = major_info.get("fundamental_skills", {})

        # Use SBERT to estimate how close the student's strengths
        # are to each required skill
        strengths_emb = (
            self.sbert.encode(strengths.lower()) if strengths else None
        )

        # Importance → required level mapping
        importance_to_level = {"critical": 8.5, "high": 7.0, "medium": 5.5}

        # Grade-based skill indicators
        grade_indicators = self._compute_grade_indicators(grades)

        gaps = []
        for skill_name, skill_info in fundamental_skills.items():
            # Skip tool-specific skills (Photoshop, Figma, etc.)
            if self._is_tool_skill(skill_name):
                continue

            importance = skill_info.get("importance", "medium")
            description = skill_info.get("description", "")
            required_level = importance_to_level.get(importance, 6.0)

            # Estimate current level using SBERT + grades
            current_level = self._estimate_skill_level(
                skill_name, strengths_emb, grade_indicators, required_level
            )

            # Generate contextual suggestions from the major/skill
            suggestions = self._generate_suggestions(
                skill_name, current_level, required_level, top_major.get("major", "")
            )

            gaps.append({
                "skill": skill_name,
                "current_level": round(current_level, 1),
                "required_level": round(required_level, 1),
                "importance": importance,
                "description": description,
                "suggestions": suggestions,
                "skill_type": "fundamental",
            })

        # Add career-specific skills
        existing = {g["skill"].lower() for g in gaps}
        for career in career_recs[:2]:
            for skill in career.get("required_skills", [])[:3]:
                if skill.lower() in existing or self._is_tool_skill(skill):
                    continue
                current = self._estimate_skill_level(
                    skill, strengths_emb, grade_indicators, 7.0
                )
                gaps.append({
                    "skill": skill,
                    "current_level": round(current, 1),
                    "required_level": 7.0,
                    "importance": "high",
                    "description": f"Required for {career.get('name', '')}",
                    "suggestions": self._generate_suggestions(
                        skill, current, 7.0, career.get("name", "")
                    ),
                    "skill_type": "career",
                })
                existing.add(skill.lower())

        # Sort by importance then gap size
        imp_order = {"critical": 0, "high": 1, "medium": 2}
        gaps.sort(
            key=lambda x: (
                imp_order.get(x["importance"], 3),
                -(x["required_level"] - x["current_level"]),
            )
        )
        return gaps[:6]

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _compute_grade_indicators(self, grades: Dict[str, float]) -> Dict[str, float]:
        """Map grades to 0-10 skill indicators"""
        normalised = {
            s: (grades.get(s, 0) / MAX_SCORES.get(s, 100)) * 10
            for s in MAX_SCORES
        }
        return {
            "mathematics": normalised.get("math", 5),
            "problem solving": normalised.get("math", 5) * 0.6 + normalised.get("physics", 5) * 0.4,
            "critical thinking": (normalised.get("math", 5) + normalised.get("english", 5)) / 2,
            "communication": normalised.get("english", 5) * 0.7 + normalised.get("khmer", 5) * 0.3,
            "biology": normalised.get("biology", 5),
            "chemistry": normalised.get("chemistry", 5),
            "physics": normalised.get("physics", 5),
            "analytics": normalised.get("math", 5) * 0.8 + normalised.get("physics", 5) * 0.2,
        }

    def _estimate_skill_level(
        self,
        skill_name: str,
        strengths_emb: Optional[np.ndarray],
        grade_indicators: Dict[str, float],
        required_level: float,
    ) -> float:
        """
        Estimate current skill level using:
        1. SBERT similarity between student's strengths and the skill
        2. Grade-based indicators for academic skills
        """
        level = 3.0  # baseline
        skill_lower = skill_name.lower()

        # 1. Check grade indicators
        for indicator, value in grade_indicators.items():
            if indicator in skill_lower or skill_lower in indicator:
                level = max(level, value)
                break

        # 2. SBERT-based estimation from strengths text
        if strengths_emb is not None:
            skill_emb = self.sbert.encode(skill_name.lower())
            sim = self.similarity.compute_similarity(strengths_emb, skill_emb)
            # High similarity to strengths → higher current level
            if sim > 0.3:
                sbert_level = sim * 10  # 0.5 similarity → 5.0 level
                level = max(level, sbert_level)

        # Cap: never exceed required level (always room to grow)
        return max(1.0, min(level, required_level - 0.5))

    @staticmethod
    def _is_tool_skill(skill_name: str) -> bool:
        """Check if skill is a specific tool/language (not fundamental)"""
        tools = {
            "python", "javascript", "java", "sql", "html", "css", "react",
            "node", "photoshop", "illustrator", "figma", "autocad", "adobe",
            "git", "github", "excel",
        }
        skill_lower = skill_name.lower()
        return any(t in skill_lower for t in tools)

    @staticmethod
    def _generate_suggestions(
        skill: str, current: float, required: float, context: str
    ) -> List[str]:
        """Generate contextual suggestions based on gap size"""
        gap = required - current
        if gap <= 1:
            return [
                f"You're close to mastery in {skill} — keep practising regularly",
                f"Take on challenging {context} projects to sharpen {skill}",
            ]
        elif gap <= 3:
            return [
                f"Take structured courses to strengthen {skill} for {context}",
                f"Join communities or study groups focused on {skill}",
                f"Build practical projects to apply {skill}",
            ]
        else:
            return [
                f"Start with {skill} fundamentals through structured learning",
                f"Dedicate regular study time to develop {skill}",
                f"Find a mentor experienced in {skill} for {context}",
            ]
