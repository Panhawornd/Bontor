"""
Main API Router - Complete recommendation workflow
"""
from fastapi import APIRouter, HTTPException
from app.schemas.models import RecommendationRequest, RecommendationResponse
from core.nlp import NLPService
from core.features import FeatureEngine
from core.ml_engine import MLEngine
from core.rules import RuleEngine
from core.career_mapper import CareerMapper
from core.university_mapper import UniversityMapper
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize services (singleton pattern ensures single load)
nlp_service = NLPService()
feature_engine = FeatureEngine()
ml_engine = MLEngine()
rule_engine = RuleEngine()
career_mapper = CareerMapper()
university_mapper = UniversityMapper()

@router.post("/recommend", response_model=RecommendationResponse)
async def get_recommendations(request: RecommendationRequest):
    """
    Complete recommendation workflow
    """
    try:
        # Parse user input
        grades = {g.subject.lower(): g.score for g in request.grades}
        interests = request.interests
        career_goals = request.career_goals or ""
        
        # Feature engineering
        features = feature_engine.build_features(grades, interests, career_goals)
        
        # ML prediction
        ml_predictions = ml_engine.predict(features)
        
        # Rule-based filtering
        filtered_majors = rule_engine.apply_rules(ml_predictions, grades, interests)
        
        # Career and skill mapping
        careers = career_mapper.map_careers(filtered_majors)
        skill_gaps = career_mapper.identify_skill_gaps(careers, grades)
        
        # University matching
        universities = university_mapper.map_universities(filtered_majors, grades)
        
        return RecommendationResponse(
            majors=filtered_majors,
            careers=careers,
            universities=universities,
            skill_gaps=skill_gaps
        )
        
    except Exception as e:
        logger.error(f"Recommendation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
