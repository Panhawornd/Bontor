"""
Pydantic models for API requests and responses
Output format matches requirements STRICTLY
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Optional


# ========================================
# INPUT MODELS
# ========================================

class GradeInput(BaseModel):
    """Single subject grade input"""
    subject: str
    score: float


class RecommendationRequest(BaseModel):
    """
    Complete recommendation request
    
    Required:
    - grades: All 7 subject scores
    
    Optional:
    - interests: Student interests
    - career_goals: Career goal text
    - strengths: logic, communication, creativity, problem-solving
    - preferences: coding, analysis, design, networking
    """
    grades: List[GradeInput]
    interests: str = ""
    career_goals: Optional[str] = ""
    strengths: Optional[str] = ""
    preferences: Optional[str] = ""


# ========================================
# OUTPUT MODELS
# ========================================

class MajorRecommendation(BaseModel):
    """Single major recommendation"""
    major: str
    confidence: float = Field(..., description="Probability/confidence score")
    similarity_score: float = Field(0.0, description="SBERT similarity score")
    description: str
    required_subjects: List[str]
    career_paths: List[str]
    source: str = "ML-RandomForest"


class UniversityRecommendation(BaseModel):
    """University matching result"""
    name: str
    location: str
    matching_programs: List[str]
    min_grade_required: float
    fit: str  # "Target", "Safety", or "Stretch"
    your_avg_grade: float


class CareerRecommendation(BaseModel):
    """Career recommendation with skills"""
    name: str
    description: str
    required_skills: List[str]
    avg_salary: str
    education_level: str = ""
    related_major: str
    similarity_score: float = 0.0


class SkillGap(BaseModel):
    """Skill gap analysis result with numeric levels for visualization"""
    skill: str
    current_level: float = Field(..., description="Current skill level 0-10")
    required_level: float = Field(..., description="Required skill level 0-10")
    importance: str  # "critical", "high", "medium"
    description: str = ""
    suggestions: List[str] = []
    skill_type: str = "fundamental"  # "fundamental", "career", "academic"


class RecommendationResponse(BaseModel):
    """
    FINAL OUTPUT FORMAT (STRICT)
    
    Returns ONLY:
    - major_recommendations
    - universities
    - career_recommendations
    - skill_gaps
    - match_percentage
    """
    major_recommendations: List[MajorRecommendation]
    universities: List[UniversityRecommendation]
    career_recommendations: List[CareerRecommendation]
    skill_gaps: List[SkillGap]
    match_percentage: float = Field(..., description="Overall match percentage (0-100)")


# ========================================
# ANALYZE ENDPOINT MODELS (Frontend Compatible)
# ========================================

class AnalyzeRequest(BaseModel):
    """Frontend-compatible analyze request"""
    grades: List[GradeInput]
    interest_text: str = ""
    career_goals: Optional[str] = ""
    strengths: Optional[str] = ""
    preferences: Optional[str] = ""


class AnalyzeMajor(BaseModel):
    """Major format for frontend"""
    name: str
    score: float
    description: str
    source: str = "ML-RandomForest"


class AnalyzeCareer(BaseModel):
    """Career format for frontend"""
    title: str
    match_score: float
    description: str


class AnalyzeUniversity(BaseModel):
    """University format for frontend"""
    name: str
    country: str
    programs: List[str]
    fit: str = ""


class AnalyzeSkillGap(BaseModel):
    """Skill gap format for frontend visualization"""
    skill: str
    current_level: float
    required_level: float
    suggestions: List[str] = []


class SubjectAnalysis(BaseModel):
    """Subject analysis for frontend"""
    score: float
    normalized: float
    strength: str


class AnalyzeResponse(BaseModel):
    """Frontend-compatible analyze response"""
    majors: List[AnalyzeMajor]
    careers: List[AnalyzeCareer]
    universities: List[AnalyzeUniversity]
    skill_gaps: List[AnalyzeSkillGap]
    subject_analysis: Dict[str, SubjectAnalysis]
