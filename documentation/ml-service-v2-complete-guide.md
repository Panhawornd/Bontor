# 🎓 ML-Service-V2 — Complete Documentation Guide

> **What is this project?**
> This is an **AI-powered educational recommendation system** built for Cambodian high school students.
> A student enters their **grades**, **interests**, and **career goals**, and the system recommends:
>
> - Which **university major** fits them best
> - Which **universities** in Cambodia offer that major
> - Which **careers** they could pursue
> - What **skills** they need to develop
>
> The system uses a combination of **Natural Language Processing (NLP)** to understand what the student writes,
> **Machine Learning (ML)** to predict the best major based on patterns, and **Academic Rules** to ensure
> the student actually qualifies for the recommended major.

---

## 📁 Project Folder Structure

Below is the complete folder structure. Think of it like a factory with different departments,
each handling a specific job:

```
ml-service-v2/
│
├── app/                          ← 🚪 THE FRONT DOOR (API Layer)
│   ├── main.py                   ← The main entry point of the whole application
│   ├── routers/
│   │   └── recommendations.py    ← Handles incoming requests from the frontend
│   └── schemas/
│       └── models.py             ← Defines what data looks like (input/output shapes)
│
├── nlp/                          ← 🧠 THE LANGUAGE BRAIN (NLP Layer)
│   ├── preprocess.py             ← Cleans messy text into useful words
│   ├── sbert.py                  ← Converts words into numbers (vectors)
│   ├── similarity.py             ← Measures how similar two texts are
│   └── semantic_intent.py        ← Understands what the student REALLY means
│
├── core/                         ← ⚙️ THE CONTROL CENTER (Orchestration Layer)
│   ├── feature_builder.py        ← Packages everything into numbers for ML
│   └── recommendation_service.py ← The MAIN BRAIN that runs the whole pipeline
│
├── rules/                        ← 📏 THE RULE BOOK (Academic Rules)
│   └── eligibility.py            ← Checks if grades meet minimum requirements
│
├── ml/                           ← 🤖 THE PREDICTION ENGINE (Machine Learning)
│   ├── predict.py                ← Uses the trained model to make predictions
│   ├── train_rf.py               ← Creates fake students and trains the model
│   └── models/                   ← Saved trained model files (.pkl)
│
├── data/                         ← 📚 THE KNOWLEDGE BASE (Static Data)
│   ├── majors.py                 ← Information about 20+ university majors
│   ├── careers.py                ← Information about 30+ career paths
│   └── universities.py           ← Information about 17 Cambodian universities
│
├── train_model.py                ← 🏋️ Script to train the ML model (run once)
└── requirements.txt              ← 📦 List of Python packages needed
```

---

## 🔄 How a Request Flows Through the System (Step by Step)

Imagine a student named **Sokha** opens the website and fills in this form:

- **Grades:** Math: 100, Physics: 60, Chemistry: 50, Biology: 45, English: 40, Khmer: 55, History: 35
- **Interests:** "I love coding and building websites"
- **Career Goal:** "I want to become a software developer"
- **Strengths:** "logic, problem-solving"
- **Preferences:** "coding"

Here is exactly what happens inside the system, step by step:

```
┌──────────────────────────────────────────────────────────────────┐
│  STEP 1: Frontend sends Sokha's data to the API                 │
│  POST /api/analyze  →  recommendations.py receives it           │
├──────────────────────────────────────────────────────────────────┤
│  STEP 2: Text is cleaned                                        │
│  "I love coding and building websites"                          │
│  → preprocess.py → "love coding building website"               │
├──────────────────────────────────────────────────────────────────┤
│  STEP 3: Text is converted to numbers (SBERT)                   │
│  "love coding building website"                                 │
│  → sbert.py → [0.23, -0.15, 0.87, ... ] (384 numbers)          │
├──────────────────────────────────────────────────────────────────┤
│  STEP 4: System measures similarity to every major              │
│  → similarity.py →                                              │
│     Software Engineering: 0.82 (very similar!)                  │
│     Medicine: 0.12 (not similar at all)                         │
│     Architecture: 0.25 (a little similar)                       │
├──────────────────────────────────────────────────────────────────┤
│  STEP 5: System detects Sokha's intent                          │
│  → semantic_intent.py →                                         │
│     "coding" trigger detected! → Software Engineering boost: 6.0│
│     "building websites" detected! → Software Engineering: 6.0   │
├──────────────────────────────────────────────────────────────────┤
│  STEP 6: Rules check if Sokha qualifies                         │
│  → eligibility.py →                                             │
│     Math: 100/125 = 80% ✅ (above 50% threshold)               │
│     English: 40/50 = 80% ✅                                     │
│     → Software Engineering: ELIGIBLE                            │
├──────────────────────────────────────────────────────────────────┤
│  STEP 7: All data → single number vector                        │
│  → feature_builder.py →                                         │
│     [0.80, 0.80, 0.67, 0.60, 0.80, 0.73, 0.70, ... ] (71 nums)│
├──────────────────────────────────────────────────────────────────┤
│  STEP 8: ML model predicts major probabilities                  │
│  → predict.py (Random Forest) →                                 │
│     Software Engineering: 85% probability                       │
│     Data Science: 8% probability                                │
│     Civil Engineering: 3% probability                           │
├──────────────────────────────────────────────────────────────────┤
│  STEP 9: All signals are merged together                        │
│  → recommendation_service.py →                                  │
│     ML says SE: 85% + SBERT says SE: 0.82 + Rules say: OK      │
│     + Intent boost: 6.0 → Final: Software Engineering WINS      │
├──────────────────────────────────────────────────────────────────┤
│  STEP 10: Final JSON response sent to frontend                  │
│  → { majors: [...], careers: [...], universities: [...] }       │
└──────────────────────────────────────────────────────────────────┘
```

---

## 📂 FOLDER 1: `app/` — The Front Door

This folder handles **communication with the outside world**. When the frontend website
sends data to the backend, this is where it arrives first.

---

### 📄 File: `app/main.py`

**What it does in simple words:**
This file is like the **main entrance** of a restaurant. It sets up the restaurant (the app),
decides who is allowed to enter (CORS), and puts up signs showing where to go (routes).

**Code breakdown:**

```python
from fastapi import FastAPI

app = FastAPI(
    title="Grade Analysis ML Service",
    version="3.1.0"
)
```

**What this does:** Creates the application. FastAPI is the framework that handles
HTTP requests (like when your browser sends data to a server). Think of `app` as the
"restaurant" itself.

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**What this does:** CORS stands for "Cross-Origin Resource Sharing." By default, web browsers
block requests between different websites for security. For example, if your frontend runs at
`localhost:3000` and your backend runs at `localhost:8000`, the browser will block the request.
This middleware says "allow requests from anywhere" so the frontend can talk to the backend.

The `"*"` means "allow all." In production, you would replace this with your actual frontend URL
for better security.

```python
app.include_router(recommendations.router, prefix="/api", tags=["Recommendations"])
```

**What this does:** This connects the recommendation endpoints to the app. The `prefix="/api"`
means all routes defined in `recommendations.py` will start with `/api/`. So if
`recommendations.py` defines `/recommend`, the full URL becomes `/api/recommend`.

```python
@app.get("/health")
async def health():
    predictor = MLPredictor()
    return {
        "status": "healthy" if predictor.model is not None else "degraded",
        "model_loaded": predictor.model is not None,
    }
```

**What this does:** This is a "health check" endpoint. Monitoring tools (or humans) can call
`GET /health` to check if the service is working. It checks if the ML model loaded successfully.
If the model failed to load, it reports "degraded" status.

---

### 📄 File: `app/routers/recommendations.py`

**What it does in simple words:**
This file is like a **waiter in the restaurant**. It takes the customer's order (the request),
passes it to the kitchen (the recommendation service), and brings back the food (the response).

There are **two endpoints** (two menus):

**Endpoint 1: `POST /api/recommend`**
This is the "raw" output format. It returns data in the internal system format.

```python
@router.post("/recommend")
async def get_recommendations(request: RecommendationRequest):
    # Step 1: Convert the grades from a list to a dictionary
    # Input:  [{"subject": "math", "score": 100}, {"subject": "physics", "score": 60}]
    # Output: {"math": 100, "physics": 60}
    grades = {g.subject.lower(): g.score for g in request.grades}

    # Step 2: Call the recommendation service (the kitchen)
    result = recommendation_service.get_recommendations(
        grades=grades,
        interests=request.interests or "",
        career_goal=request.career_goals or "",
        strengths=request.strengths or "",
        preferences=request.preferences or ""
    )

    # Step 3: Return the result (serve the food)
    return RecommendationResponse(
        major_recommendations=result["major_recommendations"],
        universities=result["universities"],
        career_recommendations=result["career_recommendations"],
        skill_gaps=result["skill_gaps"],
        match_percentage=result["match_percentage"]
    )
```

**Endpoint 2: `POST /api/analyze`**
This is the "frontend-friendly" output. It transforms the data into the format that
the React/Next.js frontend expects. For example:

- Renames `major` → `name`
- Renames `confidence` → `score`
- Adds a `subject_analysis` section that shows each subject with labels like "Excellent" or "Needs Improvement"

```python
# This is how subject analysis is calculated:
max_scores = {"math": 125, "physics": 75, "chemistry": 75, ...}
normalized = (score / max_score) * 100

# Example: Math score = 100, max = 125
# normalized = (100 / 125) * 100 = 80%

if normalized >= 80:
    strength = "Excellent"      # 80-100%
elif normalized >= 65:
    strength = "Good"           # 65-79%
elif normalized >= 50:
    strength = "Average"        # 50-64%
else:
    strength = "Needs Improvement"  # Below 50%
```

**Error handling:**

```python
except Exception as e:
    error_id = str(uuid.uuid4())[:8]    # Generate unique error reference
    logger.error(f"Error (ref: {error_id}): {e}")
    raise HTTPException(status_code=500, detail=f"Error - reference {error_id}")
```

If something goes wrong, it generates a short unique ID (like "a3f8b2c1") and logs
the full error. The user only sees the ID, which they can report to the developer
who then searches the logs for that ID. This keeps error details private.

---

### 📄 File: `app/schemas/models.py`

**What it does in simple words:**
This file defines the **exact shape** of data going in and coming out of the API.
Think of it like a **mold for cookies** — every cookie (request/response) must fit
the exact shape of the mold, or it gets rejected.

It uses **Pydantic**, which is a Python library that automatically validates data.

```python
class GradeInput(BaseModel):
    subject: str        # Must be a string (like "math")
    score: float        # Must be a number (like 100.0)
```

If someone sends `{"subject": 123, "score": "abc"}`, Pydantic will automatically
reject it with a clear error message saying "subject must be a string" and
"score must be a number."

```python
class RecommendationRequest(BaseModel):
    grades: List[GradeInput]            # REQUIRED: List of grades
    interests: str = ""                 # OPTIONAL: defaults to empty string
    career_goals: Optional[str] = ""    # OPTIONAL: can be None or string
    strengths: Optional[str] = ""
    preferences: Optional[str] = ""
```

The `= ""` means "if the user doesn't send this field, use an empty string as default."
The `Optional[str]` means "this field can be either a string or None (null)."

**Why two response models?**

- `RecommendationResponse`: Used by the `/recommend` endpoint (internal format)
- `AnalyzeResponse`: Used by the `/analyze` endpoint (frontend format)

They contain the same data but structured differently for different consumers.

---

## 📂 FOLDER 2: `nlp/` — The Language Brain

This folder is responsible for **understanding human language**. When a student writes
"I love coding and want to build websites," these files figure out that the student
is interested in **Software Engineering**.

---

### 📄 File: `nlp/preprocess.py`

**What it does in simple words:**
This file **cleans up messy text** before the AI processes it. Imagine someone writes:
"I REALLY love coding!!! It's SO fun 😊"

The AI doesn't understand capital letters, punctuation, or emojis. This file strips all
that away and keeps only the meaningful words.

**The cleaning pipeline (5 steps):**

```
INPUT:  "I REALLY love coding!!! It's SO fun"
         ↓
Step 1:  "i really love coding!!! it's so fun"          (lowercase everything)
         ↓
Step 2:  "i really love coding    it s so fun"           (remove special characters)
         ↓
Step 3:  ["i", "really", "love", "coding", "it", "s", "so", "fun"]  (split into words)
         ↓
Step 4:  ["really", "love", "coding", "fun"]             (remove stopwords like "i", "it", "so")
         ↓
Step 5:  ["really", "love", "coding", "fun"]             (lemmatize: "running" → "run")
         ↓
OUTPUT: "really love coding fun"
```

**What are "stopwords"?**
Stopwords are common words like "I", "the", "is", "and", "it", "so" that appear in
almost every sentence but don't carry meaning. Removing them helps the AI focus on
the important words like "coding" and "love."

**What is "lemmatization"?**
Lemmatization converts different forms of a word to its base form:

- "running" → "run"
- "better" → "good"
- "codes" → "code"
- "studies" → "study"

This helps the AI understand that "coding" and "codes" mean the same thing.

**Why is thread safety important here?**

```python
_nltk_init_lock = threading.Lock()

def _init_nltk():
    with _nltk_init_lock:
        if _nltk_initialized:
            return
        nltk.download('punkt', quiet=True)
```

When multiple users send requests at the same time, the server runs multiple "threads"
(parallel workers). Without the lock, two threads might try to download NLTK data
simultaneously, causing errors. The `Lock()` ensures only ONE thread downloads at a time.

**The fallback system:**
If NLTK crashes for any reason, the code doesn't just fail. It has 3 levels of fallback:

1. Try full NLTK pipeline
2. If that fails → use simple `text.split()` without NLTK tokenizer
3. If THAT fails → just return `text.lower()` (absolute minimum)

This makes the system **resilient** — it keeps working even when components fail.

---

### 📄 File: `nlp/sbert.py`

**What it does in simple words:**
This file converts **words into numbers** that a computer can understand. Specifically,
it converts any text into a list of **384 numbers** called an "embedding" or "vector."

**Why 384 numbers?**
The model `all-MiniLM-L6-v2` was trained by researchers on millions of text pairs to
learn the "meaning" of language. It learned to represent meaning in 384 dimensions.
Texts with similar meaning will have similar numbers.

**Example:**

```
"I love programming"     → [0.23, -0.15, 0.87, 0.02, ... ] (384 numbers)
"I enjoy coding"         → [0.21, -0.14, 0.85, 0.03, ... ] (VERY similar numbers!)
"I want to be a doctor"  → [-0.45, 0.67, -0.12, 0.55, ...] (VERY different numbers!)
```

Because "I love programming" and "I enjoy coding" have similar meaning, their vectors
(lists of numbers) are almost identical. But "I want to be a doctor" has a completely
different meaning, so its vector is very different.

**The Singleton Pattern explained:**

```python
class SBERTEncoder:
    _instance = None    # There can only be ONE instance of this class

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

The SBERT model is about **80 megabytes**. Loading it takes 2-3 seconds. If we loaded
it every time someone sent a request, the system would be extremely slow. The Singleton
pattern ensures **the model is loaded exactly once** when the first request comes in,
and every future request reuses the same loaded model.

Think of it like a coffee machine in an office — you buy ONE machine, and everyone
shares it, rather than buying a new machine every time someone wants coffee.

**The `encode()` method:**

```python
def encode(self, text: str) -> np.ndarray:
    if not text or not text.strip():
        return np.zeros(384)    # Empty text → 384 zeros (means "nothing")

    embedding = self.model.encode(text)
    return embedding            # Returns array of 384 numbers
```

- If the input is empty, it returns 384 zeros (a "blank" vector).
- Otherwise, it passes the text through the neural network and gets back 384 numbers.

**The `encode_batch()` method:**
Instead of encoding texts one by one (slow), this method encodes many texts at once
(much faster because the GPU/CPU can process them in parallel).

**The embedding cache:**

```python
_embedding_cache: Dict[str, np.ndarray] = {}

def get_cached_embedding(key: str, text: str, encoder=None):
    if key in _embedding_cache:
        return _embedding_cache[key]    # Already computed → return instantly

    embedding = encoder.encode(text)    # Not cached → compute it
    _embedding_cache[key] = embedding   # Save for next time
    return embedding
```

Major and career descriptions never change. So once we compute their embeddings,
we save them in memory. The next time we need them, we just look them up instead
of re-computing (which is much slower).

---

### 📄 File: `nlp/similarity.py`

**What it does in simple words:**
This file measures **how similar** the student's text is to each major and career
description. It uses a mathematical formula called **cosine similarity**.

**What is cosine similarity?**
Imagine two arrows pointing in 3D space:

- If they point in the **same direction** → similarity = 1.0 (identical meaning)
- If they point in **opposite directions** → similarity = 0.0 (opposite meaning)
- If they're at a **90° angle** → similarity = 0.5 (unrelated)

The formula calculates the "angle" between two vectors (both are 384 numbers long).

**Example output:**

```
Student says: "I love coding and building apps"

Major similarities:
  Software Engineering:      0.82  ← Very similar! (strong match)
  Data Science:              0.65  ← Somewhat similar (related field)
  Cybersecurity:             0.55  ← Moderately similar
  Architecture:              0.22  ← Not very similar
  Medicine:                  0.12  ← Not similar at all
```

**How it works step by step:**

```python
def compute_major_similarity_scores(self, student_text, majors_data):
    # 1. Clean the student's text
    clean_student = clean_text(student_text)
    # "I love coding!!!" → "love coding"

    # 2. Convert to 384-number vector
    student_embedding = self.encoder.encode(clean_student)
    # "love coding" → [0.23, -0.15, 0.87, ...]

    # 3. For EACH major in the database...
    for major_name, major_info in majors_data.items():
        # Combine description + keywords for richer context
        major_text = f"{description} {keywords}"
        # "Study of software development... programming coding algorithm..."

        # Convert major text to vector (from cache if available)
        major_embedding = get_cached_embedding(...)

        # 4. Calculate cosine similarity between student and major
        score = cosine_similarity(student_embedding, major_embedding)
        scores[major_name] = score

    return scores
```

The same process happens for **career similarity** (`compute_career_similarity_scores`),
but instead of comparing to major descriptions, it compares to career descriptions.

---

### 📄 File: `nlp/semantic_intent.py`

**What it does in simple words:**
This is the **smartest file** in the NLP folder. It figures out what the student
**really means** when they write something. It solves two big problems:

**Problem 1: Ambiguity**
When a student says "I love design," do they mean:

- Web design? → UX/UI Design
- Building design? → Architecture
- Graphic design? → Graphic Design
- Fashion design? → Graphic Design
- Product design? → Mechanical Engineering

**Problem 2: Synonyms**
When a student says "I want to help sick people," they don't use the word "doctor"
or "medicine," but they clearly mean Medicine.

**The solution: Hybrid approach (Rules + AI)**

The file uses TWO methods and combines them:

**Method 1: Contextual Rules (for precision)**
These are hard-coded patterns that catch specific phrases:

```python
CONTEXTUAL_RULES = {
    "web_design": {
        "triggers": ["web design", "ui design", "ux design", "app design"],
        "context_words": ["figma", "wireframe", "prototype", "interface"],
        "majors": [("UX/UI Design", 6.0), ("Software Engineering", 4.5)]
    },
    "building_design": {
        "triggers": ["building design", "design house", "architectural design"],
        "context_words": ["building", "house", "blueprint", "floor plan"],
        "majors": [("Architecture", 6.0), ("Civil Engineering", 5.0)]
    },
    "software_dev": {
        "triggers": ["software developer", "programmer", "build apps", "write code"],
        "context_words": ["software", "code", "coding", "program", "algorithm"],
        "majors": [("Software Engineering", 6.0), ("Cybersecurity", 4.0)]
    }
}
```

When the system checks "I love web design":

1. It finds "web design" in the triggers → **exact match!**
2. It gives UX/UI Design a boost of 6.0 (very high confidence)
3. It also gives Software Engineering a boost of 4.5 (related)

**Method 2: Semantic Concepts (for fuzzy understanding)**
For cases where the student doesn't use exact trigger phrases, the system uses SBERT:

```python
SUBJECT_CONCEPTS = {
    "mathematics": {
        "phrases": [
            "I love mathematics and numbers",
            "I enjoy solving math problems and equations",
            "calculus algebra statistics probability",
            "I'm good at mathematical calculations",
            "I like working with formulas and numerical data"
        ],
        "majors": [("Data Science", 5.0), ("Software Engineering", 4.5), ("Finance", 4.5)]
    }
}
```

At startup, the system:

1. Encodes ALL 5 phrases into vectors
2. **Averages** them into ONE "prototype" vector for "mathematics"
3. When a student writes something, it compares their text to this prototype
4. If the similarity is > 0.50, the system says "this student likes math"

**How the two methods are combined:**

```python
def detect_intent(self, text):
    contextual_boosts = self._check_contextual_rules(text)    # Method 1
    semantic_boosts = self._detect_semantic_intent(text)       # Method 2

    # Merge: contextual takes priority when both match
    for major in all_majors:
        if both_matched:
            final = max(contextual, semantic * 0.8)  # Trust rules more
        elif only_contextual:
            final = contextual
        elif only_semantic:
            final = semantic
```

**Negative sentiment detection:**
The system also detects when a student says they DON'T want something:

```python
NEGATIVE_PHRASES = ["I don't like", "I hate", "I dislike", "not interested in", ...]
```

If the student writes "I don't like coding," the system:

1. Detects the negative sentiment
2. Finds that "coding" relates to Software Engineering
3. Instead of boosting SE, it **penalizes** it (multiplies by 0.5)

---

## 📂 FOLDER 3: `core/` — The Control Center

This is the **brain** of the entire system. It takes all the outputs from NLP, Rules,
and ML, and combines them into a final recommendation.

---

### 📄 File: `core/feature_builder.py`

**What it does in simple words:**
The Machine Learning model (Random Forest) is like a calculator — it can only work with
**numbers**. It doesn't understand words like "math" or "coding." This file translates
ALL the student's data into a single list of numbers.

Think of it like a **passport** — it takes your photo, name, age, nationality and puts
them all into one standardized document that border control can read.

**The 7 types of features it creates:**

**Feature 1: Subject Grades (7 numbers)**
Each grade is normalized to 0-1 by dividing by its maximum possible score:

```
Math:      100 / 125 = 0.80
Physics:    60 / 75  = 0.80
Chemistry:  50 / 75  = 0.67
Biology:    45 / 75  = 0.60
English:    40 / 50  = 0.80
Khmer:      55 / 75  = 0.73
History:    35 / 50  = 0.70

Result: [0.80, 0.80, 0.67, 0.60, 0.80, 0.73, 0.70]
```

**Feature 2: Grade Statistics (3 numbers)**

```
Mean (average):    0.73  (how good overall?)
Std (variation):   0.07  (consistent or spiky grades?)
Max (best grade):  0.80  (how good is their best subject?)
```

**Feature 3: Interaction Features (5 numbers)**
These capture **relationships** between subjects:

```
STEM average:      mean(math, physics, chemistry, biology) = 0.72
Language average:  mean(english, khmer) = 0.77
STEM/Lang ratio:   0.72 / 0.77 = 0.94  (balanced student)
Math × Physics:    0.80 × 0.80 = 0.64  (strong engineering signal)
Chemistry × Bio:   0.67 × 0.60 = 0.40  (moderate medical signal)
```

**Why are interaction features useful?**
A student with Math=90% AND Physics=90% is MUCH more likely to succeed in Engineering
than a student with Math=90% and Physics=20%. The multiplication `math × physics`
captures this: 0.9×0.9=0.81 vs 0.9×0.2=0.18. The ML model can easily see the difference.

**Feature 4: Encoded Strengths (8 numbers)**

```
Student says strengths: "logic, problem-solving"

STRENGTHS_MAP = {
    "logic": 0,          → 1 (mentioned!)
    "communication": 1,  → 0
    "creativity": 2,     → 0
    "problem-solving": 3, → 1 (mentioned!)
    "analytical": 4,     → 0
    "leadership": 5,     → 0
    "teamwork": 6,       → 0
    "technical": 7       → 0
}

Result: [1, 0, 0, 1, 0, 0, 0, 0]
```

**Feature 5: Encoded Preferences (8 numbers)**
Same idea as strengths:

```
Student says preferences: "coding"
Result: [1, 0, 0, 0, 0, 0, 0, 0]  (only "coding" position is 1)
```

**Feature 6: SBERT Similarity Scores (20 numbers — one per major)**

```
Software Engineering:  0.82
Data Science:          0.65
Medicine:              0.12
...etc for all 20 majors
```

**Feature 7: Eligibility Flags (20 numbers — one per major)**

```
Software Engineering:  1.0  (fully eligible)
Medicine:              0.3  (penalized - low biology/chemistry)
Civil Engineering:     1.0  (eligible)
...etc for all 20 majors
```

**The final vector:**
All 7 groups are glued together into ONE list:

```python
features = np.concatenate([
    [0.80, 0.80, 0.67, 0.60, 0.80, 0.73, 0.70],  # 7 grades
    [0.73, 0.07, 0.80],                             # 3 statistics
    [0.72, 0.77, 0.94, 0.64, 0.40],                 # 5 interactions
    [1, 0, 0, 1, 0, 0, 0, 0],                       # 8 strengths
    [1, 0, 0, 0, 0, 0, 0, 0],                       # 8 preferences
    [0.82, 0.65, 0.12, ...],                         # 20 SBERT scores
    [1.0, 1.0, 0.3, ...],                            # 20 eligibility flags
])
# Total = 7 + 3 + 5 + 8 + 8 + 20 + 20 = 71 numbers
```

This single list of 71 numbers is the student's "digital fingerprint" that gets
sent to the Random Forest model.

---

### 📄 File: `core/recommendation_service.py`

**What it does in simple words:**
This is the **BIGGEST and MOST IMPORTANT file** in the entire project (1,164 lines).
It is the "General Manager" that calls every other module and combines their results
into the final recommendation.

Think of it like a **head chef** in a kitchen. The head chef doesn't cook every dish
themselves — instead, they tell each station (NLP, Rules, ML) what to prepare, then
combine everything into the final meal (recommendation).

**The 5-step pipeline inside `get_recommendations()`:**

---

**STEP 1: NLP Pipeline (Understanding the student's words)**

```python
# 1a. Clean the text
cleaned_interests = clean_text(interests)
# "I love CODING!!!" → "love coding"

# 1b. Expand short inputs into longer descriptions
expanded_text = self._expand_minimal_input(combined_text, ...)
```

The expansion step is important for short inputs. If a student just types "code,"
the system expands it to:

```
"code" → "coding programming software engineering developer apps python javascript
           backend frontend algorithm technology computer science data science
           cybersecurity network security machine learning artificial intelligence
           database sql api systems"
```

This gives SBERT much more context to work with, resulting in better similarity scores.

```python
# 1c. Calculate SBERT similarity scores
major_similarities = self.similarity.compute_major_similarity_scores(expanded_text, ...)
career_similarities = self.similarity.compute_career_similarity_scores(expanded_text, ...)

# 1d. Detect semantic intent (what does the student REALLY mean?)
semantic_boosts = self._detect_intent_semantically(raw_text)

# 1e. Detect exclusions (what does the student NOT want?)
exclusion_penalties = self._detect_exclusions(raw_text)
```

**If no text is provided at all**, the system falls back to inferring interests
from grades:

```python
if not has_text_input:
    grade_inferred_majors = self._infer_majors_from_grades(grades)
    # High math + physics → boost Engineering
    # High biology + chemistry → boost Medicine
    # High english + history → boost Law, IR
```

---

**STEP 2: Rule-Based Filtering (Checking academic eligibility)**

```python
eligible_majors, eligibility_flags = self.rules.get_eligible_majors(grades, all_majors)
```

This calls `eligibility.py` to check grade requirements. Example output:

```
eligibility_flags = {
    "Software Engineering": 1.0,      # Fully eligible
    "Medicine": 0.3,                   # Severely penalized (low bio/chem)
    "Architecture": 1.0,              # Fully eligible
    "International Relations": 0.0,   # EXCLUDED (low English)
}
```

---

**STEP 3: Feature Engineering (Converting to numbers)**

```python
features = self.feature_builder.build_features(grades, interests, career_goal, ...)
# Returns: [0.80, 0.80, 0.67, ..., 0.82, 0.65, ...] (71 numbers)
```

---

**STEP 4: ML Prediction (Random Forest)**

```python
ml_predictions = self.predictor.predict(features)
# Returns: [
#   {"major": "Software Engineering", "probability": 0.85},
#   {"major": "Data Science", "probability": 0.08},
#   {"major": "Civil Engineering", "probability": 0.03},
#   ...
# ]
```

---

**STEP 5: Signal Fusion (The most complex part)**

This is where all the signals are **merged together** to produce the final ranking.
The system processes each ML prediction through a series of filters:

```python
for pred in ml_predictions:
    major = pred['major']

    # FILTER 1: Rule exclusion (RULES ALWAYS WIN)
    if eligibility == 0.0:
        continue  # Skip this major entirely

    # FILTER 2: Apply rule penalty
    pred['probability'] *= eligibility  # e.g., 0.85 × 0.3 = 0.255

    # FILTER 3: Exclusion penalty (student said "I hate X")
    if exclusion_penalty < 1.0:
        pred['probability'] = 0.001  # Effectively dead

    # FILTER 4: Software-specific check
    # If student clearly wants coding, remove non-CS engineering
    if "programming" in text and major == "Civil Engineering":
        pred['probability'] = 0.0  # Remove

    # FILTER 5: Apply semantic boosts (student loves this topic)
    if subject_boost > 1.0:
        pred['probability'] = max(pred['probability'], 0.5)  # Minimum 50%
        pred['probability'] *= subject_boost                   # Multiply by boost

    # FILTER 6: Apply SBERT similarity
    if similarity > 0.35:
        pred['probability'] += similarity * 1.5  # Strong match bonus
    elif similarity < 0.20:
        pred['probability'] = 0.0  # No semantic match = remove
```

**Major Injection — Honoring the student's intent:**
Sometimes the ML model misses a major that the student clearly asked for. For example,
if a student says "I want to be a doctor" but their grades are mediocre, the ML might
not predict Medicine at all. The injection logic fixes this:

```python
# If semantic boost > 2.0 but ML didn't include this major:
if boost > 2.0 and major not in ml_results:
    inject this major with probability = 0.5 × boost³
```

**Post-Processing — Building the final output:**

After fusion, the system builds 4 output sections:

1. **Major Recommendations**: Top 2 majors with confidence and descriptions
2. **Universities**: Matched by checking which universities offer the recommended majors,
   sorted into Safety/Target/Stretch based on grades
3. **Career Recommendations**: Jobs ranked by SBERT similarity to student's text
4. **Skill Gap Analysis**: Compares student's current skills vs. required skills,
   with actionable suggestions like "Take online courses to strengthen your Programming"

---

## 📂 FOLDER 4: `rules/` — The Rule Book

### 📄 File: `rules/eligibility.py`

**What it does in simple words:**
This file enforces **hard academic requirements**. No matter what the AI thinks,
if a student's grades don't meet the minimum, they can't study that major.

Think of it like a **height requirement on a roller coaster** — no matter how
much you want to ride, if you're not tall enough, you can't get on.

**The rules table:**

```
┌─────────────────────────────────────────────────────────────────────┐
│ IF Math < 50%                                                       │
│ THEN EXCLUDE: Software Engineering, Civil Engineering,              │
│              Mechanical Engineering, Electrical Engineering,         │
│              Chemical Engineering, Data Science, Cybersecurity,      │
│              Telecom & Networking, Architecture                     │
│ (Penalty: 0.0 = completely removed from results)                    │
├─────────────────────────────────────────────────────────────────────┤
│ IF English < 50%                                                    │
│ THEN EXCLUDE: International Relations, Business Admin,              │
│              Business Management, Finance, Law                      │
│ (Penalty: 0.0 = completely removed from results)                    │
├─────────────────────────────────────────────────────────────────────┤
│ IF Khmer < 45%                                                      │
│ THEN PENALIZE: Psychology, International Relations, Law, Education  │
│ (Penalty: 0.6 = probability reduced by 40%)                        │
├─────────────────────────────────────────────────────────────────────┤
│ IF History < 40%                                                    │
│ THEN PENALIZE: Education, International Relations, Law,             │
│              Graphic Design                                         │
│ (Penalty: 0.7 = probability reduced by 30%)                        │
├─────────────────────────────────────────────────────────────────────┤
│ IF Biology < 50% OR Chemistry < 50%                                 │
│ THEN PENALIZE: Medicine, Pharmacy, Dentistry                       │
│ (Penalty: 0.3 = probability reduced by 70%!)                       │
├─────────────────────────────────────────────────────────────────────┤
│ IF Biology < 70% OR Chemistry < 70%                                 │
│ THEN PENALIZE: Medicine, Pharmacy, Dentistry                       │
│ (Penalty: 0.7 = probability reduced by 30%)                        │
└─────────────────────────────────────────────────────────────────────┘
```

**Important: penalties can COMPOUND (stack):**
If a student has low Khmer AND low History, the penalties multiply:

```
Psychology penalty = 0.6 (from Khmer) × 0.7 (from History) = 0.42
This means Psychology's probability is reduced by 58%!
```

**The two types of consequences:**

1. **Exclusion (penalty = 0.0):** Major is completely removed. The student will
   NEVER see this major in their results.
2. **Penalty (0.0 < penalty < 1.0):** Major stays in results but its probability
   is reduced. It might still show up if other signals are strong enough.

---

## 📂 FOLDER 5: `ml/` — The Prediction Engine

### 📄 File: `ml/predict.py`

**What it does in simple words:**
This file loads the trained **Random Forest model** from disk and uses it to predict
which major a student should study. It's like a **fortune teller** that looks at
your 71-number fingerprint and says "you are most likely to succeed in Software Engineering."

**How Random Forest works (simplified):**
Imagine you have 1,000 friends, and each one has a slightly different opinion about
which major fits a student. Each friend looks at the student's data and votes for a major.
The major with the most votes wins. That's essentially what a Random Forest does — it's
1,000 "decision trees" (the friends) that each vote independently.

**The prediction process:**

```python
def predict(self, features):
    # 1. Reshape: turn 71 numbers into a 1×71 table row
    X = features.reshape(1, -1)     # [0.8, 0.8, 0.67, ...] → [[0.8, 0.8, 0.67, ...]]

    # 2. Handle size mismatch (safety check)
    # If the feature vector has fewer numbers than expected, pad with zeros
    # If it has more, trim the extra numbers
    if X.shape[1] < expected:
        X = np.hstack([X, np.zeros(...)])   # Add zeros at the end

    # 3. Scale the features
    X = self.scaler.transform(X)
    # This converts all numbers to have mean=0 and std=1
    # Without scaling, large numbers (like grade_mean=0.73) would
    # "overpower" small numbers (like pref_coding=1.0)

    # 4. Ask the Random Forest to predict
    probabilities = self.model.predict_proba(X)[0]
    # Returns: [0.85, 0.08, 0.03, 0.02, 0.01, 0.005, ...]
    # One probability for each major

    classes = self.model.classes_
    # Returns: ["Software Engineering", "Data Science", "Civil Engineering", ...]

    # 5. Pair them together and sort
    results = []
    for major, prob in zip(classes, probabilities):
        if prob >= 0.01:    # Only keep probabilities above 1%
            results.append({"major": major, "probability": prob})

    results.sort(key=lambda x: x["probability"], reverse=True)
    # Highest probability first
```

**Confidence levels:**

```
Probability >= 15%  → "high" confidence    ← Strong prediction
Probability >= 5%   → "medium" confidence  ← Decent match
Probability >= 1%   → "low" confidence     ← Weak match
Probability < 1%    → DISCARDED            ← Too uncertain, throw away
```

**The PredictionMonitor:**
Every time a prediction is made, the system records metrics:

```python
monitor.record(results, latency_ms)
# Tracks:
#   - How many total predictions have been made
#   - How many were "low confidence" (might need model retraining)
#   - Which majors are recommended most often
#   - How fast each prediction takes (in milliseconds)
```

These metrics are exposed at `GET /metrics` so developers can monitor the system's health.

---

### 📄 File: `ml/train_rf.py`

**What it does in simple words:**
This file **creates the brain** of the ML system. It generates 50,000 fake students
with realistic grade distributions, trains a Random Forest model on them, and saves
the trained model to disk.

**Why fake data? Why not use real student data?**
Because there is no existing dataset of "Cambodian high school students + which major
they should study." So instead, the system creates REALISTIC fake students using
statistical profiles.

**Per-Major Profiles — the heart of data generation:**

Each major has its own statistical profile that defines what a "typical" student
for that major looks like:

```python
"Software Engineering": {
    "subjects": {
        "math": (0.86, 0.07),      # Average math score: 86%, spread: ±7%
        "physics": (0.58, 0.12),   # Average physics: 58%, spread: ±12%
        "biology": (0.38, 0.14),   # Average biology: 38%, spread: ±14% (low!)
    },
    "strengths": {
        "logic": 0.90,             # 90% of SE students have "logic"
        "technical": 0.95,         # 95% have "technical"
        "communication": 0.30,    # Only 30% have "communication"
    },
    "preferences": {
        "coding": 0.95,            # 95% prefer "coding"
        "helping": 0.08,           # Only 8% prefer "helping" (that's Medicine)
    }
}
```

**How a fake student is generated:**

```
For Software Engineering student #3,847:

1. GRADES (Gaussian/Normal distribution):
   Math:      random_normal(mean=0.86, std=0.07) = 0.91  → 0.91 × 125 = 113.75
   Physics:   random_normal(mean=0.58, std=0.12) = 0.62  → 0.62 × 75  = 46.50
   Biology:   random_normal(mean=0.38, std=0.14) = 0.33  → 0.33 × 75  = 24.75
   ...

2. STRENGTHS (Coin flip with biased coin):
   Logic:     random() < 0.90 ? → YES (1)
   Technical: random() < 0.95 ? → YES (1)
   Communication: random() < 0.30 ? → NO (0)
   ...

3. SBERT SIMILARITY (Gaussian):
   vs Software Engineering: random_normal(0.62, 0.12) = 0.68  (HIGH - correct major!)
   vs Medicine:           random_normal(0.32, 0.12) = 0.28  (LOW - different major)
   ...

4. LABEL: "Software Engineering"
```

**The training process:**

```python
def train(self, n_samples=50000):
    # 1. Generate 50,000 fake students
    X, y = self.generate_smart_data(50000)
    # X = 50,000 rows × 71 columns (features)
    # y = 50,000 labels (major names)

    # 2. Fit the scaler (learn the mean/std of each feature)
    self.scaler.fit(X)
    X_scaled = self.scaler.transform(X)

    # 3. Split: 80% for training, 20% for testing
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, stratify=y
    )
    # stratify=y ensures each major has equal representation in train/test

    # 4. Train the Random Forest
    self.model = RandomForestClassifier(
        n_estimators=1000,        # 1,000 decision trees
        max_depth=30,             # Each tree can be up to 30 levels deep
        min_samples_leaf=3,       # Each leaf must have at least 3 samples
        class_weight="balanced",  # Give equal importance to rare majors
    )
    self.model.fit(X_train, y_train)

    # 5. Evaluate (how good is the model?)
    accuracy = accuracy_score(y_test, y_pred)     # e.g., 92%
    cv_scores = cross_val_score(model, X, y, cv=5)  # 5-fold cross-validation

    # 6. Save everything to disk
    joblib.dump(self.model, "ml/models/random_forest_major.pkl")
    joblib.dump(self.scaler, "ml/models/feature_scaler.pkl")
    joblib.dump(training_meta, "ml/models/training_meta.pkl")
```

**What is cross-validation?**
Instead of just testing on one 80/20 split, cross-validation:

1. Splits data into 5 equal parts
2. Trains on 4 parts, tests on 1 part
3. Repeats 5 times (each part gets to be the test set once)
4. Averages the results

This gives a more reliable accuracy estimate than a single split.

---

## 📂 FOLDER 6: `data/` — The Knowledge Base

### 📄 File: `data/majors.py`

**What it does in simple words:**
This is the **encyclopedia of majors**. It contains detailed information about
20+ university majors, including descriptions, required subjects, career paths,
and fundamental skills.

**Structure of each major entry:**

```python
"Software Engineering": {
    # KEYWORDS: Used by SBERT to match student text against this major
    "keywords": ["software", "programming", "coding", "developer", "apps", ...],

    # REQUIRED SUBJECTS: Used by eligibility rules to check grade requirements
    "required_subjects": ["math", "physics"],

    # DESCRIPTION: Shown to the user + used by SBERT for similarity matching
    "description": "Study of software development life cycle, programming, and system architecture",

    # CAREER PATHS: Links this major to specific jobs in careers.py
    "career_paths": ["Software Engineer", "Full Stack Developer", "Backend Developer", ...],

    # FUNDAMENTAL SKILLS: Used for skill gap analysis
    "fundamental_skills": {
        "Programming":    {"importance": "critical", "description": "Writing clean, efficient code"},
        "Problem Solving": {"importance": "critical", "description": "Breaking down complex problems"},
        "Mathematics":    {"importance": "high",     "description": "Logical and computational thinking"},
        "Algorithms":     {"importance": "high",     "description": "Data structures and algorithm design"},
        "System Design":  {"importance": "medium",   "description": "Architecting scalable systems"},
        "Version Control": {"importance": "medium",   "description": "Git and collaboration tools"}
    }
}
```

**All 20+ majors in the database:**
Software Engineering, Medicine, Electrical Engineering, Mechanical Engineering,
Civil Engineering, Chemical Engineering, Business Administration, Data Science,
Psychology, Education, International Relations, Architecture, Dentistry, Law,
Pharmacy, Business Management, Finance, UX/UI Design, Graphic Design,
Cybersecurity, Telecommunication and Networking.

---

### 📄 File: `data/careers.py`

**What it does in simple words:**
This is the **job directory**. It contains 30+ career descriptions with required
skills, salary ranges, education requirements, and growth outlook.

**Example entry:**

```python
"Software Engineer": {
    "description": "Design, develop, and maintain software applications and systems",
    "required_skills": ["Programming", "Problem Solving", "Algorithms", "System Design", "Version Control"],
    "avg_salary": "$70,000 - $120,000",
    "education_level": "Bachelor's Degree",
    "growth_outlook": "Excellent"
}
```

**How it's used:**

1. `similarity.py` compares student text against career descriptions using SBERT
2. `recommendation_service.py` picks careers linked to the recommended majors
3. `recommendation_service.py` uses `required_skills` for skill gap analysis

---

### 📄 File: `data/universities.py`

**What it does in simple words:**
This is the **university catalog** for Cambodia. It contains 17 universities with
their locations, available programs, and admission requirements.

**Example entry:**

```python
"Cambodia Academy of Digital Technology (CADT)": {
    "location": "Phnom Penh",
    "programs": ["Software Engineering", "Data Science", "Cybersecurity",
                 "Digital Business", "Telecommunication and Networking"],
    "requirements": {
        "min_grade": 75,                            # Minimum average grade
        "preferred_subjects": ["math", "english"]   # Subjects they care about most
    }
}
```

**How university matching works:**
The system finds universities that:

1. Offer the recommended major (e.g., CADT has Software Engineering ✅)
2. The student's grades meet or exceed the minimum (e.g., avg=73 vs required=75)

Then it categorizes the fit:

```
Safety:   Your avg >= required + 10 AND preferred subjects >= 65%
          (Very likely to get in)

Target:   Your avg >= required AND preferred subjects >= 50%
          (Good chance of getting in)

Stretch:  Your avg >= required - 5 AND preferred subjects >= 40%
          (Challenging but possible)
```

---

## 📂 ROOT FILES

### 📄 File: `train_model.py`

**What it does in simple words:**
This is the **one-click training script**. You run it once before starting the server
to train the Random Forest model.

```bash
# How to run it:
cd d:\Capstone-Grade-Analyze\ml-service-v2
python train_model.py
```

**Output:**

```
============================================================
  NLP + ML Recommendation System - Model Training
============================================================

Training with 21 majors

... (training progress) ...

============================================================
  Training Complete!
============================================================
  Test Accuracy:   92.15%
  CV Accuracy:     91.83% (+/- 1.24%)
  Features:        71
  Classes:         21
============================================================
```

After training, 4 files are saved in `ml/models/`:

- `random_forest_major.pkl` — The trained model
- `feature_scaler.pkl` — The StandardScaler (must match at prediction time)
- `feature_names.pkl` — List of feature names (for debugging)
- `training_meta.pkl` — Accuracy, CV scores, metadata

---

### 📄 File: `requirements.txt`

**What it does:** Lists all Python packages the project needs to run.

Key packages:

- `fastapi` — Web framework for the API
- `uvicorn` — ASGI server to run FastAPI
- `scikit-learn` — Machine Learning library (Random Forest, StandardScaler)
- `sentence-transformers` — SBERT model for text embeddings
- `nltk` — Natural Language Toolkit for text preprocessing
- `numpy` — Numerical computing (arrays, math operations)
- `pydantic` — Data validation for API schemas
- `joblib` — Saving/loading ML models to disk

---

## 🗝️ Key Concepts Summary

### What is SBERT?

**Sentence-BERT** is a neural network that converts any sentence into a list of 384 numbers.
Sentences with similar meanings produce similar numbers. The specific model used here
(`all-MiniLM-L6-v2`) is small (~80MB) and fast, making it ideal for real-time applications.

### What is Cosine Similarity?

A math formula that measures how similar two lists of numbers are. It calculates the
"angle" between them. If both lists point in the same direction, similarity = 1.0 (same meaning).
If they point in different directions, similarity = 0.0 (different meaning).

### What is a Random Forest?

A machine learning model made of many "decision trees" (like flowcharts). Each tree makes
its own prediction, and the final answer is determined by majority vote. It's called a
"forest" because it's many trees working together.

### What is StandardScaler?

A preprocessing step that adjusts all numbers so they have an average of 0 and a spread
of 1. This prevents features with large values (like grade percentages) from dominating
features with small values (like binary strength indicators).

### What is the Singleton Pattern?

A design pattern that ensures only ONE instance of a class exists. Used here for the
SBERT model (80MB, load once) and the ML predictor (avoid re-loading the model).

### What is Signal Fusion?

The process of combining multiple different sources of information (ML prediction,
SBERT similarity, rules, semantic intent) into a single final recommendation.
Each source has its own strength and weakness, so combining them produces a more
accurate result than any single source alone.

---

## 🧪 How to Run the System

```bash
# 1. Navigate to the project folder
cd d:\Capstone-Grade-Analyze\ml-service-v2

# 2. Install dependencies
pip install -r requirements.txt

# 3. Train the ML model (only needed once, or when you change data/majors.py)
python train_model.py

# 4. Start the API server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# 5. Test it
# Open your browser and go to: http://localhost:8000/docs
# This opens the auto-generated API documentation where you can test endpoints
```

---

> **This documentation was auto-generated to help understand every component of the
> ml-service-v2 recommendation system. Each file plays a specific role in the pipeline,
> and together they form a complete AI-powered educational guidance system.**
