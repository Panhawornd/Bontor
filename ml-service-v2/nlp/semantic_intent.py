"""
Semantic Intent Detection Module
Uses SBERT embeddings + contextual keyword matching for accurate intent detection

Features:
1. SBERT embeddings for semantic similarity matching
2. Contextual keyword combinations for precision disambiguation
3. Multi-signal fusion for accurate recommendations
4. Smart disambiguation for ambiguous terms (e.g., "design" types)
"""
import logging
import re
import numpy as np
from typing import Dict, List, Tuple, Set, Optional
from functools import lru_cache

logger = logging.getLogger(__name__)


class SemanticIntentDetector:
    """
    Semantic intent detector using hybrid approach:
    1. Contextual keyword rules for high-precision matching
    2. SBERT embeddings for fuzzy semantic similarity
    3. Combined signal fusion for optimal accuracy
    """
    
    # Class-level cache for embeddings
    _concept_embeddings = None
    _encoder = None
    
    # ========================================================================
    # CONTEXTUAL RULES - High-precision disambiguation using keyword combos
    # ========================================================================
    # These are checked FIRST - if user says "web design" we KNOW they mean UX/UI
    CONTEXTUAL_RULES = {
        # ===================== DESIGN DISAMBIGUATION =====================
        "web_design": {
            "triggers": ["web design", "website design", "ui design", "ux design", 
                        "user interface", "user experience", "app design", "mobile design",
                        "design app", "design website", "design interface"],
            "context_words": ["web", "website", "app", "ui", "ux", "user", "interface", 
                            "digital", "mobile", "online", "responsive", "wireframe"],
            "majors": [("UX/UI Design", 6.0), ("Software Engineering", 4.5), ("Graphic Design", 4.0)]
        },
        "building_design": {
            "triggers": ["building design", "architectural design", "design building", 
                        "design house", "design buildings", "design architecture",
                        "design structures", "structural design"],
            "context_words": ["building", "buildings", "house", "houses", "structure", 
                            "architect", "construction", "city", "urban", "space", 
                            "floor plan", "blueprint", "interior", "exterior"],
            "majors": [("Architecture", 6.0), ("Civil Engineering", 5.0)]
        },
        "graphic_design": {
            "triggers": ["graphic design", "visual design", "logo design", "poster design",
                        "design logo", "design poster", "design graphics", "illustration design"],
            "context_words": ["graphic", "graphics", "logo", "poster", "visual", "art", 
                            "artistic", "creative", "illustration", "brand", "branding",
                            "photoshop", "illustrator", "typography"],
            "majors": [("Graphic Design", 6.0), ("UX/UI Design", 4.0)]
        },
        "product_design": {
            "triggers": ["product design", "industrial design", "design product", "3d design"],
            "context_words": ["product", "industrial", "object", "furniture", "physical", 
                            "3d", "prototype", "manufacturing", "ergonomic"],
            "majors": [("Mechanical Engineering", 5.5), ("UX/UI Design", 4.5), ("Architecture", 4.0)]
        },
        "fashion_design": {
            "triggers": ["fashion design", "clothing design", "design clothes", "design fashion"],
            "context_words": ["fashion", "clothes", "clothing", "fabric", "textile", 
                            "wear", "dress", "garment", "apparel"],
            "majors": [("Graphic Design", 5.0)]
        },
        
        # ===================== CAREER-SPECIFIC DETECTION =====================
        "doctor_medical": {
            "triggers": ["be a doctor", "become a doctor", "medical doctor", "become physician",
                        "save lives", "treat patients", "work in hospital", "surgeon"],
            "context_words": ["doctor", "physician", "surgeon", "medical", "patient", 
                            "hospital", "clinic", "heal", "cure", "treat", "diagnosis",
                            "healthcare", "medicine", "surgery"],
            "majors": [("Medicine", 6.0)]
        },
        "pharmacist": {
            "triggers": ["pharmacist", "pharmacy", "pharmaceutical", "drug development"],
            "context_words": ["pharma", "drug", "medication", "pill", "prescription", 
                            "dispense", "pharmaceutical"],
            "majors": [("Pharmacology", 6.0), ("Medicine", 4.0)]
        },
        "dentist": {
            "triggers": ["dentist", "dental", "teeth", "orthodontist"],
            "context_words": ["dental", "teeth", "tooth", "oral", "mouth", "dentistry"],
            "majors": [("Dentistry", 6.0), ("Medicine", 4.0)]
        },
        
        # ===================== ENGINEERING SPECIFIC =====================
        "software_dev": {
            "triggers": ["software developer", "software engineer", "programmer", "coder",
                        "build apps", "create software", "develop applications", "write code"],
            "context_words": ["software", "code", "coding", "program", "programming", 
                            "developer", "app", "application", "computer", "tech",
                            "algorithm", "debug", "deploy"],
            "majors": [("Software Engineering", 6.0), ("Data Science", 4.5), ("Cybersecurity", 4.0)]
        },
        "mechanical_engineer": {
            "triggers": ["mechanical engineer", "build machines", "design machines", 
                        "work with machines", "automotive engineer", "robotics engineer"],
            "context_words": ["machine", "mechanical", "robot", "engine", "motor", 
                            "gear", "mechanism", "automotive", "car", "vehicle",
                            "manufacturing", "mechanics"],
            "majors": [("Mechanical Engineering", 6.0), ("Electrical Engineering", 4.0)]
        },
        "electrical_engineer": {
            "triggers": ["electrical engineer", "electronics", "circuit design", "power systems"],
            "context_words": ["electric", "circuit", "electron", "power", "voltage", 
                            "current", "wire", "semiconductor", "microchip"],
            "majors": [("Electrical Engineering", 6.0), ("Mechanical Engineering", 4.0)]
        },
        "civil_engineer": {
            "triggers": ["civil engineer", "build bridges", "build roads", "construction engineer",
                        "infrastructure", "structural engineer"],
            "context_words": ["bridge", "road", "highway", "infrastructure", "construction", 
                            "concrete", "steel", "structural"],
            "majors": [("Civil Engineering", 6.0), ("Architecture", 4.5)]
        },
        
        # ===================== BUSINESS & FINANCE =====================
        "entrepreneur": {
            "triggers": ["start a business", "entrepreneur", "startup", "business owner",
                        "own company", "run a company", "founder"],
            "context_words": ["startup", "entrepreneur", "business", "company", "venture", 
                            "innovation", "market", "founder", "ceo"],
            "majors": [("Business Administration", 6.0), ("Business Management", 5.5), ("Finance", 4.5)]
        },
        "finance_investor": {
            "triggers": ["investment", "investor", "stock market", "trading", "financial analyst",
                        "investment banker", "portfolio manager"],
            "context_words": ["invest", "stock", "trading", "bank", "financial", "money", 
                            "capital", "asset", "portfolio", "market"],
            "majors": [("Finance", 6.0), ("Business Administration", 4.5)]
        },
        "accountant": {
            "triggers": ["accountant", "accounting", "auditor", "bookkeeper", "tax"],
            "context_words": ["account", "audit", "tax", "bookkeep", "ledger", 
                            "balance sheet", "financial statement"],
            "majors": [("Finance", 6.0), ("Business Administration", 4.0)]
        },
        "marketer": {
            "triggers": ["marketing", "marketer", "advertiser", "brand manager", 
                        "digital marketing", "social media marketing"],
            "context_words": ["market", "advertis", "brand", "campaign", "social media", 
                            "content", "seo", "digital marketing", "promotion"],
            "majors": [("Marketing", 6.0), ("Business Administration", 4.5), ("Graphic Design", 4.0)]
        },
        
        # ===================== CREATIVE & ARTS =====================
        "artist": {
            "triggers": ["be an artist", "become artist", "fine arts", "visual artist"],
            "context_words": ["paint", "drawing", "sketch", "canvas", "artistic", 
                            "gallery", "exhibition", "museum", "sculpture", "art"],
            "majors": [("Graphic Design", 5.5), ("Architecture", 4.0)]
        },
        
        # ===================== DATA & AI =====================
        "data_scientist": {
            "triggers": ["data scientist", "data science", "machine learning", "ai engineer",
                        "artificial intelligence", "data analyst", "big data"],
            "context_words": ["data", "analytics", "machine learning", "ai", "artificial", 
                            "intelligence", "algorithm", "model", "predict", "statistics"],
            "majors": [("Data Science", 6.0), ("Software Engineering", 4.5), ("Finance", 4.0)]
        },
        
        # ===================== LAW & POLITICS =====================
        "lawyer": {
            "triggers": ["lawyer", "attorney", "legal", "law school", "be a lawyer",
                        "work in law", "court", "judge"],
            "context_words": ["law", "lawyer", "attorney", "court", "legal", "justice", 
                            "rights", "constitution", "judge", "litigation"],
            "majors": [("Law", 6.0), ("International Relations", 4.0)]
        },
        "diplomat": {
            "triggers": ["diplomat", "diplomacy", "foreign affairs", "international relations",
                        "ambassador", "work at embassy"],
            "context_words": ["diplomat", "embassy", "foreign", "international", "relations",
                            "politics", "government", "affairs"],
            "majors": [("International Relations", 6.0), ("Law", 4.5)]
        },
        
        # ===================== SECURITY =====================
        "cybersecurity": {
            "triggers": ["cybersecurity", "cyber security", "hacker", "ethical hacking",
                        "security analyst", "information security", "penetration testing"],
            "context_words": ["hack", "security", "cyber", "protect", "encrypt", 
                            "firewall", "malware", "virus", "breach", "threat"],
            "majors": [("Cybersecurity", 6.0), ("Software Engineering", 4.5)]
        },
        
        # ===================== EDUCATION & HELPING =====================
        "teacher": {
            "triggers": ["teacher", "teaching", "educator", "teach students", "work in school",
                        "become a teacher", "professor"],
            "context_words": ["teach", "teacher", "school", "student", "education", 
                            "classroom", "learn", "instruct", "tutor", "professor"],
            "majors": [("Education", 6.0), ("Psychology", 4.0)]
        },
        "therapist": {
            "triggers": ["therapist", "psychologist", "counselor", "mental health",
                        "help people emotionally", "psychology", "psychiatrist"],
            "context_words": ["therapy", "counsel", "mental health", "psychology", 
                            "emotional", "anxiety", "depression", "behavior", "mind"],
            "majors": [("Psychology", 6.0), ("Medicine", 4.0)]
        }
    }
    
    # ========================================================================
    # SEMANTIC CONCEPTS - Fuzzy matching for natural language
    # ========================================================================
    SUBJECT_CONCEPTS = {
        "mathematics": {
            "phrases": [
                "I love mathematics and numbers",
                "I enjoy solving math problems and equations",
                "calculus algebra statistics probability",
                "I'm good at mathematical calculations and analysis",
                "I like working with formulas and numerical data"
            ],
            "majors": [
                ("Data Science", 5.0),
                ("Software Engineering", 4.5),
                ("Finance", 4.5),
                ("Electrical Engineering", 4.0),
                ("Mechanical Engineering", 4.0),
            ]
        },
        "physics": {
            "phrases": [
                "I love physics and mechanics",
                "I enjoy understanding forces motion and energy",
                "electricity magnetism thermodynamics optics",
                "I'm fascinated by how the physical world works",
                "I like physics experiments and theories"
            ],
            "majors": [
                ("Electrical Engineering", 5.0),
                ("Mechanical Engineering", 5.0),
                ("Civil Engineering", 4.5),
                ("Architecture", 4.0),
            ]
        },
        "chemistry": {
            "phrases": [
                "I love chemistry and chemical reactions",
                "I enjoy working in laboratories with chemicals",
                "molecules compounds elements periodic table",
                "I'm interested in how substances interact and react",
                "I like organic and inorganic chemistry"
            ],
            "majors": [
                ("Pharmacology", 5.0),
                ("Medicine", 4.5),
                ("Dentistry", 4.0),
            ]
        },
        "biology": {
            "phrases": [
                "I love biology and living organisms",
                "I enjoy studying the human body anatomy and physiology",
                "genetics cells organisms ecosystems evolution",
                "I'm fascinated by how living things work",
                "I like learning about life sciences"
            ],
            "majors": [
                ("Medicine", 5.0),
                ("Pharmacology", 4.5),
                ("Dentistry", 4.0),
                ("Psychology", 3.5),
            ]
        },
        "english": {
            "phrases": [
                "I love English literature and writing",
                "I enjoy reading books and writing essays",
                "grammar vocabulary creative writing storytelling",
                "I'm good at expressing ideas in words",
                "I like communication and language arts"
            ],
            "majors": [
                ("International Relations", 5.0),
                ("Law", 4.5),
                ("Education", 4.0),
                ("Marketing", 4.0),
            ]
        },
        "history": {
            "phrases": [
                "I love history and learning about the past",
                "I enjoy studying civilizations and historical events",
                "ancient history world history cultural heritage",
                "I'm fascinated by how societies evolved",
                "I like understanding historical context"
            ],
            "majors": [
                ("International Relations", 5.0),
                ("Law", 4.5),
                ("Education", 4.0),
            ]
        }
    }
    
    SKILL_CONCEPTS = {
        "programming": {
            "phrases": [
                "I love coding and programming computers",
                "I enjoy writing software and building applications",
                "debugging algorithms development coding languages",
                "I'm good at computer programming and logic",
                "I like creating software and solving coding problems"
            ],
            "majors": [
                ("Software Engineering", 5.0),
                ("Data Science", 4.5),
                ("Cybersecurity", 4.0),
            ]
        },
        "design_general": {
            "phrases": [
                "I love design and creating beautiful things",
                "I enjoy making things look visually appealing",
                "aesthetics visual design creativity artistic",
                "I'm good at design and visual composition",
                "I like creating and designing"
            ],
            "majors": [
                ("Graphic Design", 4.5),
                ("UX/UI Design", 4.5),
                ("Architecture", 4.0),
            ]
        },
        "architecture_skills": {
            "phrases": [
                "I love buildings and architectural design",
                "I'm fascinated by structures and how buildings are designed",
                "designing houses buildings skyscrapers construction",
                "I want to be an architect and design buildings",
                "I'm passionate about architecture and spatial design"
            ],
            "majors": [
                ("Architecture", 5.0),
                ("Civil Engineering", 4.5),
            ]
        },
        "leadership": {
            "phrases": [
                "I love leading teams and managing people",
                "I enjoy being in charge and making decisions",
                "management leadership strategy organization",
                "I'm good at directing and coordinating teams",
                "I like taking responsibility and guiding others"
            ],
            "majors": [
                ("Business Management", 5.0),
                ("Business Administration", 4.5),
                ("International Relations", 4.0),
            ]
        },
        "helping_people": {
            "phrases": [
                "I love helping people and caring for others",
                "I enjoy supporting and counseling people",
                "empathy compassion care mental health support",
                "I want to make a difference in people's lives",
                "I like helping others solve their problems"
            ],
            "majors": [
                ("Psychology", 5.0),
                ("Medicine", 4.5),
                ("Education", 4.5),
            ]
        },
        "analytical": {
            "phrases": [
                "I love analyzing data and finding patterns",
                "I enjoy research and solving complex problems",
                "data analysis statistics logical thinking research",
                "I'm good at critical thinking and analysis",
                "I like breaking down problems systematically"
            ],
            "majors": [
                ("Data Science", 5.0),
                ("Finance", 4.5),
                ("Psychology", 4.0),
            ]
        },
        "engineering_skills": {
            "phrases": [
                "I love building machines and mechanical systems",
                "I enjoy hands-on technical work with electronics",
                "circuits motors robots mechanical systems engineering",
                "I want to create and build technical things",
                "I like working with my hands on technical projects"
            ],
            "majors": [
                ("Mechanical Engineering", 5.0),
                ("Electrical Engineering", 5.0),
                ("Civil Engineering", 4.0),
            ]
        }
    }
    
    WORK_PREFERENCE_CONCEPTS = {
        "independent": {
            "phrases": [
                "I prefer working alone and independently",
                "I like solo work and being by myself",
                "remote work autonomy independent work style",
                "I don't like working in groups",
                "I do my best work when I'm alone"
            ],
            "majors": [
                ("Software Engineering", 5.0),
                ("Data Science", 4.5),
                ("Graphic Design", 4.0),
            ]
        },
        "teamwork": {
            "phrases": [
                "I love working with people in teams",
                "I enjoy collaboration and group work",
                "teamwork interaction communication cooperation",
                "I prefer working with others rather than alone",
                "I thrive in collaborative environments"
            ],
            "majors": [
                ("Business Administration", 5.0),
                ("Psychology", 4.5),
                ("Education", 4.5),
                ("Medicine", 4.0),
            ]
        },
        "outdoor": {
            "phrases": [
                "I prefer working outdoors in the field",
                "I don't like sitting at a desk all day",
                "field work site visits active work environment",
                "I want a job with physical activity and movement",
                "I like being outside and moving around"
            ],
            "majors": [
                ("Civil Engineering", 5.0),
                ("Architecture", 4.5),
            ]
        },
        "office": {
            "phrases": [
                "I prefer office work with computers",
                "I like desk jobs and stable environments",
                "corporate professional business setting office",
                "I want to work in a comfortable office environment",
                "I prefer structured work environments"
            ],
            "majors": [
                ("Finance", 4.5),
                ("Business Administration", 4.5),
                ("Software Engineering", 4.0),
            ]
        }
    }
    
    # Negative indicators
    NEGATIVE_PHRASES = [
        "I don't like", "I hate", "I dislike",
        "not interested in", "avoid", "bad at",
        "don't want", "never want", "anything but",
        "not for me", "boring", "terrible at"
    ]
    
    def __init__(self):
        """Initialize with SBERT encoder"""
        from nlp.sbert import SBERTEncoder
        if SemanticIntentDetector._encoder is None:
            SemanticIntentDetector._encoder = SBERTEncoder()
        self._precompute_embeddings()
    
    def _precompute_embeddings(self):
        """Pre-compute embeddings for all concept phrases"""
        if SemanticIntentDetector._concept_embeddings is not None:
            return
        
        logger.info("Pre-computing semantic concept embeddings...")
        SemanticIntentDetector._concept_embeddings = {}
        
        all_concepts = {
            "subjects": self.SUBJECT_CONCEPTS,
            "skills": self.SKILL_CONCEPTS,
            "preferences": self.WORK_PREFERENCE_CONCEPTS,
        }
        
        for category, concepts in all_concepts.items():
            SemanticIntentDetector._concept_embeddings[category] = {}
            for concept_name, data in concepts.items():
                # Encode all phrases and average them
                phrase_embeddings = [
                    SemanticIntentDetector._encoder.encode(phrase)
                    for phrase in data["phrases"]
                ]
                # Store average embedding as concept representation
                avg_embedding = np.mean(phrase_embeddings, axis=0)
                SemanticIntentDetector._concept_embeddings[category][concept_name] = {
                    "embedding": avg_embedding,
                    "majors": data["majors"]
                }
        
        # Pre-compute negative phrase embeddings
        neg_embeddings = [SemanticIntentDetector._encoder.encode(p) for p in self.NEGATIVE_PHRASES]
        SemanticIntentDetector._concept_embeddings["negative"] = np.mean(neg_embeddings, axis=0)
        
        logger.info("Semantic concept embeddings computed successfully")
    
    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """Compute cosine similarity between two vectors"""
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(np.dot(a, b) / (norm_a * norm_b))
    
    def _check_contextual_rules(self, text: str) -> Dict[str, float]:
        """
        PRECISION FIRST: Check explicit contextual rules for high-accuracy matching.
        This catches specific phrases like "web design" or "build machines".
        """
        text_lower = text.lower()
        boosts = {}
        matched_rules = []
        
        for rule_name, rule_data in self.CONTEXTUAL_RULES.items():
            # Check for direct trigger phrases
            trigger_match = any(trigger in text_lower for trigger in rule_data["triggers"])
            
            # Check for context word combinations
            context_words_found = sum(1 for word in rule_data["context_words"] if word in text_lower)
            strong_context = context_words_found >= 2
            
            if trigger_match or strong_context:
                matched_rules.append((rule_name, trigger_match, context_words_found))
                for major, boost in rule_data["majors"]:
                    current = boosts.get(major, 1.0)
                    # Triggers get full boost, context words get scaled boost
                    if trigger_match:
                        boosts[major] = max(current, boost)
                    else:
                        scaled_boost = boost * (context_words_found / 4)  # Scale by context strength
                        boosts[major] = max(current, scaled_boost)
        
        if matched_rules:
            logger.info(f"Contextual rules matched: {matched_rules}")
        
        return boosts
    
    def _detect_semantic_intent(self, text: str, threshold: float = 0.50) -> Dict[str, float]:
        """
        SEMANTIC FALLBACK: Use SBERT embeddings for fuzzy understanding.
        """
        if not text or not text.strip():
            return {}
        
        # Encode user text
        user_embedding = SemanticIntentDetector._encoder.encode(text.lower())
        
        # Check for negative sentiment
        neg_embedding = SemanticIntentDetector._concept_embeddings["negative"]
        neg_similarity = self._cosine_similarity(user_embedding, neg_embedding)
        is_negative = neg_similarity > 0.55
        
        boosts = {}
        detected_concepts = []
        
        # Check all concept categories
        for category in ["subjects", "skills", "preferences"]:
            concepts = SemanticIntentDetector._concept_embeddings[category]
            
            for concept_name, data in concepts.items():
                similarity = self._cosine_similarity(user_embedding, data["embedding"])
                
                if similarity >= threshold:
                    detected_concepts.append((concept_name, similarity, category))
                    
                    # Apply boosts based on similarity strength
                    for major, base_boost in data["majors"]:
                        # Scale boost by similarity
                        scaled_boost = base_boost * (similarity / 0.7)
                        scaled_boost = min(scaled_boost, base_boost)  # Cap at base boost
                        
                        if is_negative:
                            current = boosts.get(major, 1.0)
                            boosts[major] = max(0.2, current * 0.5)
                        else:
                            current = boosts.get(major, 1.0)
                            boosts[major] = max(current, scaled_boost)
        
        if detected_concepts:
            top_concepts = sorted(detected_concepts, key=lambda x: -x[1])[:5]
            logger.info(f"Semantic detection: {[(c, f'{s:.2f}') for c, s, _ in top_concepts]}")
        
        return boosts
    
    def detect_intent(self, text: str) -> Dict[str, float]:
        """
        MAIN ENTRY: Combines contextual rules + semantic understanding.
        
        Strategy:
        1. First check explicit contextual rules (high precision)
        2. Then use semantic similarity (fuzzy understanding)
        3. Merge boosts, preferring contextual when available
        """
        if not text or not text.strip():
            return {}
        
        logger.info(f"Detecting intent for: '{text[:100]}...' ")
        
        # Step 1: High-precision contextual matching
        contextual_boosts = self._check_contextual_rules(text)
        
        # Step 2: Semantic similarity matching
        semantic_boosts = self._detect_semantic_intent(text)
        
        # Step 3: Merge - contextual takes priority
        final_boosts = {}
        all_majors = set(contextual_boosts.keys()) | set(semantic_boosts.keys())
        
        for major in all_majors:
            ctx_boost = contextual_boosts.get(major, 0)
            sem_boost = semantic_boosts.get(major, 0)
            
            if ctx_boost > 0 and sem_boost > 0:
                # Both matched - combine with priority to contextual
                final_boosts[major] = max(ctx_boost, sem_boost * 0.8)
            elif ctx_boost > 0:
                final_boosts[major] = ctx_boost
            else:
                final_boosts[major] = sem_boost
        
        if final_boosts:
            sorted_boosts = sorted(final_boosts.items(), key=lambda x: -x[1])[:5]
            logger.info(f"Final intent boosts: {sorted_boosts}")
        
        return final_boosts
    
    def extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords from text"""
        if not text:
            return []
        
        important_words = {
            "math", "physics", "chemistry", "biology", "english", "history",
            "coding", "programming", "design", "architecture", "building",
            "leadership", "management", "research", "analysis", "data",
            "team", "alone", "people", "outdoor", "office", "computer",
            "machine", "robot", "creative", "help", "teach", "doctor",
            "lawyer", "engineer", "business", "finance", "art", "music"
        }
        
        text_lower = text.lower()
        return [w for w in important_words if w in text_lower]


# Singleton instance
_detector_instance = None

def get_semantic_detector() -> SemanticIntentDetector:
    """Get singleton instance of semantic detector"""
    global _detector_instance
    if _detector_instance is None:
        _detector_instance = SemanticIntentDetector()
    return _detector_instance
