"""
Main API Router - Complete Recommendation Workflow
Uses NLP + ML + Rules pipeline
"""
from fastapi import APIRouter, HTTPException
from app.schemas.models import RecommendationRequest, RecommendationResponse, AnalyzeRequest, AnalyzeResponse
from core.recommendation_service import RecommendationService
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize service (singleton pattern inside class)
recommendation_service = RecommendationService()


@router.post("/recommend", response_model=RecommendationResponse)
async def get_recommendations(request: RecommendationRequest):
    """
    Complete recommendation endpoint
    
    Pipeline:
    1. NLTK preprocessing
    2. SBERT embeddings
    3. Rule-based filtering (before ML)
    4. Random Forest prediction
    5. Post-processing
    
    Returns:
    - major_recommendations
    - universities
    - career_recommendations
    - skill_gaps
    - match_percentage
    """
    try:
        # Parse grades
        grades = {g.subject.lower(): g.score for g in request.grades}
        
        # Get recommendations
        result = recommendation_service.get_recommendations(
            grades=grades,
            interests=request.interests or "",
            career_goal=request.career_goals or "",
            strengths=request.strengths or "",
            preferences=request.preferences or ""
        )
        
        return RecommendationResponse(
            major_recommendations=result["major_recommendations"],
            universities=result["universities"],
            career_recommendations=result["career_recommendations"],
            skill_gaps=result["skill_gaps"],
            match_percentage=result["match_percentage"]
        )
        
    except Exception as e:
        logger.error(f"Recommendation error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    """
    Frontend-compatible analyze endpoint
    
    Transforms internal recommendation format to frontend-expected format:
    - majors: [{name, score, description}]
    - careers: [{title, match_score, description}]
    - universities: [{name, country, programs}]
    - skill_gaps: [{skill, current_level, required_level, suggestions}]
    - subject_analysis: {subject: {score, normalized, strength}}
    """
    try:
        # Parse grades
        grades = {g.subject.lower(): g.score for g in request.grades}
        
        # Get recommendations
        result = recommendation_service.get_recommendations(
            grades=grades,
            interests=request.interest_text or "",
            career_goal=request.career_goals or "",
            strengths=request.strengths or "",
            preferences=request.preferences or ""
        )
        
        # Transform majors
        majors = [
            {
                "name": m["major"],
                "score": m["confidence"],
                "description": m["description"],
                "source": m.get("source", "ML-RandomForest")
            }
            for m in result["major_recommendations"]
        ]
        
        # Transform careers
        careers = [
            {
                "title": c["name"],
                "match_score": c.get("similarity_score", 0.5),
                "description": c["description"]
            }
            for c in result["career_recommendations"]
        ]
        
        # Transform universities
        universities = [
            {
                "name": u["name"],
                "country": u["location"],
                "programs": u["matching_programs"],
                "fit": u.get("fit", "")
            }
            for u in result["universities"]
        ]
        
        # Transform skill gaps (already in correct format)
        skill_gaps = [
            {
                "skill": s["skill"],
                "current_level": s["current_level"],
                "required_level": s["required_level"],
                "suggestions": s.get("suggestions", [])
            }
            for s in result["skill_gaps"]
        ]
        
        # Build subject analysis
        max_scores = {
            "math": 125, "physics": 75, "chemistry": 75, "biology": 75,
            "english": 50, "khmer": 75, "history": 50
        }
        
        subject_analysis = {}
        for subject, score in grades.items():
            max_score = max_scores.get(subject.lower(), 100)
            normalized = (score / max_score) * 100
            
            if normalized >= 80:
                strength = "Excellent"
            elif normalized >= 65:
                strength = "Good"
            elif normalized >= 50:
                strength = "Average"
            else:
                strength = "Needs Improvement"
            
            subject_analysis[subject] = {
                "score": score,
                "normalized": round(normalized, 1),
                "strength": strength
            }
        
        return AnalyzeResponse(
            majors=majors,
            careers=careers,
            universities=universities,
            skill_gaps=skill_gaps,
            subject_analysis=subject_analysis
        )
        
    except Exception as e:
        logger.error(f"Analyze error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
