"""
Complete Recommendation Service
Integrates NLP + ML + Rules for final recommendations

Output ONLY:
- major_recommendations
- universities
- career_recommendations  
- skill_gaps
- match_percentage (suitability percentage)
"""
import logging
from typing import Dict, List, Optional

from nlp.preprocess import clean_text
from nlp.sbert import SBERTEncoder
from nlp.similarity import SimilarityEngine
from rules.eligibility import EligibilityRules
from ml.predict import MLPredictor
from core.feature_builder import FeatureBuilder
from data.majors import MAJOR_DATABASE
from data.careers import CAREER_DATABASE
from data.universities import UNIVERSITY_DATABASE

logger = logging.getLogger(__name__)


class RecommendationService:
    """
    Complete recommendation pipeline:
    1. NLTK preprocessing
    2. SBERT embedding
    3. Rule-based filtering (BEFORE ML)
    4. Random Forest prediction
    5. Post-processing
    
    Returns ONLY:
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
        top_n: int = 4
    ) -> Dict:
        """
        Complete recommendation workflow
        
        Args:
            grades: Subject scores (raw, not normalized)
            interests: Student interests text
            career_goal: Career goal text (optional)
            strengths: Strengths description
            preferences: Preferences description
            top_n: Number of top majors to return
            
        Returns:
            {
                "major_recommendations": [...],
                "universities": [...],
                "career_recommendations": [...],
                "skill_gaps": [...],
                "match_percentage": float
            }
        """
        # Normalize grade keys
        grades_lower = {k.lower(): v for k, v in grades.items()}
        
        # ========================================
        # STEP 1: NLP Pipeline (NLTK + SBERT)
        # ========================================
        
        # Clean text using NLTK (runs BEFORE SBERT)
        cleaned_interests = clean_text(interests)
        cleaned_goal = clean_text(career_goal)
        combined_text = f"{cleaned_interests} {cleaned_goal}".strip()
        
        # Expand short/vague inputs with synonyms
        expanded_text = self._expand_minimal_input(combined_text, career_goal, interests)
        
        # Compute SBERT similarity scores
        major_similarities = {}
        career_similarities = {}
        
        if expanded_text:
            major_similarities = self.similarity.compute_major_similarity_scores(
                expanded_text, self.majors_db
            )
            career_similarities = self.similarity.compute_career_similarity_scores(
                expanded_text, self.careers_db
            )
        
        # If no text provided, infer interests from grades
        has_text_input = bool(combined_text.strip())
        grade_inferred_majors = {}
        if not has_text_input:
            grade_inferred_majors = self._infer_majors_from_grades(grades_lower)
        
        # ========================================
        # STEP 2: Rule-Based Filtering (BEFORE ML)
        # ========================================
        
        all_majors = list(self.majors_db.keys())
        eligible_majors, eligibility_flags = self.rules.get_eligible_majors(
            grades_lower, all_majors
        )
        
        logger.info(f"Eligible majors after rules: {len(eligible_majors)}/{len(all_majors)}")
        
        # ========================================
        # STEP 3: Feature Engineering
        # ========================================
        
        features = self.feature_builder.build_features(
            grades=grades_lower,
            interests=interests,
            career_goal=career_goal,
            strengths=strengths,
            preferences=preferences
        )
        
        # ========================================
        # STEP 4: ML Prediction (Random Forest)
        # ========================================
        
        ml_predictions = self.predictor.predict(features)
        
        # Find max similarity score to know if SBERT found strong matches
        max_similarity = max(major_similarities.values()) if major_similarities else 0.0
        
        # Apply rule filtering to ML predictions
        # RULES OVERRIDE ML
        filtered_predictions = []
        for pred in ml_predictions:
            # Make a shallow copy to avoid mutating cached/reused objects
            pred_copy = dict(pred)
            major = pred_copy['major']
            eligibility = eligibility_flags.get(major, 1.0)
            
            if eligibility == 0.0:
                # Excluded by rules - skip
                continue
            
            # Apply eligibility penalty
            pred_copy['probability'] *= eligibility
            
            # Boost based on SBERT similarity (if available)
            # When user provides clear text input, semantic match should be trusted
            similarity_score = major_similarities.get(major, 0.0)
            
            if has_text_input and max_similarity > 0.25:
                # User provided clear text input - SBERT should drive recommendations
                # Strong semantic match = big boost
                if similarity_score > 0.35:
                    # Good SBERT match - significant boost
                    sbert_boost = similarity_score * 1.5
                    pred_copy['probability'] += sbert_boost
                elif similarity_score > 0.25:
                    # Moderate match - small boost
                    pred_copy['probability'] *= 1.3
                elif similarity_score > 0.20:
                    # Weak match - slight penalty
                    pred_copy['probability'] *= 0.3
                else:
                    # No semantic match to user's stated interests
                    # EXCLUDE unrelated majors entirely when user clearly stated interest
                    pred_copy['probability'] = 0.0
            else:
                # No text input - rely more on ML + grade-inferred boosts
                if not has_text_input and major in grade_inferred_majors:
                    grade_boost = grade_inferred_majors[major]
                    pred_copy['probability'] *= (1 + grade_boost * 2.0)
            
            pred_copy['similarity_score'] = similarity_score
            pred_copy['rule_penalty'] = eligibility < 1.0
            
            # Only include if probability > 0
            if pred_copy['probability'] > 0:
                filtered_predictions.append(pred_copy)
        
        # Re-normalize probabilities
        total_prob = sum(p['probability'] for p in filtered_predictions)
        if total_prob > 0:
            for pred in filtered_predictions:
                pred['probability'] /= total_prob
        
        # Sort by probability
        filtered_predictions.sort(key=lambda x: x['probability'], reverse=True)
        
        # ========================================
        # STEP 5: Post-Processing
        # ========================================
        
        # 5.1 Major Recommendations - Only return majors that actually match
        # If user provided interest, only return majors with semantic match
        if has_text_input and max_similarity > 0.25:
            # Filter to only show majors with meaningful similarity (related to user's interests)
            relevant_predictions = [
                p for p in filtered_predictions 
                if p.get('similarity_score', 0) >= 0.22
            ]
            # Use relevant predictions, limit to top_n
            predictions_to_use = relevant_predictions[:top_n] if relevant_predictions else filtered_predictions[:1]
        else:
            predictions_to_use = filtered_predictions[:top_n]
        
        major_recommendations = self._build_major_recommendations(predictions_to_use)
        
        # Calculate match percentage (top major probability as percentage)
        match_percentage = 0.0
        if major_recommendations:
            # Use weighted average of probability and similarity
            top_prob = major_recommendations[0].get('confidence', 0)
            top_sim = major_recommendations[0].get('similarity_score', 0)
            match_percentage = min(100, round((top_prob * 70 + top_sim * 30) * 100, 1))
        
        # 5.2 University Matching
        universities = self._match_universities(
            major_recommendations, grades_lower
        )
        
        # 5.3 Career Recommendations (ranked by SBERT similarity)
        career_recommendations = self._build_career_recommendations(
            major_recommendations, career_similarities
        )
        
        # 5.4 Skill Gap Analysis
        skill_gaps = self._analyze_skill_gaps(
            major_recommendations, career_recommendations, 
            grades_lower, strengths
        )
        
        # ========================================
        # FINAL OUTPUT (STRICT FORMAT)
        # ========================================
        
        return {
            "major_recommendations": major_recommendations,
            "universities": universities,
            "career_recommendations": career_recommendations,
            "skill_gaps": skill_gaps,
            "match_percentage": match_percentage
        }
    
    def _expand_minimal_input(self, combined_text: str, career_goal: str, interests: str) -> str:
        """
        Expand short/vague inputs with related terms to improve SBERT matching
        """
        if not combined_text.strip():
            return ""
        
        # Expansion mappings for common short inputs
        expansions = {
            # Single word interests
            "health": "healthcare medical health hospital patient doctor medicine nursing",
            "medical": "medical doctor healthcare patient hospital medicine treatment surgery",
            "business": "business administration management finance marketing entrepreneur company corporate",
            "tech": "technology software engineering programming coding developer computer science",
            "computer": "computer science programming software developer coding technology apps applications",
            "code": "coding programming software engineering developer apps python javascript backend frontend algorithm technology computer science data science cybersecurity network security machine learning artificial intelligence database sql api systems",
            "coding": "coding programming software engineering developer apps python javascript backend frontend algorithm technology computer science data science cybersecurity network security machine learning artificial intelligence database sql api systems",
            "programming": "programming coding software engineering developer apps python javascript backend frontend algorithm technology computer science data science cybersecurity network machine learning artificial intelligence database systems",
            "software": "software engineering programming coding developer apps applications technology computer science backend frontend cybersecurity data science machine learning systems architecture",
            "law": "law legal lawyer justice court attorney advocate litigation",
            "design": "design creative visual graphics art user interface architecture",
            "art": "art creative design visual graphics illustration artistic",
            "science": "science research laboratory analysis chemistry physics biology scientific",
            "finance": "finance financial investment banking accounting money economics",
            "marketing": "marketing business advertising brand promotion sales digital marketing",
            "teaching": "teaching education teacher school classroom learning pedagogy",
            "engineering": "engineering software electrical mechanical civil chemical technical math physics",
            "medicine": "medicine medical doctor hospital patient healthcare surgery physician",
            "python": "python programming coding software engineering developer backend data science machine learning algorithm technology",
            "javascript": "javascript programming coding software engineering developer frontend web development technology",
            "developer": "software engineering developer programming coding apps applications technology computer science",
            "doctor": "medicine medical physician healthcare patient hospital surgery treatment anatomy",
            "lawyer": "law legal lawyer justice court attorney advocate litigation rights",
            "teacher": "education teaching teacher school classroom student learning pedagogy",
            "manager": "business administration business management leadership team organization corporate",
            "designer": "UX UI design creative visual graphics user interface prototype",
            "analyst": "data science analyst analysis data research business financial statistics",
            "nurse": "nursing healthcare patient medical hospital care treatment medicine",
            "accountant": "finance accounting financial numbers business economics investment",
        }
        
        text_lower = combined_text.lower().strip()
        expanded = combined_text
        
        # Check for matches and expand
        for keyword, expansion in expansions.items():
            if keyword in text_lower:
                expanded = f"{combined_text} {expansion}"
                break
        
        return expanded
    
    def _infer_majors_from_grades(self, grades: Dict[str, float]) -> Dict[str, float]:
        """
        Infer likely majors based on grade patterns when no text input is provided
        Returns boost factors for each inferred major
        """
        boosts = {}
        
        max_scores = {
            "math": 125, "physics": 75, "chemistry": 75, "biology": 75,
            "english": 50, "khmer": 75, "history": 50
        }
        
        # Normalize grades
        normalized = {}
        for subject, score in grades.items():
            max_score = max_scores.get(subject.lower(), 100)
            normalized[subject.lower()] = score / max_score
        
        # Find strong subjects (above 70%)
        strong_subjects = [s for s, n in normalized.items() if n >= 0.7]
        
        # Calculate combined scores
        math_physics = (normalized.get('math', 0) + normalized.get('physics', 0)) / 2
        bio_chem = (normalized.get('biology', 0) + normalized.get('chemistry', 0)) / 2
        humanities = (normalized.get('english', 0) + normalized.get('history', 0)) / 2
        
        # Apply boosts based on grade patterns
        if math_physics >= 0.75:
            # Strong STEM - boost engineering/tech majors
            boosts["Software Engineering"] = math_physics
            boosts["Electrical Engineering"] = math_physics * 0.95
            boosts["Mechanical Engineering"] = math_physics * 0.9
            boosts["Civil Engineering"] = math_physics * 0.85
            boosts["Data Science"] = math_physics * 0.9
            boosts["Cybersecurity"] = math_physics * 0.85
            boosts["Architecture"] = math_physics * 0.8
            
        if bio_chem >= 0.75:
            # Strong bio/chem - boost medical/science majors
            boosts["Medicine"] = bio_chem * 1.2
            boosts["Pharmacy"] = bio_chem * 1.1
            boosts["Dentistry"] = bio_chem
            boosts["Chemical Engineering"] = bio_chem * 0.9
            
        if normalized.get('math', 0) >= 0.7 and humanities >= 0.6:
            # Math + humanities - business/finance
            boosts["Business Administration"] = 0.8
            boosts["Business Management"] = 0.75
            boosts["Finance"] = 0.8
            
        if humanities >= 0.75:
            # Strong humanities
            boosts["Law"] = humanities * 0.7  # Less boost for humanities-only
            boosts["International Relations"] = humanities * 0.7
            boosts["Education"] = humanities * 0.7
            boosts["Psychology"] = humanities * 0.6
        
        return boosts
    
    def _build_major_recommendations(
        self,
        predictions: List[Dict]
    ) -> List[Dict]:
        """Build formatted major recommendations - only include majors with meaningful confidence"""
        recommendations = []
        
        for pred in predictions:
            # Skip majors with very low confidence (less than 5%)
            if pred['probability'] < 0.05:
                continue
                
            major_name = pred['major']
            major_info = self.majors_db.get(major_name, {})
            
            recommendations.append({
                "major": major_name,
                "confidence": round(pred['probability'], 4),
                "similarity_score": round(pred.get('similarity_score', 0), 3),
                "description": major_info.get('description', ''),
                "required_subjects": major_info.get('required_subjects', []),
                "career_paths": major_info.get('career_paths', []),
                "source": pred.get('source', 'ML-RandomForest')
            })
        
        return recommendations
    
    def _match_universities(
        self,
        major_recommendations: List[Dict],
        grades: Dict[str, float]
    ) -> List[Dict]:
        """Match universities to recommended majors, prioritizing top major and returning all matches"""
        universities = []
        
        # Calculate average grade
        avg_grade = sum(grades.values()) / len(grades) if grades else 0
        
        # Get top major (highest priority)
        top_major = major_recommendations[0]['major'] if major_recommendations else None
        
        # Get recommended majors with priority (top major = highest priority)
        major_priority = {}
        for i, m in enumerate(major_recommendations):
            major_name = m['major']
            major_priority[major_name] = len(major_recommendations) - i  # Higher = better
        
        desired_majors = set(major_priority.keys())
        
        # Collect all matching universities with scores
        all_matches = []
        
        for uni_name, uni_data in self.universities_db.items():
            # Check program availability
            programs = set(uni_data.get('programs', []))
            matching = desired_majors.intersection(programs)
            
            if not matching:
                continue
            
            # Check if university has the TOP major (highest priority)
            has_top_major = top_major in programs
            
            # Calculate match score based on which majors the uni offers
            # Higher score = matches higher-ranked major
            match_score = max(major_priority.get(m, 0) for m in matching)
            
            # Bonus for having top major
            if has_top_major:
                match_score += 100  # Ensure top major unis come first
            
            # Check eligibility
            min_grade = uni_data.get('requirements', {}).get('min_grade', 0)
            
            if avg_grade >= min_grade + 10:
                fit = "Safety"
                fit_score = 2
            elif avg_grade >= min_grade:
                fit = "Target"
                fit_score = 3  # Prefer Target
            else:
                fit = "Stretch"
                fit_score = 1
            
            all_matches.append({
                "name": uni_name,
                "location": uni_data.get('location', ''),
                "matching_programs": list(matching),
                "min_grade_required": min_grade,
                "fit": fit,
                "your_avg_grade": round(avg_grade, 1),
                "has_top_major": has_top_major,
                "_match_score": match_score,
                "_fit_score": fit_score
            })
        
        # Sort by: match_score (desc), then fit_score (desc)
        all_matches.sort(key=lambda x: (x['_match_score'], x['_fit_score']), reverse=True)
        
        # Return ALL universities that match, remove internal scores
        for uni in all_matches:
            del uni['_match_score']
            del uni['_fit_score']
            universities.append(uni)
        
        return universities
    
    def _build_career_recommendations(
        self,
        major_recommendations: List[Dict],
        career_similarities: Dict[str, float]
    ) -> List[Dict]:
        """Build career recommendations prioritizing top major's careers - only include meaningful matches"""
        careers = []
        seen = set()
        
        # Process majors in order - careers from top major get highest priority
        for major_idx, major_rec in enumerate(major_recommendations[:4]):
            career_paths = major_rec.get('career_paths', [])
            major_priority = len(major_recommendations) - major_idx  # Higher = better
            
            for career_name in career_paths:
                if career_name in seen:
                    continue
                
                career_info = self.careers_db.get(career_name, {})
                if not career_info:
                    continue
                
                similarity = career_similarities.get(career_name, 0.0)
                
                # Combined score: major_priority * 0.5 + similarity * 0.5
                combined_score = (major_priority / len(major_recommendations)) * 0.5 + similarity * 0.5
                
                careers.append({
                    "name": career_name,
                    "description": career_info.get('description', ''),
                    "required_skills": career_info.get('required_skills', []),
                    "avg_salary": career_info.get('avg_salary', 'Varies'),
                    "education_level": career_info.get('education_level', ''),
                    "related_major": major_rec['major'],
                    "similarity_score": round(similarity, 3),
                    "_combined_score": combined_score
                })
                
                seen.add(career_name)
        
        # Sort by combined score (prioritizes top major's careers)
        careers.sort(key=lambda x: x['_combined_score'], reverse=True)
        
        # Filter out careers with very low scores (less than 5%)
        # Keep minimum of 3 careers even if they're low
        filtered_careers = [c for c in careers if c['_combined_score'] >= 0.05]
        if len(filtered_careers) < 3 and len(careers) >= 3:
            filtered_careers = careers[:3]
        elif len(filtered_careers) < len(careers) and len(filtered_careers) < 3:
            filtered_careers = careers[:min(3, len(careers))]
        
        # Remove internal score and limit results
        for career in filtered_careers:
            del career['_combined_score']
        
        return filtered_careers[:10]
    
    def _analyze_skill_gaps(
        self,
        major_recommendations: List[Dict],
        career_recommendations: List[Dict],
        grades: Dict[str, float],
        strengths: str
    ) -> List[Dict]:
        """
        Analyze skill gaps with numeric current/goal levels for visualization.
        Only shows FUNDAMENTAL skills (not programming languages).
        - If student has experience: current_level <= required_level
        - If student wants to learn/fascinated: current_level is low
        """
        gaps = []
        
        if not major_recommendations:
            return gaps
        
        # Get top major info
        top_major = major_recommendations[0]
        major_name = top_major.get('major', '')
        major_info = self.majors_db.get(major_name, {})
        
        # Parse student strengths and interests
        strengths_lower = strengths.lower() if strengths else ""
        strength_keywords = set(word.lower().strip() for word in strengths.replace(',', ' ').split()) if strengths else set()
        
        # Detect "want to learn" or "fascinated" phrases (low experience)
        learning_phrases = ["want to learn", "interested in", "fascinated", "curious about", "new to", "beginner", "learning"]
        is_learning = any(phrase in strengths_lower for phrase in learning_phrases)
        
        # Detect "experience" or "skilled" phrases (has experience)
        experience_phrases = ["experience", "experienced", "skilled", "good at", "proficient", "know how", "familiar with"]
        has_experience = any(phrase in strengths_lower for phrase in experience_phrases)
        
        # Get grade-based skill indicators
        grade_skill_map = self._map_grades_to_skills(grades)
        
        # Skills to exclude (programming languages - not fundamental)
        excluded_keywords = {"python", "javascript", "java", "c++", "r ", " r", "/r", "r/", "sql", "html", "css", "react", "node", "photoshop", "illustrator", "figma", "autocad", "adobe", "git", "github"}
        
        def is_excluded_skill(skill: str) -> bool:
            """Check if skill name contains any programming language keywords"""
            skill_lower = skill.lower()
            # Check for exact match or keyword in skill name
            for kw in excluded_keywords:
                if kw in skill_lower:
                    return True
            return False
        
        # 1. Process fundamental skills from the major
        fundamental_skills = major_info.get('fundamental_skills', {})
        
        for skill_name, skill_info in fundamental_skills.items():
            # Skip programming language-specific skills
            if is_excluded_skill(skill_name):
                continue
            
            importance = skill_info.get('importance', 'medium')
            description = skill_info.get('description', '')
            
            # Calculate required level based on importance
            required_level = self._get_required_level(importance)
            
            # Estimate current level
            current_level = self._estimate_current_level_v2(
                skill_name, strength_keywords, grade_skill_map, grades,
                is_learning, has_experience, required_level
            )
            
            # Generate smart suggestions
            suggestions = self._generate_skill_suggestions(
                skill_name, current_level, required_level, major_name
            )
            
            gaps.append({
                "skill": skill_name,
                "current_level": round(current_level, 1),
                "required_level": round(required_level, 1),
                "importance": importance,
                "description": description,
                "suggestions": suggestions,
                "skill_type": "fundamental"
            })
        
        # 2. Add career-specific fundamental skills (not languages)
        top_careers = career_recommendations[:2] if career_recommendations else []
        existing_skills = {g['skill'].lower() for g in gaps}
        
        for career in top_careers:
            for skill in career.get('required_skills', [])[:3]:
                skill_lower = skill.lower()
                # Skip if already exists or is a programming language
                if skill_lower in existing_skills or is_excluded_skill(skill):
                    continue
                    
                current_level = self._estimate_current_level_v2(
                    skill, strength_keywords, grade_skill_map, grades,
                    is_learning, has_experience, 7.0
                )
                required_level = 7.0
                
                gaps.append({
                    "skill": skill,
                    "current_level": round(current_level, 1),
                    "required_level": round(required_level, 1),
                    "importance": "high",
                    "description": f"Required for {career.get('name', 'career')}",
                    "suggestions": self._generate_skill_suggestions(
                        skill, current_level, required_level, career.get('name', '')
                    ),
                    "skill_type": "career"
                })
                existing_skills.add(skill_lower)
        
        # Sort by gap size (biggest gaps first) then by importance
        importance_order = {"critical": 0, "high": 1, "medium": 2}
        gaps.sort(key=lambda x: (
            importance_order.get(x['importance'], 3),
            -(x['required_level'] - x['current_level'])
        ))
        
        # Return top 6 most relevant skills for clean visualization
        return gaps[:6]
    
    def _estimate_current_level_v2(
        self,
        skill_name: str,
        strength_keywords: set,
        grade_skill_map: Dict[str, float],
        grades: Dict[str, float],
        is_learning: bool,
        has_experience: bool,
        required_level: float
    ) -> float:
        """
        Estimate student's current skill level with smart logic:
        - If "want to learn" / "fascinated" → low level (2-4)
        - If "experience" → good level but NOT higher than required
        - Otherwise → estimate from grades
        """
        skill_lower = skill_name.lower()
        
        # Check if skill matches a strength keyword
        skill_mentioned = any(kw in skill_lower or skill_lower in kw for kw in strength_keywords)
        
        # Case 1: Student wants to learn this → low level
        if is_learning and skill_mentioned:
            return min(3.5, required_level - 3)  # Low but not zero
        
        # Case 2: Student wants to learn (general) → slightly low
        if is_learning:
            base_level = 3.0
            # Still use grades for base estimation
            for indicator, level in grade_skill_map.items():
                if indicator in skill_lower or skill_lower in indicator:
                    base_level = max(base_level, level * 0.6)  # 60% of grade estimate
                    break
            return min(base_level, required_level - 1)
        
        # Case 3: Student has experience in this skill → good but capped
        if has_experience and skill_mentioned:
            # Cap at required level (never exceed target)
            return min(required_level - 0.5, 7.5)
        
        # Case 4: Default - estimate from grades
        base_level = 3.0
        
        for indicator, level in grade_skill_map.items():
            if indicator in skill_lower or skill_lower in indicator:
                base_level = max(base_level, level)
                break
        
        # Infer from related keywords
        skill_grade_hints = {
            "math": ["mathematics", "calculus", "statistics", "quantitative", "analytics", "modeling"],
            "physics": ["mechanics", "thermodynamics", "electronics", "circuit", "signals"],
            "chemistry": ["chemical", "pharmaceutical", "lab"],
            "biology": ["anatomy", "patient", "medical", "health"],
            "english": ["communication", "writing", "presentation", "languages"],
        }
        
        for subject, keywords in skill_grade_hints.items():
            if any(kw in skill_lower for kw in keywords):
                max_scores = {"math": 125, "physics": 75, "chemistry": 75, "biology": 75, "english": 50}
                score = grades.get(subject, 0)
                max_score = max_scores.get(subject, 100)
                inferred_level = (score / max_score) * 10
                base_level = max(base_level, inferred_level * 0.8)
                break
        
        # CRITICAL: Current level should NEVER exceed required level
        # Cap at required_level - 0.5 to always show room for improvement
        capped_level = min(base_level, required_level - 0.5)
        
        # Clamp to valid range (minimum 1.0)
        return max(1.0, capped_level)
    
    def _map_grades_to_skills(self, grades: Dict[str, float]) -> Dict[str, float]:
        """Map academic grades to skill indicators (0-10 scale)"""
        max_scores = {
            "math": 125, "physics": 75, "chemistry": 75, "biology": 75,
            "english": 50, "khmer": 75, "history": 50
        }
        
        # Calculate normalized scores
        normalized = {}
        for subject, score in grades.items():
            max_score = max_scores.get(subject.lower(), 100)
            normalized[subject.lower()] = (score / max_score) * 10
        
        # Map to skill categories
        skill_indicators = {
            "mathematics": normalized.get('math', 5),
            "problem solving": normalized.get('math', 5) * 0.6 + normalized.get('physics', 5) * 0.4,
            "critical thinking": (normalized.get('math', 5) + normalized.get('english', 5)) / 2,
            "communication": normalized.get('english', 5) * 0.7 + normalized.get('khmer', 5) * 0.3,
            "writing": normalized.get('english', 5) * 0.6 + normalized.get('khmer', 5) * 0.4,
            "research skills": (normalized.get('english', 5) + normalized.get('history', 5)) / 2,
            "biology": normalized.get('biology', 5),
            "chemistry": normalized.get('chemistry', 5),
            "physics": normalized.get('physics', 5),
            "creativity": normalized.get('english', 5) * 0.5 + 5,
            "analytics": normalized.get('math', 5) * 0.8 + normalized.get('physics', 5) * 0.2,
        }
        
        return skill_indicators
    
    def _get_required_level(self, importance: str) -> float:
        """Get required level based on skill importance"""
        levels = {
            "critical": 8.5,
            "high": 7.0,
            "medium": 5.5
        }
        return levels.get(importance, 6.0)
    
    def _generate_skill_suggestions(
        self,
        skill_name: str,
        current_level: float,
        required_level: float,
        context: str
    ) -> List[str]:
        """Generate actionable suggestions based on skill gap"""
        gap = required_level - current_level
        suggestions = []
        
        if gap <= 1:
            suggestions.append(f"You're close! Practice {skill_name} regularly to reach mastery")
            suggestions.append(f"Take on challenging projects involving {skill_name}")
        elif gap <= 3:
            suggestions.append(f"Take online courses to strengthen your {skill_name}")
            suggestions.append(f"Join study groups or communities focused on {skill_name}")
            suggestions.append(f"Practice {skill_name} through hands-on projects")
        else:
            suggestions.append(f"Start with fundamentals of {skill_name} through structured learning")
            suggestions.append(f"Dedicate regular study time to develop {skill_name}")
            suggestions.append(f"Seek mentorship or tutoring in {skill_name}")
        
        return suggestions



