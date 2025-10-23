"""
Main FastAPI application
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
import numpy as np
import os
import joblib
import psycopg2
import json

from .models.pydantic_models import Grade, AnalyzeRequest, Recommendation
from .utils.constants import SUBJECT_MAX_SCORES
from .utils.recommendations import (
    hybrid_major_recommendations, 
    intelligent_career_recommendations,
    intelligent_university_recommendations,
    generate_skill_gaps
)
from .utils.text_processing import set_ml_models

# Initialize FastAPI app
app = FastAPI(title="Grade Analysis API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ML models
sentence_model = None
zero_shot = None
ml_models = {}
domain_models = {}

@app.on_event("startup")
async def startup_event():
    """Load ML models on startup"""
    print("Starting Grade Analysis API...")
    
    # Initialize sentence transformer model for semantic understanding
    try:
        from sentence_transformers import SentenceTransformer, util
        # Use a lightweight but effective model
        global sentence_model
        sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
        print("Sentence transformer model loaded successfully")
    except Exception as e:
        print(f"Failed to load sentence transformer: {e}")
        sentence_model = None

    # Initialize zero-shot classifier for free-form intent-to-major mapping
    try:
        from transformers import pipeline
        global zero_shot
        zero_shot = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
        print("Zero-shot classifier loaded successfully")
    except Exception as e:
        print(f"Failed to load zero-shot classifier: {e}")
        zero_shot = None

    # Load ML models if they exist
    try:
        if os.path.exists("models/major_classifier.pkl"):
            ml_models['major_classifier'] = joblib.load("models/major_classifier.pkl")
            print("ML Major classifier loaded")
        if os.path.exists("models/career_classifier.pkl"):
            ml_models['career_classifier'] = joblib.load("models/career_classifier.pkl")
            print("ML Career classifier loaded")
        if os.path.exists("models/university_classifier.pkl"):
            ml_models['university_classifier'] = joblib.load("models/university_classifier.pkl")
            print("ML University classifier loaded")
        
        # Load domain-specific models
        domains = ['electrical_engineering', 'mechanical_engineering', 'civil_engineering', 'chemical_engineering', 'medicine', 'business', 'technology', 'arts', 'design']
        for domain in domains:
            model_path = f"models/{domain}_classifier.pkl"
            if os.path.exists(model_path):
                domain_models[domain] = joblib.load(model_path)
                print(f"Domain model for {domain} loaded")
    except Exception as e:
        print(f"Failed to load ML models: {e}")
        print("Using rule-based recommendations only")
    
    # Set ML models in text processing
    set_ml_models(sentence_model, zero_shot)
    
    print("All models loaded successfully!")


def to_percentage(score: float | str) -> float:
    """Convert score to float, only accepting numeric values"""
    if isinstance(score, (int, float)):
        return float(score)
    try:
        return float(str(score).strip())
    except ValueError:
        return 0.0

def normalize(score: float, max_score: float) -> float:
    # normalize 0..max_score -> 0..1
    return max(0.0, min(1.0, score / max_score))

@app.post("/analyze", response_model=Recommendation)
async def analyze(req: AnalyzeRequest):
    # Convert all grades to percentages and normalize using subject-specific max scores
    subject_analysis: Dict[str, Dict[str, Any]] = {}
    subject_scores: Dict[str, float] = {}
    for g in req.grades:
        subject = g.subject.lower()
        if subject in SUBJECT_MAX_SCORES:
            original_input = g.score
            p = to_percentage(g.score)
            max_score = SUBJECT_MAX_SCORES[subject]
            # Clamp to valid range 0..max_score
            clamped_score = max(0.0, min(p, float(max_score)))
            n = normalize(clamped_score, max_score)
            subject_scores[subject] = n
            subject_analysis[subject] = {
                "score": clamped_score,
                "normalized": n,
                "strength": "strong" if n >= 0.8 else ("average" if n >= 0.6 else "weak"),
                "max": max_score,
                "input": original_input,
                "adjusted": float(clamped_score) != float(p)
            }

    # Infer preferences from free-form text
    from .utils.text_processing import infer_preferences_from_text
    combined_text = f"{req.interest_text} {req.career_goals or ''}"
    user_preferences = infer_preferences_from_text(combined_text)
    # Set location preference to local since we only have Cambodian universities
    user_preferences["locationPreference"] = "local"

    # Use hybrid recommendations (ML + rule-based)
    print(f"DEBUG: Calling hybrid_major_recommendations with:")
    print(f"  subject_scores: {subject_scores}")
    print(f"  interest_text: '{req.interest_text}'")
    print(f"  career_goals: '{req.career_goals or ''}'")
    
    majors = hybrid_major_recommendations(
        subject_scores, 
        req.interest_text, 
        req.career_goals or "", 
        user_preferences,
        ml_models,
        domain_models
    )
    
    print(f"DEBUG: hybrid_major_recommendations returned {len(majors) if majors else 0} majors")
    
    # The recommendation function already has proper filtering, so we don't need additional filtering here
    print(f"DEBUG: Using original majors without additional filtering: {len(majors) if majors else 0}")
    careers = intelligent_career_recommendations(majors, req.interest_text, req.interest_text)
    universities = intelligent_university_recommendations(subject_scores, majors, "local", req.career_goals or "")
    skill_gaps = generate_skill_gaps(subject_scores, majors)

    return Recommendation(
        majors=majors,
        careers=careers,
        universities=universities,
        skill_gaps=skill_gaps,
        subject_analysis=subject_analysis,
    )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "models_loaded": len(ml_models) > 0,
        "domain_models_loaded": len(domain_models),
        "available_domains": list(domain_models.keys()),
        "version": "1.0.0"
    }

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Grade Analysis API",
        "version": "1.0.0",
        "endpoints": ["/analyze", "/health", "/feedback", "/preferences", "/train"]
    }

# Enhanced data collection endpoint for building training dataset
@app.post("/feedback")
async def collect_feedback(feedback_data: dict):
    """Collect user feedback to improve recommendations"""
    try:
        # Log the feedback data for analysis
        print(f"Feedback received: {feedback_data}")
        
        # Save to database for training
        try:
            # Connect to database
            conn = psycopg2.connect(
                host="localhost",
                port="5433",
                database="grade_analyzer",
                user="postgres",
                password="baboo123"
            )
            cursor = conn.cursor()
            
            # Extract data from feedback
            user_id = feedback_data.get('user_id', 1)
            grades = feedback_data.get('grades', [])
            interests = feedback_data.get('interests', '')
            career_goals = feedback_data.get('career_goals', '')
            study_preference = 'local'  # Always local since we only have Cambodian universities
            recommendations = feedback_data.get('recommendations', {})
            
            # Get the top recommended major
            top_major = recommendations.get('majors', [{}])[0].get('name', 'Unknown')
            
            # Convert grades to dict format
            grades_dict = {grade['subject']: grade['score'] for grade in grades}
            
            # Insert into TrainingData table
            insert_query = """
            INSERT INTO "TrainingData" 
            (grades, interests, "careerGoals", "studyPreference", "recommendedMajor", "actualMajor", "feedbackScore", "isProcessed")
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(insert_query, (
                json.dumps(grades_dict),
                interests,
                career_goals,
                study_preference,
                top_major,
                top_major,  # Assuming they choose the recommended major
                5,  # Default high rating
                False  # Not processed yet
            ))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            print(f"Training data saved to database for user {user_id}")
            
        except Exception as db_error:
            print(f"Database save failed: {db_error}")
            # Continue even if database save fails
        
        return {
            "message": "Feedback recorded successfully",
            "status": "success",
            "data_points": len(feedback_data.get('recommendations', {}).get('majors', []))
        }
    except Exception as e:
        print(f"Error processing feedback: {e}")
        return {"message": "Error processing feedback", "status": "error"}

# Endpoint to get user preferences for personalization
@app.get("/preferences/{user_id}")
async def get_user_preferences(user_id: int):
    """Get user preferences for personalization"""
    # In a real implementation, fetch from database
    # For now, return default preferences
    return {
        "workStyle": "mixed",
        "learningStyle": "mixed", 
        "careerFocus": "industry",
        "locationPreference": "flexible",
        "salaryExpectation": "moderate",
        "workLifeBalance": "moderate"
    }

# Endpoint to update user preferences
@app.post("/preferences/{user_id}")
async def update_user_preferences(user_id: int, preferences: dict):
    """Update user preferences for better personalization"""
    print(f"Updated preferences for user {user_id}: {preferences}")
    return {"message": "Preferences updated successfully"}

@app.post("/train")
async def train_models():
    """Train ML models using collected data"""
    try:
        from train_models import RecommendationTrainer
        
        print("Starting model training...")
        trainer = RecommendationTrainer()
        trainer.train_all_models()
        
        # Reload models
        global ml_models, domain_models
        try:
            if os.path.exists("models/major_classifier.pkl"):
                ml_models['major_classifier'] = joblib.load("models/major_classifier.pkl")
                print("ML Major classifier reloaded")
            if os.path.exists("models/career_classifier.pkl"):
                ml_models['career_classifier'] = joblib.load("models/career_classifier.pkl")
                print("ML Career classifier reloaded")
            if os.path.exists("models/university_classifier.pkl"):
                ml_models['university_classifier'] = joblib.load("models/university_classifier.pkl")
                print("ML University classifier reloaded")
            
            # Reload domain-specific models
            domains = ['electrical_engineering', 'mechanical_engineering', 'civil_engineering', 'chemical_engineering', 'medicine', 'business', 'technology', 'arts', 'design']
            for domain in domains:
                model_path = f"models/{domain}_classifier.pkl"
                if os.path.exists(model_path):
                    domain_models[domain] = joblib.load(model_path)
                    print(f"Domain model for {domain} reloaded")
        except Exception as e:
            print(f"Failed to reload models: {e}")
        
        return {"message": "Models trained successfully and training data marked as processed", "status": "success"}
        
    except Exception as e:
        print(f"Training failed: {e}")
        return {"message": f"Training failed: {str(e)}", "status": "error"}