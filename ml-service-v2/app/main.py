"""
FastAPI Main Application
NLP + ML Recommendation System

Pipeline:
1. NLTK preprocessing
2. SBERT embeddings (all-MiniLM-L6-v2)
3. Rule-based filtering (BEFORE ML)
4. Random Forest prediction (with StandardScaler)
5. Post-processing + Monitoring

Security:
- API Key authentication (X-API-Key header)
- Restricted CORS (only allowed origins)
- Rate limiting (per-IP)
- Bound to 127.0.0.1 by default (localhost only)
"""
import os
import time
import logging
from collections import defaultdict
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from app.routers import recommendations
from ml.predict import MLPredictor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================
# Load environment variables
# ============================================
def _load_env():
    """Load .env file manually (no extra dependency needed)"""
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, value = line.partition("=")
                    os.environ.setdefault(key.strip(), value.strip())

_load_env()

API_KEY = os.environ.get("ML_API_KEY", "capstone-ml-secret-key-2026")
ALLOWED_ORIGINS = os.environ.get(
    "ALLOWED_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000"
).split(",")
HOST = os.environ.get("HOST", "127.0.0.1")
PORT = int(os.environ.get("PORT", "8000"))


# ============================================
# Security Middleware: API Key Authentication
# ============================================
class APIKeyMiddleware(BaseHTTPMiddleware):
    """
    Verifies that every request (except public endpoints) includes
    a valid API key in the X-API-Key header.
    
    Public endpoints (no key needed):
    - GET /           (service info)
    - GET /health     (health check)
    - GET /docs       (Swagger docs)
    - GET /openapi.json
    """
    PUBLIC_PATHS = {"/", "/health", "/docs", "/openapi.json", "/redoc"}

    async def dispatch(self, request: Request, call_next):
        # Allow public endpoints without API key
        if request.url.path in self.PUBLIC_PATHS:
            return await call_next(request)

        # Allow OPTIONS requests (CORS preflight)
        if request.method == "OPTIONS":
            return await call_next(request)

        # Check API key
        api_key = request.headers.get("X-API-Key")
        if api_key != API_KEY:
            logger.warning(
                f"Unauthorized request to {request.url.path} "
                f"from {request.client.host if request.client else 'unknown'}"
            )
            raise HTTPException(
                status_code=403,
                detail="Invalid or missing API key"
            )

        return await call_next(request)


# ============================================
# Security Middleware: Rate Limiting
# ============================================
class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Simple in-memory rate limiter.
    Limits each IP to a maximum number of requests per time window.
    
    Default: 30 requests per 60 seconds per IP.
    """
    def __init__(self, app, max_requests: int = 30, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)  # {ip: [timestamp, timestamp, ...]}

    async def dispatch(self, request: Request, call_next):
        # Skip rate limiting for health checks
        if request.url.path in {"/", "/health", "/docs", "/openapi.json"}:
            return await call_next(request)

        client_ip = request.client.host if request.client else "unknown"
        now = time.time()

        # Clean old timestamps outside the window
        self.requests[client_ip] = [
            t for t in self.requests[client_ip]
            if now - t < self.window_seconds
        ]

        # Check rate limit
        if len(self.requests[client_ip]) >= self.max_requests:
            logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            raise HTTPException(
                status_code=429,
                detail="Too many requests. Please try again later."
            )

        # Record this request
        self.requests[client_ip].append(now)

        return await call_next(request)


# ============================================
# Create FastAPI App
# ============================================
app = FastAPI(
    title="Grade Analysis ML Service",
    description="NLP + ML powered educational recommendation system using NLTK, SBERT, and Random Forest",
    version="3.2.0"
)

# ============================================
# Apply Security Middlewares (order matters!)
# Middlewares execute in REVERSE order of adding:
# 1. CORS (outermost - handles preflight first)
# 2. Rate Limiting (before auth - block spammers early)
# 3. API Key Auth (innermost - only reached if not rate limited)
# ============================================

# 3. API Key Authentication (applied last = runs first after CORS)
app.add_middleware(APIKeyMiddleware)

# 2. Rate Limiting: 30 requests per 60 seconds per IP
app.add_middleware(RateLimitMiddleware, max_requests=30, window_seconds=60)

# 1. CORS - Restricted to allowed origins only
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "X-API-Key"],
)

# Include routers
app.include_router(recommendations.router, prefix="/api", tags=["Analyze"])


# ============================================
# Public Endpoints (no API key required)
# ============================================

@app.get("/")
async def root():
    return {
        "service": "Grade Analysis ML Service",
        "version": "3.2.0",
        "status": "operational",
        "security": "API key required for /api/* endpoints",
        "pipeline": [
            "NLTK preprocessing",
            "SBERT embeddings (all-MiniLM-L6-v2)",
            "Rule-based eligibility filtering",
            "Feature scaling (StandardScaler)",
            "Random Forest prediction",
            "Confidence monitoring",
            "Post-processing"
        ],
        "endpoints": ["/api/analyze", "/health", "/metrics"]
    }


@app.get("/health")
async def health():
    """Health check with model status."""
    predictor = MLPredictor()
    return {
        "status": "healthy" if predictor.model is not None else "degraded",
        "version": "3.2.0",
        "model_loaded": predictor.model is not None,
        "scaler_loaded": predictor.scaler is not None,
        "training_meta": {
            "accuracy": predictor.training_meta.get("test_accuracy") if predictor.training_meta else None,
            "cv_accuracy": predictor.training_meta.get("cv_accuracy_mean") if predictor.training_meta else None,
        } if predictor.training_meta else None,
    }


@app.get("/metrics")
async def metrics(request: Request):
    """Prediction monitoring metrics endpoint (requires API key)."""
    predictor = MLPredictor()
    return predictor.get_monitor_metrics()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=HOST,
        port=PORT,
        reload=True
    )
