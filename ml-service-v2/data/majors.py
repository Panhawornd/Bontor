"""
Major database with keywords, descriptions, and career paths
"""
MAJOR_DATABASE = {
    "Software Engineering": {
        "keywords": ["software", "programming", "coding", "developer", "apps", "python", "javascript", "backend", "frontend", "algorithm"],
        "required_subjects": ["math", "physics"],
        "description": "Study of software development life cycle, programming, and system architecture",
        "career_paths": ["Software Engineer", "Full Stack Developer", "Backend Developer", "Frontend Developer", "App Developer", "System Architect"]
    },
    "Medicine": {
        "keywords": ["doctor", "medical", "health", "biology", "anatomy", "patient", "hospital", "clinic", "helping people", "saving lives", "help people", "save lives", "care", "healing", "treatment", "cure", "medicine", "healthcare", "surgeon", "physician", "medical research", "diagnosis", "surgery", "pharmacology", "cardiology", "neurology", "pediatrics", "emergency medicine", "medical technology", "clinical", "therapeutic", "medical practice", "healthcare provider", "medical specialist", "medical school", "medical degree", "medical profession"],
        "required_subjects": ["biology", "chemistry", "math"],
        "description": "Study of human health, diseases, and medical treatment",
        "career_paths": ["Doctor", "Surgeon", "Medical Researcher", "Pharmacist", "Pediatrician", "Cardiologist", "Neurologist", "Emergency Medicine Physician", "Medical Specialist"]
    },
    "Electrical Engineering": {
        "keywords": ["electrical", "electronics", "electronic", "circuit", "power", "signal", "electrical engineering", "electrical engineer", "electrical systems", "electronic systems", "electrical design", "power systems", "electrical technology", "electrical equipment", "electrical installation", "electrical maintenance", "electrical safety", "electrical code", "electrical wiring", "electrical components", "electrical devices", "electrical machines", "electrical motors", "electrical generators", "electrical transformers", "electrical distribution", "electrical transmission", "electrical control", "electrical automation", "electrical instrumentation", "electrical measurement", "electrical testing", "electrical troubleshooting", "electrical repair", "electrical construction", "electrical project", "electrical consulting", "electrical research", "electrical development", "electrical innovation", "electrical technology", "electrical engineering degree", "electrical engineering career"],
        "required_subjects": ["math", "physics"],
        "description": "Design and development of electrical systems, electronics, and power systems",
        "career_paths": ["Electrical Engineer", "Electronics Engineer", "Power Systems Engineer", "Control Systems Engineer", "Embedded Systems Engineer", "Telecommunications Engineer", "Electrical Designer", "Electrical Project Manager"]
    },
    "Mechanical Engineering": {
        "keywords": ["mechanical", "machines", "robotics", "engine", "automotive", "thermodynamics", "manufacturing", "mechatronics"],
        "required_subjects": ["math", "physics"],
        "description": "Design, analysis, and manufacturing of mechanical systems and machines",
        "career_paths": ["Mechanical Engineer", "Design Engineer", "Manufacturing Engineer", "Robotics Engineer", "Automotive Engineer"]
    },
    "Civil Engineering": {
        "keywords": ["civil", "civil engineering", "civil engineer", "infrastructure", "bridges", "roads", "highways", "transportation", "construction", "structural", "large-scale construction", "public works", "connect communities", "civil construction", "civil infrastructure", "civil projects", "civil design", "civil technology", "civil systems", "civil structures", "civil buildings", "civil bridges", "civil roads", "civil highways", "civil transportation", "civil water", "civil drainage", "civil sewage", "civil environmental", "civil geotechnical", "civil structural", "civil materials", "civil surveying", "civil planning", "civil development", "civil maintenance", "civil repair", "civil renovation", "civil restoration", "civil preservation", "civil safety", "civil codes", "civil regulations", "civil compliance", "civil standards", "civil quality", "civil testing", "civil inspection", "civil supervision", "civil management", "civil consulting", "civil research", "civil innovation", "civil engineering degree", "civil engineering career"],
        "required_subjects": ["math", "physics"],
        "description": "Design and construction of infrastructure, buildings, and public works",
        "career_paths": ["Civil Engineer", "Structural Engineer", "Transportation Engineer", "Water Resources Engineer", "Environmental Engineer", "Geotechnical Engineer", "Construction Engineer", "Civil Project Manager"]
    },
    "Chemical Engineering": {
        "keywords": ["chemical", "chemical engineering", "chemical engineer", "chemical reactions", "chemical manufacturing", "chemical processing", "industrial plants", "chemical reactors", "chemistry labs", "chemical synthesis", "petroleum"],
        "required_subjects": ["math", "physics", "chemistry"],
        "description": "Design and operation of chemical processes and industrial systems",
        "career_paths": ["Chemical Engineer", "Process Engineer", "Plant Engineer", "Petroleum Engineer"]
    },
    "Business Administration": {
        "keywords": ["business administration", "accounting", "entrepreneurship", "run a company", "startup", "operating a business", "finance", "marketing", "business economics", "corporate strategy", "company leader", "business degree"],
        "required_subjects": ["math", "english"],
        "description": "Study of business operations, management, and organizational behavior",
        "career_paths": ["Manager", "Entrepreneur", "Financial Analyst", "Marketing Manager", "CEO", "Business Consultant", "Project Manager", "Sales Manager", "Human Resources Manager"]
    },
    "Data Science": {
        "keywords": ["data science", "data scientist", "big data", "data patterns", "analytics", "statistics", "python", " r ", "sql", "data mining", "predictive modeling", "intelligence", "datasets"],
        "required_subjects": ["math", "physics"],
        "description": "Extract insights from data using statistical and computational methods",
        "career_paths": ["Data Scientist", "Data Analyst", "Machine Learning Engineer", "Data Engineer"]
    },
    "Psychology": {
        "keywords": ["psychology", "mental", "behavior", "counseling", "therapy", "human", "mind", "helping people", "help people", "understanding people", "understand people", "human behavior", "people", "mental health", "support", "care", "psychologist", "counselor", "therapist", "clinical psychology", "cognitive psychology", "social psychology", "developmental psychology", "forensic psychology", "sports psychology", "industrial psychology", "mental health counselor", "psychological research", "behavioral analysis", "psychological assessment", "psychological treatment", "psychological therapy", "psychological degree", "psychological career"],
        "required_subjects": ["biology", "english"],
        "description": "Study of human behavior, cognition, and mental processes",
        "career_paths": ["Psychologist", "Counselor", "Therapist", "Researcher", "School Psychologist", "Forensic Psychologist", "Sports Psychologist", "Industrial Psychologist", "Mental Health Counselor"]
    },
    "Education": {
        "keywords": ["teaching", "education", "teacher", "school", "learning", "students", "classroom", "helping people", "help people", "teach", "mentor", "guide", "educator", "professor", "principal", "curriculum", "educational technology", "special education", "early childhood education", "educational administration", "educational policy", "teacher training", "educational research", "academic", "pedagogy", "instructional design", "educational leadership", "school counselor", "educational consultant", "education degree", "education career"],
        "required_subjects": ["english", "math"],
        "description": "Preparation for teaching and educational leadership roles",
        "career_paths": ["Teacher", "Principal", "Educational Consultant", "Curriculum Developer", "University Professor", "Special Education Teacher", "Educational Technology Specialist", "School Counselor", "Training and Development Manager"]
    },
    "International Relations": {
        "keywords": ["international", "diplomacy", "politics", "global", "foreign", "policy", "government", "diplomat", "foreign service", "international development", "embassy", "consulate", "peacekeeping", "international trade", "international security", "international law", "global affairs", "foreign policy", "international organizations", "united nations", "ngo", "humanitarian", "international relations degree", "international relations career", "global politics", "international cooperation", "debating", "world affairs", "global issues"],
        "required_subjects": ["history", "english"],
        "description": "Study of global politics, diplomacy, and international cooperation",
        "career_paths": ["Diplomat", "Policy Analyst", "International Consultant", "NGO Worker", "Foreign Service Officer", "International Development Specialist", "Global Affairs Analyst", "International Trade Specialist", "Peacekeeping Officer"]
    },
    "Architecture": {
        "keywords": ["architecture", "buildings", "floor plans", "blueprint", "urban planning", "construction design", "structural aesthetics", "spatial design"],
        "required_subjects": ["math", "physics"],
        "description": "Art and science of designing buildings and structures",
        "career_paths": ["Architect", "Urban Planner", "Interior Designer", "Construction Manager", "Landscape Architect", "Project Architect", "Sustainable Design Specialist", "Historic Preservation Architect", "Commercial Architect", "Residential Architect"]
    },
    "Dentistry": {
        "keywords": ["dentistry", "dentist", "dental", "teeth", "oral", "health", "mouth", "tooth", "gum", "dental care", "orthodontist", "oral surgery", "dental hygiene", "dental clinic", "oral health", "dental treatment", "dental procedures", "dental technology", "cosmetic dentistry", "dental implants", "periodontics", "endodontics", "prosthodontics", "pediatric dentistry", "dental research", "dental materials", "dental degree", "dental career", "dental profession"],
        "required_subjects": ["biology", "chemistry", "math"],
        "description": "Study of oral health, dental care, and treatment of teeth and gums",
        "career_paths": ["Dentist", "Orthodontist", "Oral Surgeon", "Dental Hygienist", "Dental Assistant", "Periodontist", "Endodontist", "Prosthodontist", "Pediatric Dentist", "Cosmetic Dentist"]
    },
    "Law": {
        "keywords": ["law", "legal", "lawyer", "justice", "court", "rights", "legal system", "jurisprudence", "advocate", "attorney", "legal practice", "litigation", "legal advice", "legal research", "constitutional", "criminal law", "civil law", "legal profession", "criminal defense", "corporate law", "family law", "environmental law", "intellectual property", "international law", "immigration law", "human rights law", "legal aid", "contract law", "legal degree", "legal career", "legal profession", "arguing", "debating", "rules", "logic", "persuasion"],
        "required_subjects": ["english", "history"],
        "description": "Study of legal systems, jurisprudence, and legal practice",
        "career_paths": ["Lawyer", "Judge", "Legal Advisor", "Prosecutor", "Legal Researcher", "Corporate Counsel", "Public Defender", "Legal Consultant", "Criminal Defense Attorney", "Family Lawyer", "Environmental Lawyer", "Intellectual Property Lawyer"]
    },
    "Pharmacy": {
        "keywords": ["pharmacy", "pharmacist", "medication", "drugs", "pharmaceutical", "prescription", "pharmacology", "dispensing", "dosage", "medical drugs", "chemists", "pharmacy practice", "clinical pharmacy", "pharmaceutical chemistry", "pharmaceutical technology", "pharmaceutical manufacturing"],
        "required_subjects": ["biology", "chemistry", "math"],
        "description": "Study of medications, drug development, and pharmaceutical care",
        "career_paths": ["Pharmacist", "Pharmaceutical Researcher", "Clinical Pharmacist", "Pharmaceutical Sales Representative", "Pharmaceutical Marketing Manager", "Pharmaceutical Quality Assurance Manager", "Pharmaceutical Regulatory Affairs Specialist", "Pharmaceutical Manufacturing Manager", "Pharmaceutical Consultant", "Pharmaceutical Analyst"]
    },
    "Business Management": {
        "keywords": ["business management", "leadership", "team management", "operations management", "organizational leadership", "supervision", "managing teams", "business operations", "resource management", "strategic leadership", "team leader", "management skills"],
        "required_subjects": ["math", "english"],
        "description": "Study of business management, leadership, and organizational behavior",
        "career_paths": ["Business Manager", "Operations Manager", "Project Manager", "Team Leader", "Department Manager", "General Manager", "Management Consultant", "Business Analyst", "Management Trainee", "Executive Manager"]
    },
    "Finance": {
        "keywords": ["finance", "financial", "investment", "banking", "financial analysis", "financial planning", "financial management", "financial services", "financial markets", "financial instruments", "financial modeling", "financial reporting", "financial accounting", "financial risk", "financial strategy", "financial consulting", "financial advisor", "financial analyst", "financial manager", "financial controller", "financial director", "financial executive", "financial degree", "financial career", "financial profession", "corporate finance", "personal finance", "public finance", "international finance", "quantitative finance", "financial engineering"],
        "required_subjects": ["math", "english"],
        "description": "Study of financial systems, investment, and financial management",
        "career_paths": ["Financial Analyst", "Investment Banker", "Financial Advisor", "Financial Manager", "Financial Controller", "Investment Manager", "Risk Manager", "Financial Consultant", "Corporate Finance Manager", "Portfolio Manager"]
    },
    "UX/UI Design": {
        "keywords": ["ux design", "ui design", "user interface", "user experience", "interface design", "figma", "wireframe", "prototype", "usability", "interaction design", "adobe xd", "product design", "ux designer", "ui designer"],
        "required_subjects": ["english", "math"],
        "description": "Design of user interfaces and experiences for digital products, focusing on usability and user satisfaction",
        "career_paths": ["UX Designer", "UI Designer", "Product Designer", "UX Researcher", "Interaction Designer"]
    },
    "Graphic Design": {
        "keywords": ["graphic design", "graphic designer", "visual design", "branding", "logo", "poster", "illustrator", "photoshop", "indesign", "typography", "layout", "print design", "marketing design", "visual identity", "art director"],
        "required_subjects": ["english", "history"],
        "description": "Visual communication and design for print and digital media, including branding, marketing materials, and digital graphics",
        "career_paths": ["Graphic Designer", "Brand Designer", "Visual Designer", "Art Director", "Creative Director", "Marketing Designer", "Illustrator", "Digital Designer", "Print Designer", "Packaging Designer"]
    },
    "Cybersecurity": {
        "keywords": ["cybersecurity", "security", "hacking", "encryption", "network security", "privacy", "protecting data", "puzzles", "hidden weaknesses", "staying invisible", "ethical hacking", "digital safety", "firewall", "cyber", "security analyst", "information security"],
        "required_subjects": ["math", "physics"],
        "description": "Protection of computer systems and networks from information disclosure, theft, or damage",
        "career_paths": ["Cybersecurity Analyst", "Security Engineer", "Ethical Hacker", "Information Security Manager", "Network Security Architect", "Incident Responder"]
    },
    "Telecommunication and Networking": {
        "keywords": ["telecommunication", "networking", "network engineer", "cisco", "routing", "switching", "internet protocol", "ip", "transmission", "signals", "5g", "wireless", "telecom", "infrastructure", "connectivity", "fiber optics", "network administration"],
        "required_subjects": ["math", "physics"],
        "description": "Study of network architecture, data transmission, and communication systems",
        "career_paths": ["Network Engineer", "Telecom Engineer", "Network Administrator", "Systems Engineer", "Connectivity Specialist"]
    }
}
