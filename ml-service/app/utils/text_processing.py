"""
Text processing utilities for translation, preprocessing, and similarity
"""
import re
import difflib
import numpy as np
from typing import List, Dict, Any
from .constants import LETTER_MAP, KHMER_TO_ENGLISH, DOMAIN_KEYWORDS

# Import ML models (will be initialized in main.py)
sentence_model = None
zero_shot = None

def set_ml_models(sentence_transformer=None, zero_shot_classifier=None):
    """Set ML models for text processing"""
    global sentence_model, zero_shot
    sentence_model = sentence_transformer
    zero_shot = zero_shot_classifier

def translate_to_english(text: str) -> str:
    """Translate Khmer text to English using basic mapping"""
    result = text
    for khmer, english in KHMER_TO_ENGLISH.items():
        result = result.replace(khmer, english)
    return result

def detect_and_translate_text(text: str) -> str:
    """Detect if text contains Khmer and translate to English"""
    # Check if text contains Khmer Unicode characters
    if any('\u1780' <= char <= '\u17FF' for char in text):
        return translate_to_english(text)
    return text

def enhanced_preprocess_text(text: str) -> str:
    """Enhanced text preprocessing with fuzzy matching and synonym expansion"""
    if not text:
        return ""
    
    # Convert to lowercase and remove special characters
    text = re.sub(r'[^a-zA-Z\s]', '', text.lower())
    text = ' '.join(text.split())
    
    # Lightweight fuzzy correction to map common misspellings to known domain terms
    # Build a small vocabulary from major keywords and common domains
    vocab = set()
    from ..databases.majors import MAJOR_DATABASE
    for m in MAJOR_DATABASE.values():
        for kw in m.get('keywords', []):
            for token in kw.split():
                vocab.add(token.lower())
        for cp in m.get('career_paths', []):
            for token in cp.split():
                vocab.add(token.lower())
    # Add domain terms explicitly
    vocab.update(["electrical", "electronics", "mechanical", "civil", "chemical", "software", "data", "ai", "ml", "machine", "learning"])    
    
    def correct_token(tok: str) -> str:
        if tok in vocab or len(tok) <= 3:
            return tok
        # Find close matches
        matches = difflib.get_close_matches(tok, list(vocab), n=1, cutoff=0.86)
        return matches[0] if matches else tok
    
    text = ' '.join(correct_token(t) for t in text.split())

    # Comprehensive synonym expansion
    synonyms = {
        # Technology & Programming
        'coding': 'programming code software development',
        'programming': 'coding software development programming',
        'computer': 'technology tech computing digital',
        'software': 'programming coding applications apps',
        'tech': 'technology computer digital',
        'apps': 'applications software mobile',
        'website': 'web development frontend backend',
        'data': 'analytics statistics information',
        'ai': 'artificial intelligence machine learning',
        'ml': 'machine learning artificial intelligence',
        'training': 'machine learning ai ml training models',
        'train': 'training machine learning ai ml',
        'numbers': 'math mathematics numerical',
        'working with': 'work with',
        
        # Engineering & Electronics - CRITICAL for electrical detection
        'electronic': 'electronics electrical circuit power signal embedded',
        'electronics': 'electronic electrical circuit power embedded signal',
        'electrical': 'electric electronics circuit power',
        'circuit': 'electronics electrical electronic',
        'mechanic': 'mechanical machine engineering',
        'mechanical': 'mechanic machine mechanism engineering',
        
        # Medical & Health
        'doctor': 'medical physician healthcare medicine',
        'medical': 'healthcare medicine doctor health',
        'health': 'medical healthcare medicine wellness',
        'helping people': 'help people care healing medical',
        'saving lives': 'save lives medical health doctor',
        'patient': 'medical healthcare doctor treatment',
        'hospital': 'medical healthcare clinic treatment',
        'dentist': 'dental oral health teeth',
        'nurse': 'nursing healthcare medical',
        'help people': 'helping people care',
        'save lives': 'saving lives medical',
        
        # Business & Management
        'business': 'management commerce entrepreneurship',
        'money': 'finance business economics',
        'management': 'business leadership administration',
        'entrepreneur': 'business startup founder',
        'finance': 'money business economics',
        'marketing': 'advertising promotion business',
        
        # Arts & Design
        'art': 'creative design artistic',
        'design': 'creative art visual',
        'drawing': 'art design creative visual',
        'music': 'art creative musical',
        'creative': 'art design innovative',
        
        # Education & Teaching
        'teaching': 'education teacher instructor',
        'teacher': 'education teaching instructor',
        'education': 'teaching learning academic',
        'students': 'education teaching learning',
        
        # Engineering & Construction
        'building': 'construction engineering architecture',
        'construction': 'building engineering architecture',
        'engineer': 'engineering technical design',
        'designing': 'design engineering creative',
        
        # General Interest Terms
        'love': 'enjoy like passionate interested',
        'enjoy': 'love like interested passionate',
        'interested': 'curious fascinated drawn to',
        'want': 'desire wish hope aspire',
        'dream': 'aspire wish goal ambition',
        'passion': 'love enjoy interested',
        'career': 'job profession work',
        'job': 'career profession work',
        'work': 'job career profession',
    }
    
    # Apply synonym expansion
    words = text.split()
    expanded_words = []
    for word in words:
        if word in synonyms:
            expanded_words.append(synonyms[word])
        else:
            expanded_words.append(word)
    
    return ' '.join(expanded_words)

def calculate_similarity(text1: str, text2: str) -> float:
    """Calculate semantic similarity between two texts"""
    return enhanced_calculate_text_similarity(text1, [text2])

def enhanced_calculate_text_similarity(user_text: str, keywords: List[str]) -> float:
    """Enhanced text similarity calculation with multiple metrics"""
    if not user_text or not keywords:
        return 0.0

    try:
        # Preprocess both texts with enhanced preprocessing
        user_clean = enhanced_preprocess_text(user_text)
        keywords_text = ' '.join(keywords)
        keywords_clean = enhanced_preprocess_text(keywords_text)
        
        # Use sentence transformers for semantic understanding
        if sentence_model is not None:
            try:
                from sentence_transformers import util
                user_embedding = sentence_model.encode([user_clean], convert_to_tensor=True)
                keywords_embedding = sentence_model.encode([keywords_clean], convert_to_tensor=True)
                semantic_similarity = float(util.cos_sim(user_embedding, keywords_embedding)[0][0])
            except:
                semantic_similarity = 0.0
        else:
            semantic_similarity = 0.0
        
        # Enhanced keyword matching
        user_words = set(user_clean.split())
        keyword_words = set(keywords_clean.split())
        
        # Jaccard similarity
        intersection = user_words.intersection(keyword_words)
        union = user_words.union(keyword_words)
        jaccard_sim = len(intersection) / len(union) if union else 0.0
        
        # Partial word matching
        partial_matches = 0
        for user_word in user_words:
            for keyword_word in keyword_words:
                if user_word in keyword_word or keyword_word in user_word:
                    partial_matches += 1
                    break
        
        partial_sim = partial_matches / len(user_words) if user_words else 0.0
        
        # Enhanced weighted combination with higher sensitivity to user prompts
        if semantic_similarity > 0:
            # Boost keyword matching for better prompt responsiveness
            final_similarity = (semantic_similarity * 0.5) + (jaccard_sim * 0.3) + (partial_sim * 0.2)
        else:
            # Fallback to keyword matching only with higher weights
            final_similarity = (jaccard_sim * 0.7) + (partial_sim * 0.3)
        
        # Boost similarity for exact keyword matches
        exact_matches = sum(1 for keyword in keywords if keyword.lower() in user_clean.lower())
        if exact_matches > 0:
            final_similarity += (exact_matches * 0.1)  # Boost for exact matches
        
        return min(1.0, final_similarity)
    except Exception as e:
        print(f"Error in enhanced text similarity calculation: {e}")
        return 0.0

def zero_shot_major_scores(user_text: str) -> Dict[str, float]:
    """Score each major label directly from free-form text using zero-shot classification."""
    if not zero_shot or not user_text:
        return {}
    from ..databases.majors import MAJOR_DATABASE
    labels = list(MAJOR_DATABASE.keys())
    try:
        out = zero_shot(user_text, candidate_labels=labels, multi_label=True)
        return {lbl: float(score) for lbl, score in zip(out["labels"], out["scores"])}
    except Exception as e:
        print(f"Zero-shot scoring failed: {e}")
        return {}

def recognize_user_intent(text: str) -> Dict[str, Any]:
    """Recognize user intent and extract key information"""
    text_lower = text.lower()
    
    intent = {
        'field_of_interest': None,
        'career_goals': None,
        'work_style': None,
        'values': [],
        'skills_mentioned': [],
        'confidence': 0.0
    }
    
    # Field detection with confidence scoring
    field_keywords = {
        'technology': ['programming', 'coding', 'software', 'computer', 'tech', 'ai', 'data', 'apps', 'website'],
        'healthcare': ['doctor', 'medical', 'health', 'helping', 'patient', 'hospital', 'dentist', 'nurse', 'medicine'],
        'business': ['business', 'money', 'management', 'entrepreneur', 'finance', 'marketing', 'commerce'],
        'arts': ['art', 'design', 'creative', 'drawing', 'music', 'artistic', 'visual'],
        'education': ['teaching', 'education', 'teacher', 'students', 'learning', 'academic'],
        'engineering': ['building', 'construction', 'engineer', 'designing', 'technical', 'architecture'],
        'law': ['law', 'legal', 'lawyer', 'justice', 'court', 'rights'],
        'science': ['research', 'science', 'laboratory', 'experiment', 'discovery']
    }
    
    field_scores = {}
    for field, keywords in field_keywords.items():
        score = sum(1 for keyword in keywords if keyword in text_lower)
        if score > 0:
            field_scores[field] = score / len(keywords)
    
    if field_scores:
        intent['field_of_interest'] = max(field_scores, key=field_scores.get)
        intent['confidence'] = max(field_scores.values())
    
    # Work style detection
    if any(word in text_lower for word in ['team', 'group', 'collaborate', 'together']):
        intent['work_style'] = 'teamwork'
    elif any(word in text_lower for word in ['alone', 'independent', 'solo', 'individual']):
        intent['work_style'] = 'independent'
    elif any(word in text_lower for word in ['lead', 'leadership', 'manage', 'direct']):
        intent['work_style'] = 'leadership'
    
    # Values detection
    if any(word in text_lower for word in ['help', 'care', 'people', 'society', 'community']):
        intent['values'].append('helping_others')
    if any(word in text_lower for word in ['money', 'wealth', 'rich', 'success', 'profit']):
        intent['values'].append('financial_success')
    if any(word in text_lower for word in ['creative', 'artistic', 'innovative', 'original']):
        intent['values'].append('creativity')
    if any(word in text_lower for word in ['stable', 'secure', 'safe', 'reliable']):
        intent['values'].append('stability')
    if any(word in text_lower for word in ['challenge', 'difficult', 'complex', 'problem']):
        intent['values'].append('challenge')
    
    # Skills mentioned
    skill_keywords = {
        'communication': ['speak', 'write', 'present', 'explain', 'communicate'],
        'analytical': ['analyze', 'think', 'logic', 'reasoning', 'problem'],
        'creative': ['create', 'design', 'imagine', 'innovate', 'artistic'],
        'technical': ['technical', 'programming', 'coding', 'software', 'computer'],
        'leadership': ['lead', 'manage', 'direct', 'guide', 'team'],
        'mathematical': ['math', 'calculate', 'numbers', 'statistics', 'analytics']
    }
    
    for skill, keywords in skill_keywords.items():
        if any(keyword in text_lower for keyword in keywords):
            intent['skills_mentioned'].append(skill)
    
    return intent

def context_aware_text_processing(user_text: str) -> Dict[str, Any]:
    """Process user text with context awareness and multilingual support"""
    # Detect and translate if needed
    translated_text = detect_and_translate_text(user_text)
    
    # Recognize user intent
    intent = recognize_user_intent(translated_text)
    
    # Enhanced preprocessing
    processed_text = enhanced_preprocess_text(translated_text)
    
    return {
        'original_text': user_text,
        'translated_text': translated_text,
        'processed_text': processed_text,
        'intent': intent,
        'is_multilingual': translated_text != user_text
    }

def detect_primary_domain(text: str) -> Dict[str, Any]:
    """Detect the primary domain from user text with confidence scoring"""
    if not text:
        return {"domain": None, "confidence": 0.0, "keywords_found": []}
    
    text_lower = text.lower()
    domain_scores = {}
    keywords_found = {}
    
    for domain, keywords in DOMAIN_KEYWORDS.items():
        score = 0
        found_keywords = []
        
        for keyword in keywords:
            if keyword in text_lower:
                # Weight longer, more specific keywords higher
                weight = len(keyword.split()) * 2 if len(keyword.split()) > 1 else 1
                score += weight
                found_keywords.append(keyword)
        
        if score > 0:
            domain_scores[domain] = score
            keywords_found[domain] = found_keywords
    
    if not domain_scores:
        return {"domain": None, "confidence": 0.0, "keywords_found": []}
    
    # Find the domain with highest score
    primary_domain = max(domain_scores, key=domain_scores.get)
    max_score = domain_scores[primary_domain]
    
    # Calculate confidence based on score and keyword specificity
    # Special boost for mechanical engineering with "building machine" keywords (but not for "building intelligent systems")
    if primary_domain == "mechanical_engineering" and any(kw in text_lower for kw in ["building machine", "building machines", "constructing machine"]) and not any(kw in text_lower for kw in ["intelligent systems", "ai", "artificial intelligence", "machine learning", "data analysis"]):
        confidence = 0.9  # High confidence for building machine input
    else:
        confidence = min(1.0, max_score / 8)  # More generous confidence calculation
    
    return {
        "domain": primary_domain,
        "confidence": confidence,
        "keywords_found": keywords_found.get(primary_domain, []),
        "all_scores": domain_scores
    }

def get_domain_guardrails(primary_domain: str) -> Dict[str, Any]:
    """Get domain-specific guardrails to prevent cross-domain confusion"""
    guardrails = {
        "electrical_engineering": {
            "boost_majors": ["Electrical Engineering"],
            "boost_careers": ["Electrical Engineer", "Electronics Engineer", "Power Systems Engineer"],
            "demote_majors": ["Architecture", "Business Administration", "Medicine", "Law"],
            "demote_careers": ["Architect", "Business Manager", "Doctor", "Lawyer"],
            "required_keywords": ["electrical", "electric", "circuit", "power", "electronics"]
        },
        "mechanical_engineering": {
            "boost_majors": ["Mechanical Engineering"],
            "boost_careers": ["Mechanical Engineer", "Robotics Engineer", "Manufacturing Engineer", "Industrial Engineer", "Automation Engineer", "Aerospace Engineer"],
            "demote_majors": ["Architecture", "Business Administration", "Medicine", "Law"],
            "demote_careers": ["Architect", "Business Manager", "Doctor", "Lawyer"],
            "required_keywords": ["mechanical", "machine", "mechanism", "manufacturing", "building machine", "building machines", "flight", "space", "aircraft", "rocket", "rockets", "aerospace", "aviation", "airplane", "airplanes", "helicopter", "helicopters", "satellite", "satellites", "spacecraft", "engineering challenges", "designed", "designing"]
        },
        "civil_engineering": {
            "boost_majors": ["Civil Engineering"],
            "boost_careers": ["Civil Engineer", "Structural Engineer", "Construction Manager"],
            "demote_majors": ["Architecture", "Business Administration", "Medicine", "Law"],
            "demote_careers": ["Architect", "Business Manager", "Doctor", "Lawyer"],
            "required_keywords": ["civil", "infrastructure", "bridge", "road", "construction"]
        },
        "chemical_engineering": {
            "boost_majors": ["Chemical Engineering"],
            "boost_careers": ["Chemical Engineer", "Process Engineer", "Materials Engineer"],
            "demote_majors": ["Architecture", "Business Administration", "Medicine", "Law"],
            "demote_careers": ["Architect", "Business Manager", "Doctor", "Lawyer"],
            "required_keywords": ["chemical", "chemistry", "process", "reaction"]
        },
        "software_engineering": {
            "boost_majors": ["Computer Science", "Data Science"],
            "boost_careers": ["Software Engineer", "Developer", "Programmer", "Data Scientist"],
            "demote_majors": ["Architecture", "Business Administration", "Medicine"],
            "demote_careers": ["Architect", "Business Manager", "Doctor", "Civil Engineer"],
            "required_keywords": ["software", "coding", "programming", "computer"]
        },
        "data_science": {
            "boost_majors": ["Computer Science", "Data Science"],
            "boost_careers": ["Data Scientist", "Data Analyst", "Machine Learning Engineer"],
            "demote_majors": ["Architecture", "Business Administration", "Medicine"],
            "demote_careers": ["Architect", "Business Manager", "Doctor", "Civil Engineer"],
            "required_keywords": ["data", "analytics", "ai", "ml", "machine learning"]
        },
        "medicine": {
            "boost_majors": ["Medicine"],
            "boost_careers": ["Doctor", "Surgeon", "Medical Researcher", "Physician"],
            "demote_majors": ["Architecture", "Business Administration", "Engineering"],
            "demote_careers": ["Architect", "Business Manager", "Engineer", "Civil Engineer"],
            "required_keywords": ["medical", "doctor", "medicine", "health", "patient"]
        },
        "dentistry": {
            "boost_majors": ["Dentistry"],
            "boost_careers": ["Dentist", "Orthodontist", "Oral Surgeon"],
            "demote_majors": ["Architecture", "Business Administration", "Engineering"],
            "demote_careers": ["Architect", "Business Manager", "Engineer", "Doctor"],
            "required_keywords": ["dentistry", "dentist", "dental", "teeth", "oral"]
        },
        "architecture": {
            "boost_majors": ["Architecture"],
            "boost_careers": ["Architect", "Urban Planner", "Interior Designer"],
            "demote_majors": ["Engineering", "Business Administration", "Medicine"],
            "demote_careers": ["Engineer", "Business Manager", "Doctor", "Civil Engineer"],
            "required_keywords": ["architecture", "architect", "building design", "buildings"]
        },
        "business": {
            "boost_majors": ["Business Administration"],
            "boost_careers": ["Manager", "Entrepreneur", "Business Consultant"],
            "demote_majors": ["Engineering", "Architecture", "Medicine"],
            "demote_careers": ["Engineer", "Architect", "Doctor", "Civil Engineer"],
            "required_keywords": ["business", "management", "finance", "marketing"]
        },
        "psychology": {
            "boost_majors": ["Psychology"],
            "boost_careers": ["Psychologist", "Counselor", "Therapist"],
            "demote_majors": ["Engineering", "Architecture", "Medicine"],
            "demote_careers": ["Engineer", "Architect", "Doctor", "Civil Engineer"],
            "required_keywords": ["psychology", "psychologist", "mental", "behavior"]
        },
        "international_relations": {
            "boost_majors": ["International Relations"],
            "boost_careers": ["Diplomat", "Policy Analyst", "International Consultant", "Foreign Service Officer", "International Development Specialist", "Global Affairs Analyst", "International Trade Specialist", "Peacekeeping Officer"],
            "demote_majors": ["Engineering", "Architecture", "Medicine"],
            "demote_careers": ["Engineer", "Architect", "Doctor", "Civil Engineer"],
            "required_keywords": ["international", "diplomacy", "politics", "global", "foreign", "policy", "government", "diplomat", "foreign service", "international development", "embassy", "consulate", "peacekeeping", "international trade", "international security", "international law", "global affairs", "foreign policy", "international organizations", "united nations", "ngo", "humanitarian"]
        },
        "education": {
            "boost_majors": ["Education"],
            "boost_careers": ["Teacher", "Principal", "Educational Consultant", "Curriculum Developer", "University Professor", "Special Education Teacher", "Educational Technology Specialist", "School Counselor", "Training and Development Manager"],
            "demote_majors": ["Engineering", "Architecture", "Medicine"],
            "demote_careers": ["Engineer", "Architect", "Doctor", "Civil Engineer"],
            "required_keywords": ["teaching", "education", "teacher", "school", "learning", "students", "classroom", "teach", "mentor", "guide", "educator", "professor", "principal", "curriculum", "educational technology", "special education", "early childhood education", "educational administration", "educational policy", "teacher training", "educational research", "academic", "pedagogy", "instructional design", "educational leadership", "school counselor", "educational consultant"]
        },
        "psychology": {
            "boost_majors": ["Psychology"],
            "boost_careers": ["Psychologist", "Counselor", "Therapist", "Researcher", "School Psychologist", "Forensic Psychologist", "Sports Psychologist", "Industrial Psychologist", "Mental Health Counselor"],
            "demote_majors": ["Engineering", "Architecture", "Medicine"],
            "demote_careers": ["Engineer", "Architect", "Doctor", "Civil Engineer"],
            "required_keywords": ["psychology", "mental", "behavior", "counseling", "therapy", "human", "mind", "helping people", "help people", "mental health", "support", "care", "psychologist", "counselor", "therapist", "clinical psychology", "cognitive psychology", "social psychology", "developmental psychology", "forensic psychology", "sports psychology", "industrial psychology", "mental health counselor", "psychological research", "behavioral analysis", "psychological assessment", "psychological treatment", "psychological therapy", "psychological degree", "psychological career"]
        }
    }
    
    return guardrails.get(primary_domain, {
        "boost_majors": [],
        "boost_careers": [],
        "demote_majors": [],
        "demote_careers": [],
        "required_keywords": []
    })

def infer_preferences_from_text(text: str) -> Dict[str, str]:
    """Infer user preferences (no questions asked) from free-form text."""
    t = (text or "").lower()
    prefs: Dict[str, str] = {}
    # Study location preference - always local since we only have Cambodian universities
    prefs["locationPreference"] = "local"
    # Work style
    if any(k in t for k in ["team", "collaborat", "group"]):
        prefs["workStyle"] = "teamwork"
    elif any(k in t for k in ["independent", "alone", "solo", "individual"]):
        prefs["workStyle"] = "solo"
    else:
        prefs["workStyle"] = "mixed"
    # Learning style
    if any(k in t for k in ["hands-on", "hands on", "practical", "project", "build", "make"]):
        prefs["learningStyle"] = "practical"
    elif any(k in t for k in ["theory", "theoretical", "research", "academic"]):
        prefs["learningStyle"] = "theory"
    else:
        prefs["learningStyle"] = "mixed"
    # Career focus
    if any(k in t for k in ["startup", "entrepreneur", "founder"]):
        prefs["careerFocus"] = "entrepreneurship"
    elif any(k in t for k in ["industry", "company", "corporate"]):
        prefs["careerFocus"] = "industry"
    elif any(k in t for k in ["research", "lab", "academic", "university"]):
        prefs["careerFocus"] = "research"
    else:
        prefs["careerFocus"] = "industry"
    return prefs