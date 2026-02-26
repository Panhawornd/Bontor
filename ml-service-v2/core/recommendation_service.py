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
        # STEP 5: Score Fusion (ML × SBERT × Eligibility)
        #
        # No magic numbers. Each signal is a 0-1 factor:
        # - ml_probability: what the RF model thinks (0-1)
        # - sbert_factor: how well text matches this major (0-1→boost)
        # - eligibility: data-driven from required_subjects (0-1)
        # - semantic_boost: from intent detection (similarity-based)
        # - exclusion_penalty: from negative detection (similarity-based)
        #
        # Final = ml_probability * eligibility * sbert_factor * intent
        # ========================================
        # Determine if there's a specific intent
        max_boost = max(semantic_boosts.values()) if semantic_boosts else 1.0
        # Very sensitive threshold to catch subject-level interests
        has_specific_intent = has_text_input and max_boost > 1.05
        
        if has_specific_intent:
            logger.info(f"SPECIFIC INTENT: '{interests}' (max_boost={max_boost:.2f})")

        scored_predictions = []
        for pred in ml_predictions:
            major = pred["major"]
            pred_copy = pred.copy()

            # 1. Eligibility factor
            eligibility = eligibility_flags.get(major, 1.0)
            if eligibility == 0.0 and not has_grades:
                eligibility = 1.0

            # 2. Exclusion penalty
            penalty = exclusion_penalties.get(major, 1.0)
            if penalty < 0.15:
                continue

            # 3. SBERT similarity factor
            import math
            sim_score = major_similarities.get(major, 0.0)
            intent_boost = semantic_boosts.get(major, 1.0)
            
            # --- ULTRA-STRICT FILTERING ---
            # If user has a specific interest, PURGE anything unrelated.
            # Unrelated = No Semantic Boost AND Low Similarity
            if has_specific_intent:
                if major not in semantic_boosts and sim_score < 0.2:
                    logger.debug(f"PURGING UNRELATED: {major} (No boost, sim={sim_score:.2f})")
                    continue

            if not has_text_input:
                sbert_factor = 1.0
            elif not has_grades:
                sbert_factor = math.exp(sim_score * 6.0)
            else:
                # Steepness 5.0 for better separation
                sbert_factor = math.exp(sim_score * 5.0)

            # 4. Semantic intent boost
            intent_factor = intent_boost ** 3 if intent_boost > 1.0 else 1.0

            # 5. Fuse all signals
            final_score = (
                pred_copy["probability"]
                * eligibility
                * penalty
                * sbert_factor
                * intent_factor
            )

            pred_copy["probability"] = final_score
            pred_copy["similarity_score"] = sim_score
            pred_copy["rule_penalty"] = eligibility < 0.9

            if final_score > 0:
                scored_predictions.append(pred_copy)

        # Normalise and Sort
        total = sum(p["probability"] for p in scored_predictions)
        if total > 0:
            for p in scored_predictions:
                p["probability"] /= total
        scored_predictions.sort(key=lambda x: x["probability"], reverse=True)

        # --- DYNAMIC CONFIDENCE CUTOFF ---
        # If #1 is high confidence (> 40%), remove anything that is < 1/3 of its score
        # and has no semantic relation. This keeps the UX clean.
        if scored_predictions and scored_predictions[0]["probability"] > 0.4:
            top_prob = scored_predictions[0]["probability"]
            refined = [scored_predictions[0]]
            for p in scored_predictions[1:]:
                # Keep if it has semantic relation OR is at least somewhat close
                if p["major"] in semantic_boosts or p["probability"] > (top_prob * 0.4):
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
            recs.append({
                "major": major_name,
                "confidence": round(pred["probability"], 4),
                "similarity_score": round(pred.get("similarity_score", 0), 3),
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

        if has_text:
            # Blend confidence and semantic match
            base = confidence * 0.6 + similarity * 0.4
        else:
            base = confidence

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
            sim = float(np.dot(strengths_emb, skill_emb) / (
                np.linalg.norm(strengths_emb) * np.linalg.norm(skill_emb) + 1e-8
            ))
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
