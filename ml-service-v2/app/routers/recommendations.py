"""
Main API Router - Analyze Endpoint
Uses NLP + ML pipeline
"""
from fastapi import APIRouter, HTTPException
from app.schemas.models import AnalyzeRequest, AnalyzeResponse
from core.recommendation_service import RecommendationService
import logging
import uuid

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize service (singleton pattern inside class)
recommendation_service = RecommendationService()


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
                "match_score": c.get("match_score", 0.5),
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
        
        # Build subject analysis — max scores from the shared constant
        from core.feature_builder import MAX_SCORES as _MAX_SCORES
        
        subject_analysis = {}
        norm_scores = []
        for subject, score in grades.items():
            max_score = _MAX_SCORES.get(subject.lower(), 100)
            normalized = (score / max_score) * 100 if max_score > 0 else 0
            norm_scores.append(normalized)
            subject_analysis[subject] = {
                "score": score,
                "normalized": round(normalized, 1),
                "strength": ""  # filled below
            }
        
        # Assign strength labels based on distribution (percentile-aware)
        import numpy as np
        if norm_scores:
            mean_n = float(np.mean(norm_scores))
            std_n = float(np.std(norm_scores)) if len(norm_scores) > 1 else 10.0
            for subject in subject_analysis:
                n = subject_analysis[subject]["normalized"]
                if n >= mean_n + std_n:
                    subject_analysis[subject]["strength"] = "Excellent"
                elif n >= mean_n:
                    subject_analysis[subject]["strength"] = "Good"
                elif n >= mean_n - std_n:
                    subject_analysis[subject]["strength"] = "Average"
                else:
                    subject_analysis[subject]["strength"] = "Needs Improvement"
        
        return AnalyzeResponse(
            majors=majors,
            careers=careers,
            universities=universities,
            skill_gaps=skill_gaps,
            subject_analysis=subject_analysis
        )
        
    except Exception as e:
        error_id = str(uuid.uuid4())[:8]
        logger.error(f"Analyze error (ref: {error_id}): {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error - reference {error_id}")
