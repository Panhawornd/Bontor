"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel
from typing import List, Dict, Any

class Grade(BaseModel):
    subject: str
    score: float  # accepts 0-100 or will try to interpret letters

class AnalyzeRequest(BaseModel):
    grades: List[Grade]
    interest_text: str
    career_goals: str | None = None

class Recommendation(BaseModel):
    majors: List[Dict[str, Any]]
    careers: List[Dict[str, Any]]
    universities: List[Dict[str, Any]]
    skill_gaps: List[Dict[str, Any]]
    subject_analysis: Dict[str, Dict[str, Any]]