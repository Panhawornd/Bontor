"""
FastAPI Main Application
NLP + ML Recommendation System

Pipeline:
1. NLTK preprocessing
2. SBERT embeddings (all-MiniLM-L6-v2)
3. Rule-based filtering (BEFORE ML)
4. Random Forest prediction
5. Post-processing
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import recommendations
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create app
app = FastAPI(
    title="Grade Analysis ML Service",
    description="NLP + ML powered educational recommendation system using NLTK, SBERT, and Random Forest",
    version="3.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(recommendations.router, prefix="/api", tags=["Recommendations"])


@app.get("/")
async def root():
    return {
        "service": "Grade Analysis ML Service",
        "version": "3.0.0",
        "status": "operational",
        "pipeline": [
            "NLTK preprocessing",
            "SBERT embeddings (all-MiniLM-L6-v2)",
            "Rule-based eligibility filtering",
            "Random Forest prediction",
            "Post-processing"
        ],
        "endpoints": ["/api/recommend", "/api/analyze", "/health"]
    }


@app.get("/health")
async def health():
    return {"status": "healthy", "version": "3.0.0"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
