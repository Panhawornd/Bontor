"""
FastAPI Main Application
NLP + ML Recommendation System

Pipeline:
1. NLTK preprocessing
2. SBERT embeddings (all-MiniLM-L6-v2)
3. Rule-based filtering (BEFORE ML)
4. Random Forest prediction (with StandardScaler)
5. Post-processing + Monitoring
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import recommendations
from ml.predict import MLPredictor
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
    version="3.1.0"
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
        "version": "3.1.0",
        "status": "operational",
        "pipeline": [
            "NLTK preprocessing",
            "SBERT embeddings (all-MiniLM-L6-v2)",
            "Rule-based eligibility filtering",
            "Feature scaling (StandardScaler)",
            "Random Forest prediction",
            "Confidence monitoring",
            "Post-processing"
        ],
        "endpoints": ["/api/recommend", "/api/analyze", "/health", "/metrics"]
    }


@app.get("/health")
async def health():
    """Health check with model status."""
    predictor = MLPredictor()
    return {
        "status": "healthy" if predictor.model is not None else "degraded",
        "version": "3.1.0",
        "model_loaded": predictor.model is not None,
        "scaler_loaded": predictor.scaler is not None,
        "training_meta": {
            "accuracy": predictor.training_meta.get("test_accuracy") if predictor.training_meta else None,
            "cv_accuracy": predictor.training_meta.get("cv_accuracy_mean") if predictor.training_meta else None,
        } if predictor.training_meta else None,
    }


@app.get("/metrics")
async def metrics():
    """Prediction monitoring metrics endpoint."""
    predictor = MLPredictor()
    return predictor.get_monitor_metrics()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
