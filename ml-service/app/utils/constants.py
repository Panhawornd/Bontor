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

# Enhanced domain keywords with strict boundaries - NO OVERLAP
DOMAIN_KEYWORDS = {
    # Engineering Domains
    "electrical_engineering": ["electrical", "electronics", "circuit", "power", "embedded", "signal", "voltage", "current"],
    
    "mechanical_engineering": ["mechanical", "manufacturing", "mechatronics", "robotics", "engines", "gears", "aerospace", "aircraft", "rocket"],
    
    "civil_engineering": ["civil engineering", "infrastructure", "bridge", "construction", "structural", "transportation", "geotechnical"],
    
    "chemical_engineering": ["chemical", "petrochemical", "pharmaceutical", "polymer", "biochemical"],
    
    # Technology Domains
    "software_engineering": ["software", "coding", "programming", "developer", "application", "backend", "frontend", " api "],
    
    "data_science": ["data science", "analytics", "statistics", "machine learning", "data mining", "predictive", "big data"],
    
    # Medical Domains
    "medicine": ["medical", "doctor", "physician", "clinical", "hospital", "surgery", "diagnosis", "healthcare"],
    
    "dentistry": ["dentistry", "dentist", "dental", "teeth", "oral", "orthodontist"],
    
    # Social Sciences
    "psychology": ["psychology", "psychologist", "mental health", "counseling", "therapy", "behavioral"],
    
    "business": ["business", "entrepreneur", "management", "finance", "marketing", "corporate", "investment"],
    
    # Design Domains
    "design": ["ux", "ui", "user experience", "wireframe", "figma", "adobe xd", "graphic design", "visual design", "logo", "branding", "photoshop", "illustrator", "web interface", "interface design", "digital interface", "designing interface", "web design", "interface"],
    
    "architecture": ["architecture", "architect", "architectural", "building", "urban planning", "landscape", "blueprint", "cad"],
    
    # Others
    "education": ["teaching", "teacher", "educator", "classroom", "curriculum"],
    
    "law": ["law", "legal", "lawyer", "justice", "court", "attorney"],
    
    "international_relations": ["international relations", "diplomacy", "foreign policy", "global politics"]
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