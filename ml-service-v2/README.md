# Grade Analysis ML Service v2

## ✅ Clean, Professional ML Service

### 🎯 7-Step Workflow

1. **User Input** → Student grades & interests
2. **NLP Processing** → Sentence Transformer + Zero-Shot
3. **Feature Engineering** → Combines all features
4. **ML Prediction** → Random Forest classifier
5. **Rule-Based Filtering** → Validates results
6. **Career Mapping** → Skills & career recommendations
7. **Final Output** → Complete recommendations

### 📁 Structure

```
ml-service-v2/
├── app/main.py              # FastAPI entry
├── app/routers/             # API endpoints
├── core/                    # 6 clean modules (Steps 2-6)
├── data/                    # Databases
└── models/                  # ML models
```

### 🚀 Quick Start

```bash
cd ml-service-v2
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 📌 API

**POST /api/recommend**

- Input: grades, interests, career_goals
- Output: majors, careers, skill_gaps, processing_steps

### ✨ Features

- Clean code (each module <100 lines)
- Type hints throughout
- Comprehensive logging
- Production-ready
