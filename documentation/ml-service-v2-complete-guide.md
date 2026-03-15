# 🎓 ML-Service-V2 — Complete Documentation Guide (Updated)

> **What is this project?**
> This is a **fully data-driven, AI-powered educational recommendation system** built for Cambodian high school students.
> A student enters their **grades**, **interests**, and **career goals**, and the system recommends:
>
> - Which **university major** fits them best
> - Which **universities** in Cambodia offer that major
> - Which **careers** they could pursue
> - What **skills** they need to develop
>
> The V2 system removes all hardcoded heuristics. It uses **Natural Language Processing (NLP)** via SBERT to understand semantic intent, **Machine Learning (Random Forest)** trained on auto-generated database profiles, and **Continuous Sigmoid Eligibility Rules** derived purely from major requirements to provide an intelligent, flexible recommendation pipeline.

---

## 📁 Project Folder Structure

Below is the complete folder structure. Think of it like a factory with different departments, each handling a specific job:

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
│   ├── preprocess.py             ← Cleans messy text into useful words (NLTK)
│   ├── sbert.py                  ← Converts words into numbers (semantic vectors)
│   ├── similarity.py             ← Measures how similar two texts are
│   └── semantic_intent.py        ← Understands intent and exclusions semantically
│
├── core/                         ← ⚙️ THE CONTROL CENTER (Orchestration Layer)
│   ├── feature_builder.py        ← Packages everything into a numerical vector (71 numbers)
│   └── recommendation_service.py ← The MAIN BRAIN that merges all signals (No magic numbers)
│
├── rules/                        ← 📏 THE RULE BOOK (Academic Rules)
│   └── eligibility.py            ← Computes soft continuous eligibility (Sigmoid curve)
│
├── ml/                           ← 🤖 THE PREDICTION ENGINE (Machine Learning)
│   ├── predict.py                ← Uses the trained Random Forest model to make predictions
│   ├── train_rf.py               ← Auto-generates training profiles from the DB and trains the model
│   └── models/                   ← Saved trained model files (.pkl)
│
├── data/                         ← 📚 THE KNOWLEDGE BASE (Static Data)
│   ├── majors.py                 ← Information about 20+ university majors + requirements
│   ├── careers.py                ← Information about 30+ career paths
│   └── universities.py           ← Information about Cambodian universities
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
│  STEP 4: Semantic Intent & Similarity (Pure AI)                 │
│  → semantic_intent.py & similarity.py →                         │
│     System computes similarity between the student's semantic   │
│     vector and pre-computed profiles for every major from the DB│
│     Software Engineering: 0.82 (very similar!)                  │
│     Medicine: 0.12 (not similar at all)                         │
├──────────────────────────────────────────────────────────────────┤
│  STEP 5: Data-Driven Eligibility (Sigmoid)                      │
│  → eligibility.py →                                             │
│     Math is required for SE. 100/125 = 80%.                     │
│     Passes through sigmoid curve → Eligibility Factor: 0.95     │
├──────────────────────────────────────────────────────────────────┤
│  STEP 6: All data → single number vector                        │
│  → feature_builder.py →                                         │
│     [0.80, 0.80, 0.67... ] (71 numbers)                         │
│     (Grades, Stats, SBERT similarities for Strengths/Prefs)     │
├──────────────────────────────────────────────────────────────────┤
│  STEP 7: ML model predicts major probabilities                  │
│  → predict.py (Random Forest) →                                 │
│     Software Engineering: 85% probability                       │
├──────────────────────────────────────────────────────────────────┤
│  STEP 8: All signals are merged together                        │
│  → recommendation_service.py →                                  │
│     ML pred * Eligibility * SBERT * Intent * Subject Anchors    │
│     Final score computed. Concept anchors can lock intent.      │
├──────────────────────────────────────────────────────────────────┤
│  STEP 9: Final JSON response sent to frontend                   │
│  → { majors: [...], careers: [...], universities: [...] }       │
└──────────────────────────────────────────────────────────────────┘
```

---

## 📂 FOLDER 1: `app/` — The Front Door

This folder handles **communication with the outside world**. When the frontend website sends data to the backend, this is where it arrives first.

### 📄 File: `app/main.py`

This file is like the **main entrance** of a restaurant. It sets up the restaurant (FastAPI application), decides who is allowed to enter (CORS), and puts up signs showing where to go (routes). It also includes a `/health` endpoint for monitoring if the ML model is successfully loaded.

### 📄 File: `app/routers/recommendations.py`

This acts as our waiter. It provides two endpoints:

- **`POST /api/analyze`**: Packages the data into a consumer-friendly format suitable for the React/Next.js frontend. It transforms normalized grades into readable bands like "Excellent" or "Needs Improvement" and restructures JSON keys nicely.

### 📄 File: `app/schemas/models.py`

Defines the **exact shape** of data going in and coming out using **Pydantic**. This validates things like making sure `grades` is a list and `score` is a numeric value. It guarantees no badly-formatted data crashes the internal servers.

---

## 📂 FOLDER 2: `nlp/` — The Language Brain

This folder is responsible for **understanding human language**. The philosophy here in V2 is to eradicate hardcoded assumptions and let modern embedding models (SBERT) capture intent from the actual text.

### 📄 File: `nlp/preprocess.py`

**Cleans** messy text before the AI processes it.
It utilizes **NLTK** safely with threading locks. The 5 steps are:

1. Lowercase
2. Remove special characters
3. Tokenize (split into words)
4. Remove Stopwords (e.g., "I", "an", "the")
5. Lemmatize (e.g., "running" → "run")

It includes three fallback tiers if NLTK fails, making the pipeline highly resilient.

### 📄 File: `nlp/sbert.py`

Converts words into a list of **384 numbers** (a dense vector or embedding). It uses `all-MiniLM-L6-v2`. Semantic meaning is captured such that "I enjoy coding" and "I love programming" produce almost identical vectors, whilst "I want to be a doctor" produces a very different vector.

It uses a **Singleton Pattern** to ensure the 80MB model is loaded only once and includes an inner cache (`_embedding_cache`) so that static descriptions from the database do not need to be recalculated constantly.

### 📄 File: `nlp/similarity.py`

Measures how similar the student's text is to each major and career using **cosine similarity**. Cosine similarity measures the angle between two semantic vectors. A score of 1.0 means exactly the same meaning, while 0.0 means completely orthogonal (unrelated).

### 📄 File: `nlp/semantic_intent.py`

This V2 iteration completely removes hardcoded dictionaries and manual boost multipliers! It is purely data-driven.

1. **Semantic Setup:** Upon initialization, it calculates rich structural vectors for every major in `MAJOR_DATABASE` by combining its description, keywords, careers, and weighted fundamental skills.
2. **Detection:** It takes the student's input and checks distance to every generated major vector. The similarity score _is_ the boost logic.
3. **Exclusion / Negation:** It actively handles semantic negation combining SBERT negative sentiment checks (using precomputed anchor phrases like "I hate this") and keyword overrides to rigorously penalize majors the user specifies they don't want (e.g., "I don't like math").

---

## 📂 FOLDER 3: `core/` — The Control Center

This is the brain that maps NLP inputs and Database rules explicitly to Machine Learning representations.

### 📄 File: `core/feature_builder.py`

The AI needs a single, unified number list containing everything known about the student. It outputs exactly **71 numbers**, incorporating NLP and grades:

1. **Normalized Subject Grades**: 7 numbers.
2. **Grade Statistics**: 3 numbers (Mean, Standard Deviation, Max score).
3. **Interaction Features**: 5 numbers mapping STEM vs Language interplay (e.g. `STEM average`, `Math × Physics`).
4. **Encoded Strengths**: 8 continuous numbers using SBERT similarity to concepts (no longer simple binary flags).
5. **Encoded Preferences**: 8 continuous numbers via SBERT.
6. **SBERT Similarities**: 20 numbers representing similarity to the 20 majors.
7. **Eligibility Flags**: 20 numbers based on data-driven grade eligibility rules.

### 📄 File: `core/recommendation_service.py`

The **Head Chef** spanning ~900 lines. The system no longer uses chained `if/elif` statements. Instead, it fuses signals mathematically:

`Final Score = ML Pred × Eligibility × Penalty × SBERT Factor × Intent Factor × Subject Factor × Concept Anchor`

- **Data-Driven Eligibility**: Calls `EligibilityRules`.
- **Academic Signal Locking**: Extracts named subject interests.
- **Concept Anchoring System**: Uses semantic anchors mapped correctly to groups to ensure if the user explicitly writes "I want software engineering", the prediction heavily anchors there, avoiding ML failure cases from poor grades.
- **Ultra-Strict Filtering**: If intent is high, unassociated domains are thoroughly purged to keep recommendations clean.
- Maps recommendations, checks university fits with fallback categories (Safety, Target, Stretch), lists careers, and creates skill-gap suggestions via semantic distance between the user's `strengths` and the major's `fundamental_skills`.

---

## 📂 FOLDER 4: `rules/` — Academic Rules

### 📄 File: `rules/eligibility.py`

**Pure Database-Driven Rules.** This replaces hard thresholds (like "Math < 60 = fail").
It reads the `required_subjects` dynamically from `MAJOR_DATABASE`. It calculates the normalized average score of these required subjects and passes it through a **continuous sigmoid curve**.

- Score ~ 0.5 → Eligibility = 0.50 (middle slope)
- Score ~ 1.0 → Eligibility ≈ 0.95
  This imposes a "soft penalty", avoiding completely blocking students out of majors just because they missed an arbitrary grade cutoff by 1 point. It allows intense NLP intent to bridge a slight gap in grades.

---

## 📂 FOLDER 5: `ml/` — The Prediction Engine

### 📄 File: `ml/train_rf.py`

The actual Machine Learning generator. In previous versions, synthetic data was created based on developer-hardcoded distributions per major. **In V2, profiles are auto-generated from `MAJOR_DATABASE`**:

- It looks at a major's `required_subjects` to dynamically alter the mean/std sampling for grades.
- It uses SBERT directly against the major text array to derive synthetic generation probabilities for Strengths and Preferences.

The system generates ~50,000 synthetic rows of data matching this derived database distribution and trains the `RandomForestClassifier`.

When training finishes, it saves **FOUR** files to the `ml/models/` directory:

1. **`random_forest_major.pkl`**: The actual trained Random Forest model. It contains the "brain" (decision trees) that maps the 71-number input vector to a major probability.
2. **`feature_scaler.pkl`**: A standard scaler. ML models perform better when features are scaled (e.g., between 0 and 1 with a consistent standard deviation). This remembers exactly how the data was scaled during training so we can scale real user requests the exact same way before passing them to the model.
3. **`feature_names.pkl`**: A list of strings (e.g., "grade_math", "sbert_sim_Software Engineering"). If `predict.py` ever notices the user is sending 71 numbers, but the model expects 72, we use this file to immediately debug exactly which feature is missing!
4. **`training_meta.pkl`**: Metadata about the training run. It holds the model's accuracy, cross-validation scores, and the classes (majors) it was trained on. `predict.py` reads this to ensure it understands what the output probabilities map to.

random_forest_major.pkl: This is the actual Machine Learning model. It contains the trained "Decision Trees" that take the 71 numbers we give it and output probability percentages for all 20+ majors.
feature_scaler.pkl: Machine learning models prefer data to be "scaled" (e.g. distributed perfectly between 0.0 and 1.0) so large numbers like Max Grade = 125 don't overwhelm small NLP scores of 0.82. When the model trained, it scaled all the synthetic student data. This file saves exactly how it scaled the training data, so we can apply the exact same mathematical scale to live students' data in

predict.py
before making a prediction.
feature_names.pkl: This saves the exact list of the 71 feature names (e.g. ['grade_math', 'grade_physics', ..., 'sbert_sim_Software Engineering']). This file is extremely useful for debugging. If a user's data produces 70 numbers instead of 71,

predict.py
can load this file to figure out exactly which feature is missing by comparing the names!
training_meta.pkl: This saves metadata about the training run, such as the total rows used, the cross-validation accuracy, and crucially, the output classes (the alphabetical list of all the Majors the model was trained to predict). It ensures the live API knows exactly what accuracy the currently loaded model achieved during testing.

### 📄 File: `ml/predict.py`

Responsible for evaluating the trained Random Forest `joblib` file against the 71-feature vector generated by `FeatureBuilder`. It automatically loads all 4 `.pkl` files mentioned above. It first uses `feature_scaler` to normalize the user's data, then uses `random_forest_major` to predict.

It also features a `PredictionMonitor` class which tracks latency, top major frequencies, and low-confidence predictions to monitor model health in real-time.

---

## Conclusion

The architecture of **ML-Service-V2** succeeds by shifting business logic out of rigid code and into mathematical combinations derived directly from the Knowledge Base (`data/`). SBERT handles human messiness; `RandomForest` recognizes holistic patterns; `Eligibility` handles hard institutional realities, and `RecommendationService` directs them all symbiotically.

---

## 💻 Key Code Snippets Explained

To truly understand how V2 works, here are the most important pieces of code explained in simple terms.

### 1. The Continuous Sigmoid Curve (No Hard Cutoffs)

_(File: `rules/eligibility.py`)_

Instead of using a rigid rule like `if math < 50: reject()`, we use a math function called a **sigmoid curve** to create a gentle, sliding scale for grades.

```python
def _sigmoid_eligibility(avg_normalised: float) -> float:
    k = 8  # How steep the curve is
    midpoint = 0.5  # The "average" score (50%)

    # This formula creates an S-shaped curve
    # Score 0.0 → returns ~0.05
    # Score 0.5 → returns 0.50
    # Score 1.0 → returns ~0.95
    return float(1.0 / (1.0 + np.exp(-k * (avg_normalised - midpoint))))
```

**Why this is genius:** If a student scores `0.48` instead of `0.50`, they don't get an automatic `0%` eligibility (a hard fail). They might get a `0.45` eligibility factor. Because the final score is multiplied together, a `0.45` eligibility combined with a massive SBERT Intent Boost (e.g. they typed that they really love the topic) can still result in the major being recommended!

### 2. Auto-Generating The "Prototype" for a Major

_(File: `nlp/semantic_intent.py`)_

To check if a student fits a major, we first need to define what the major "looks like" in text. We don't hardcode this anymore. We pull it from the database and glue it together.

```python
# We take pieces from the database
desc = info.get("description", "")
keywords = info.get("keywords", [])
careers = info.get("career_paths", [])
subjects = info.get("required_subjects", [])

# We merge them into one giant "Profile Paragraph"
# We repeat keywords and subjects to give them more "weight" in the SBERT vector
major_text = (
    f"{desc} "
    f"{' '.join(keywords)} {' '.join(keywords)} "
    f"{' '.join(careers)} "
    f"{' '.join(subjects)} {' '.join(subjects)}"  # Repeated so "math" stands out more
)

# Convert this giant paragraph into exactly 384 numbers
embedding = enc.encode(clean_text(major_text))
```

**Why this is genius:** If you change the `description` or add a new `keyword` to the database, the AI instantly updates its understanding of what the major is. You never have to update the logic code!

### 3. Measuring SBERT Similarity (Cosine Similarity)

_(File: `nlp/semantic_intent.py` & `nlp/similarity.py`)_

Once we have the student's text turned into 384 numbers, and the major's text turned into 384 numbers, how do we compare them? We check the "angle" between those two lists using **Cosine Similarity**.

```python
def _cosine(a: np.ndarray, b: np.ndarray) -> float:
    # a = student's 384 numbers
    # b = major's 384 numbers

    # Calculate vector length
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    if na == 0 or nb == 0:
        return 0.0

    # Dot product divided by lengths = Cosine Similarity
    # 1.0 = identical meaning
    # 0.0 = completely unrelated
    return float(np.dot(a, b) / (na * nb))
```

**Why this is genius:** SBERT puts semantically similar concepts close to each other in mathematical space. If `a` is "I enjoy building houses" and `b` is the vector for Architecture (which contains "blueprint" and "construction"), the angle between them will be very small, yielding a high similarity like `0.85`. You don't need keyword matching anymore!

### 4. The Final "Fusion" Equation

_(File: `core/recommendation_service.py`)_

This is where everything comes together. Notice there is no `if/else` logic deciding the winner. It's pure multiplication.

```python
final_score = (
    pred_copy["probability"]    # From the Machine Learning Random Forest Model (e.g., 0.80)
    * eligibility               # From the Sigmoid Rule (e.g., 0.95)
    * penalty                   # Exclusion penalty (1.0 if none, 0.1 if user hates it)
    * sbert_factor              # Text similarity boost (e.g., exponential boost if very similar)
    * intent_factor             # Direct intent boost
    * subject_factor            # Did they mention a core subject like "math"?
    * anchor_factor             # Concept anchors (Overrides ML if the user specifically asked for this)
)
```

**Why this is genius:** Every single layer (ML, NLP, Rules) provides a "multiplier" between 0 and N.

- If ML says "NO" (`0.05`), but the student explicitly typed "I want software engineering" (Concept Anchor = `50.0`), the final score becomes huge, forcing the recommendation.
- If NLP says "YES" (`2.0`), but the student failed all required subjects (Sigmoid = `0.05`), the final score is squished down towards zero.
  They naturally balance each other out!
