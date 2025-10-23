"""
Constants and configuration values
"""
SCIENCE_SUBJECTS = {"math", "physics", "chemistry", "biology"}
LANG_SUBJECTS = {"khmer", "english"}
SOCIAL_SUBJECTS = {"history"}

# Subject max scores for BacII
SUBJECT_MAX_SCORES = {
    "math": 125,
    "physics": 75,
    "chemistry": 75,
    "biology": 75,
    "khmer": 75,
    "english": 50,
    "history": 50
}

# Enhanced domain keywords with strict boundaries for better major/career distinction
DOMAIN_KEYWORDS = {
    # Engineering Domains
    "electrical_engineering": ["electrical", "electric", "electronic", "electronics", "circuit", "power", "embedded", "signal", "voltage", "current", "resistor", "capacitor", "transformer", "generator", "motor", "wiring", "electrical systems", "power systems", "control systems", "telecommunication"],
    "mechanical_engineering": ["mechanical", "mechanical machine", "mechanical mechanism", "manufacturing", "mechatronics", "robotics", "automation", "mechanical systems", "engines", "gears", "bearings", "hydraulics", "pneumatics", "thermodynamics", "mechanical design", "building machine", "building machines", "constructing machine", "constructing machines", "building mechanical", "building engines", "building gears", "flight", "space", "aircraft", "rocket", "rockets", "aerospace", "aviation", "airplane", "airplanes", "helicopter", "helicopters", "satellite", "satellites", "spacecraft", "engineering challenges", "designed", "designing"],
    "civil_engineering": ["civil", "infrastructure", "bridge", "road", "highway", "dam", "tunnel", "foundation", "structural engineering", "construction engineering", "transportation", "water systems", "sewage", "public works"],
    "chemical_engineering": ["chemical", "chemistry", "process", "reaction", "materials", "chemical processes", "petrochemical", "pharmaceutical", "polymer", "biochemical", "process engineering", "chemical plants"],
    
    # Technology Domains
    "software_engineering": ["software", "coding", "programming", "developer", "programmer", "computer", "application", "software development", "web development", "mobile apps", "algorithms", "data structures", "software architecture", "building software", "building applications", "building programs"],
    "data_science": ["data", "analytics", "ai", "ml", "machine learning", "artificial intelligence", "pattern", "statistics", "data analysis", "big data", "data mining", "predictive modeling", "data visualization", "intelligent systems", "building intelligent systems", "programming", "data analysis"],
    
    # Medical Domains
    "medicine": ["medical", "doctor", "medicine", "health", "anatomy", "patient", "clinical", "hospital", "physician", "surgery", "diagnosis", "treatment", "medical practice", "healthcare"],
    "dentistry": ["dentistry", "dentist", "dental", "teeth", "oral", "tooth", "gum", "dental care", "orthodontist", "oral surgery", "dental hygiene"],
    
    # Social Sciences
    "psychology": ["psychology", "psychologist", "mental", "behavior", "counseling", "therapy", "mental health", "psychological", "cognitive", "behavioral", "clinical psychology", "understanding people", "thoughts", "emotions", "people's thoughts", "people's emotions", "helping people", "mental wellbeing", "human behavior", "listening", "advice", "mental health", "support", "care", "understanding", "people", "feelings", "mind", "human", "help people", "helping", "wellbeing"],
    "business": ["business", "entrepreneur", "management", "finance", "marketing", "administration", "commerce", "corporate", "startup", "investment", "business strategy", "business management", "leadership", "team management", "organizational management", "business leadership", "management skills", "management degree", "management career", "management profession", "corporate management", "strategic management", "operations management", "project management", "human resource management", "financial management", "marketing management", "management consulting", "management training", "management development", "management strategy", "management planning", "management decision", "management control", "management coordination", "management supervision", "management direction", "management guidance", "management oversight", "financial", "financial markets", "money", "banking", "financial analysis", "financial planning", "financial management", "financial services", "financial markets", "financial instruments", "financial modeling", "financial reporting", "financial accounting", "financial risk", "financial strategy", "financial consulting", "financial advisor", "financial analyst", "financial manager", "financial controller", "financial director", "financial executive", "financial degree", "financial career", "financial profession", "corporate finance", "personal finance", "public finance", "international finance", "quantitative finance", "financial engineering"],
    
    # Design Domains
    "design": ["ux", "ui", "user experience", "user interface", "wireframe", "prototype", "figma", "adobe xd", "sketch", "usability", "interaction design", "product design", "graphic design", "visual design", "logo", "branding", "photoshop", "illustrator", "indesign", "typography", "layout", "poster", "graphic designer", "ux designer", "ui designer", "brand designer", "visual designer", "art director", "creative director", "design", "designer", "creative design", "digital design", "web design", "app design", "mobile design"],
    "architecture": ["architecture", "architect", "building design", "buildings", "sustainable", "green", "cad", "drawing", "blueprint", "creative", "visual", "space", "urban planning", "interior design", "landscape architecture", "real estate", "housing", "skyscraper", "monument", "facade", "floor plan", "architectural design", "structural design"],
    
    # Education
    "education": ["teaching", "education", "teacher", "school", "learning", "students", "classroom", "teach", "mentor", "guide", "educator", "professor", "principal", "curriculum", "teach", "educate", "next generation", "teaching", "education", "teacher", "school", "learning", "students", "classroom", "teach", "mentor", "guide", "educator", "professor", "principal", "curriculum", "teach", "educate", "next generation"],
    
    # Law
    "law": ["law", "legal", "lawyer", "justice", "court", "rights", "legal system", "jurisprudence", "advocate", "attorney", "legal practice", "litigation", "legal advice", "legal research"],
    
    # International Relations
    "international_relations": ["international", "diplomacy", "politics", "global", "foreign", "policy", "government", "diplomat", "foreign service", "international development", "embassy", "consulate", "peacekeeping", "international trade", "international security", "international law"]
}

# Khmer to English translation mapping
KHMER_TO_ENGLISH = {
    'វិទ្យាសាស្ត្រកុំព្យូទ័រ': 'computer science',
    'វេជ្ជសាស្ត្រ': 'medicine',
    'វិស្វកម្ម': 'engineering',
    'ពាណិជ្ជកម្ម': 'business',
    'សិល្បៈ': 'arts',
    'អប់រំ': 'education',
    'ជំនាញ': 'skills',
    'ការងារ': 'work job career',
    'សុបិន្ត': 'dream',
    'ចង់': 'want desire',
    'ចូលចិត្ត': 'like love enjoy',
    'ជួយ': 'help',
    'មនុស្ស': 'people',
    'ព្រះរាជាណាចក្រកម្ពុជា': 'cambodia',
    'ភាសាខ្មែរ': 'khmer language',
    'ភាសាអង់គ្លេស': 'english language',
    'គណិតវិទ្យា': 'mathematics math',
    'រូបវិទ្យា': 'physics',
    'គីមីវិទ្យា': 'chemistry',
    'ជីវវិទ្យា': 'biology',
    'ប្រវត្តិសាស្ត្រ': 'history',
    'វិទ្យាស្ថាន': 'university institute',
    'សាកលវិទ្យាល័យ': 'university',
    'វិទ្យាល័យ': 'college',
    'សាលា': 'school',
    'អ្នកជំនាញ': 'expert specialist',
    'អ្នកវិជ្ជាជីវៈ': 'professional',
    'អ្នកវិជ្ជាជីវៈវេជ្ជសាស្ត្រ': 'doctor physician',
    'អ្នកវិជ្ជាជីវៈវិស្វករ': 'engineer',
    'អ្នកវិជ្ជាជីវៈគ្រូ': 'teacher',
    'អ្នកវិជ្ជាជីវៈពាណិជ្ជកម្ម': 'business professional',
    'អ្នកវិជ្ជាជីវៈសិល្បៈ': 'artist',
    'អ្នកវិជ្ជាជីវៈច្បាប់': 'lawyer',
    'អ្នកវិជ្ជាជីវៈវិស្វករស្ថាបត្យកម្ម': 'architect',
    'អ្នកវិជ្ជាជីវៈធ្មេញ': 'dentist'
}