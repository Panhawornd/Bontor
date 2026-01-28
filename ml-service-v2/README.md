# ML Service v3.0 - NLP + ML Recommendation System

An intelligent educational recommendation system using **NLTK** for text preprocessing, **SBERT** for semantic embeddings, and **Random Forest** for major prediction.

## 🏗️ Architecture

```
backend/
├── nlp/                    # NLP Pipeline
│   ├── preprocess.py      # NLTK text cleaning
│   ├── sbert.py           # SBERT encoder (all-MiniLM-L6-v2)
│   └── similarity.py      # Cosine similarity computation
├── ml/                     # Machine Learning
│   ├── train_rf.py        # Random Forest training
│   ├── predict.py         # Prediction engine
│   └── models/            # Saved models
├── rules/                  # Rule-Based Filtering
│   └── eligibility.py     # Subject-aware rules
├── data/                   # Data Sources
│   ├── majors.py/json     # Major database
│   ├── careers.py/json    # Career database
│   └── universities.py/json # University database
├── core/                   # Core Logic
│   ├── feature_builder.py # Feature engineering
│   └── recommendation_service.py # Main service
└── app/                    # FastAPI Application
    ├── main.py            # Entry point
    ├── routers/           # API routes
    └── schemas/           # Pydantic models
```

## 🔧 Pipeline Flow

1. **INPUT FEATURES**
   - Academic Subjects: Math, Physics, Chemistry, Biology, Khmer, English, History
   - Student Attributes: Strengths, Preferences, Career Goals

2. **NLP PIPELINE**
   - NLTK preprocessing (lowercase, tokenize, stopwords, lemmatize)
   - SBERT encoding (all-MiniLM-L6-v2 - NOT retrained)
   - Cosine similarity scores

3. **RULE-BASED FILTERING (BEFORE ML)**
   - Math < threshold → exclude Engineering/CS
   - Khmer < threshold → penalize social sciences
   - History < threshold → penalize humanities
   - English < threshold → exclude international programs

4. **MACHINE LEARNING**
   - Random Forest Classifier
   - Probability per major
   - Ranked major list

5. **POST-PROCESSING**
   - Major recommendations (top-N)
   - University matching
   - Career recommendations (SBERT ranked)
   - Skill gap analysis

## 📦 Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"

# Train the model
python train_model.py

# Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 🚀 API Usage

### POST /api/recommend

**Request:**

```json
{
  "grades": [
    { "subject": "math", "score": 100 },
    { "subject": "physics", "score": 65 },
    { "subject": "chemistry", "score": 60 },
    { "subject": "biology", "score": 55 },
    { "subject": "english", "score": 40 },
    { "subject": "khmer", "score": 60 },
    { "subject": "history", "score": 35 }
  ],
  "interests": "I like coding and building software applications",
  "career_goals": "I want to become a software engineer",
  "strengths": "logic, problem-solving",
  "preferences": "coding, analysis"
}
```

**Response:**

```json
{
  "major_recommendations": [...],
  "universities": [...],
  "career_recommendations": [...],
  "skill_gaps": [...],
  "match_percentage": 85.5
}
```

## ⚠️ Hard Constraints

- **SBERT Model**: `all-MiniLM-L6-v2` (DO NOT retrain)
- **NLTK runs BEFORE SBERT**
- **Rules OVERRIDE ML**
- **ML only sees numbers**
- **Output ONLY recommendation results**

## 📊 Subjects & Max Scores

| Subject   | Max Score |
| --------- | --------- |
| Math      | 125       |
| Physics   | 75        |
| Chemistry | 75        |
| Biology   | 75        |
| English   | 50        |
| Khmer     | 75        |
| History   | 50        |
