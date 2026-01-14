"""
FastAPI Main Application
Clean, minimal entry point
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
    description="ML-powered educational recommendation system",
    version="2.0.0"
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
        "version": "2.0.0",
        "status": "operational",
        "endpoints": ["/api/recommend", "/health"]
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "version": "2.0.0"}
