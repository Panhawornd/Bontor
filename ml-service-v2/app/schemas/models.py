"""Pydantic models for API requests and responses"""
from pydantic import BaseModel
from typing import List, Dict, Optional

class GradeInput(BaseModel):
    subject: str
    score: float

class RecommendationRequest(BaseModel):
    grades: List[GradeInput]
    interests: str
    career_goals: Optional[str] = ""

class MajorRecommendation(BaseModel):
    major: str
    probability: float
    description: str
    required_subjects: List[str]
    career_paths: List[str]
    source: str

class CareerRecommendation(BaseModel):
    name: str
    description: str
    required_skills: List[str]
    avg_salary: str
    related_major: str

class SkillGap(BaseModel):
    skill: str
    current_level: str
    importance: str
    suggestions: List[str]

class UniversityRecommendation(BaseModel):
    name: str
    location: str
    matching_programs: List[str]
    min_grade_required: float
    fit: str
    your_avg_grade: float

class RecommendationResponse(BaseModel):
    majors: List[MajorRecommendation]
    careers: List[CareerRecommendation]
    universities: List[UniversityRecommendation]
    skill_gaps: List[SkillGap]
