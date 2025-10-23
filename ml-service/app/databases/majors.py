"""
Major database with keywords, descriptions, and career paths
"""
MAJOR_DATABASE = {
    "Computer Science": {
        "keywords": ["programming", "computer", "coding", "software", "technology", "algorithm", "data", "ai", "machine learning", "training", "train", "numbers", "math", "code", "develop", "build", "create", "software engineer", "developer", "programmer"],
        "required_subjects": ["math", "physics"],
        "description": "Study of computational systems, algorithms, and software development",
        "career_paths": ["Software Engineer", "Data Scientist", "AI Engineer", "Machine Learning Engineer", "Cybersecurity Analyst", "Web Developer", "Mobile App Developer"]
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
        "keywords": ["mechanical", "mechanical engineering", "mechanical engineer", "mechanical systems", "mechanical design", "mechanical technology", "mechanical equipment", "mechanical devices", "mechanical machines", "mechanical components", "mechanical parts", "mechanical assembly", "mechanical manufacturing", "mechanical production", "mechanical automation", "mechanical robotics", "mechanical maintenance", "mechanical repair", "mechanical construction", "mechanical project", "mechanical consulting", "mechanical research", "mechanical development", "mechanical innovation", "mechanical technology", "building machines", "constructing machines", "machine design", "machine building", "machine construction", "machine manufacturing", "machine assembly", "machine automation", "machine maintenance", "machine repair", "machine troubleshooting", "machine optimization", "machine efficiency", "machine performance", "machine testing", "machine quality", "machine safety", "machine standards", "machine codes", "machine regulations", "machine compliance", "mechanical engineering degree", "mechanical engineering career"],
        "required_subjects": ["math", "physics"],
        "description": "Design, analysis, and manufacturing of mechanical systems and machines",
        "career_paths": ["Mechanical Engineer", "Design Engineer", "Manufacturing Engineer", "Robotics Engineer", "Automotive Engineer", "Aerospace Engineer", "Mechanical Designer", "Mechanical Project Manager"]
    },
    "Civil Engineering": {
        "keywords": ["civil", "civil engineering", "civil engineer", "civil construction", "civil infrastructure", "civil projects", "civil design", "civil technology", "civil systems", "civil structures", "civil buildings", "civil bridges", "civil roads", "civil highways", "civil transportation", "civil water", "civil drainage", "civil sewage", "civil environmental", "civil geotechnical", "civil structural", "civil materials", "civil surveying", "civil planning", "civil development", "civil maintenance", "civil repair", "civil renovation", "civil restoration", "civil preservation", "civil safety", "civil codes", "civil regulations", "civil compliance", "civil standards", "civil quality", "civil testing", "civil inspection", "civil supervision", "civil management", "civil consulting", "civil research", "civil innovation", "civil engineering degree", "civil engineering career"],
        "required_subjects": ["math", "physics"],
        "description": "Design and construction of infrastructure, buildings, and public works",
        "career_paths": ["Civil Engineer", "Structural Engineer", "Transportation Engineer", "Water Resources Engineer", "Environmental Engineer", "Geotechnical Engineer", "Construction Engineer", "Civil Project Manager"]
    },
    "Chemical Engineering": {
        "keywords": ["chemical", "chemical engineering", "chemical engineer", "chemical processes", "chemical manufacturing", "chemical production", "chemical technology", "chemical systems", "chemical equipment", "chemical plants", "chemical facilities", "chemical safety", "chemical environmental", "chemical sustainability", "chemical materials", "chemical products", "chemical research", "chemical development", "chemical innovation", "chemical design", "chemical optimization", "chemical efficiency", "chemical quality", "chemical testing", "chemical analysis", "chemical laboratory", "chemical experiments", "chemical reactions", "chemical synthesis", "chemical separation", "chemical purification", "chemical treatment", "chemical processing", "chemical operations", "chemical maintenance", "chemical troubleshooting", "chemical engineering degree", "chemical engineering career"],
        "required_subjects": ["math", "physics", "chemistry"],
        "description": "Design and operation of chemical processes and industrial systems",
        "career_paths": ["Chemical Engineer", "Process Engineer", "Plant Engineer", "Environmental Engineer", "Materials Engineer", "Petroleum Engineer", "Biochemical Engineer", "Chemical Project Manager"]
    },
    "Business Administration": {
        "keywords": ["business", "management", "finance", "marketing", "economics", "leadership", "entrepreneur", "ceo", "manager", "corporate", "startup", "investment", "strategy", "operations", "human resources", "sales", "customer service", "project management", "business consultant", "digital marketing", "social media", "business analytics", "supply chain", "international business", "business degree", "business school", "business profession", "business career"],
        "required_subjects": ["math", "english"],
        "description": "Study of business operations, management, and organizational behavior",
        "career_paths": ["Manager", "Entrepreneur", "Financial Analyst", "Marketing Manager", "CEO", "Business Consultant", "Project Manager", "Sales Manager", "Human Resources Manager"]
    },
    "Data Science": {
        "keywords": ["data", "analytics", "statistics", "machine learning", "python", "r", "analysis", "numbers", "math", "coding", "programming", "statistical", "data scientist", "data analyst", "big data", "data mining", "predictive analytics", "business intelligence", "data visualization", "database", "sql", "data engineering", "artificial intelligence", "deep learning", "neural networks", "data modeling", "quantitative analysis", "research scientist", "data science degree", "data science career"],
        "required_subjects": ["math", "physics"],
        "description": "Extract insights from data using statistical and computational methods",
        "career_paths": ["Data Scientist", "Data Analyst", "Machine Learning Engineer", "Data Engineer", "Statistician", "Quantitative Analyst", "Data Visualization Specialist", "Predictive Analytics Expert"]
    },
    "Psychology": {
        "keywords": ["psychology", "mental", "behavior", "counseling", "therapy", "human", "mind", "helping people", "help people", "mental health", "support", "care", "psychologist", "counselor", "therapist", "clinical psychology", "cognitive psychology", "social psychology", "developmental psychology", "forensic psychology", "sports psychology", "industrial psychology", "mental health counselor", "psychological research", "behavioral analysis", "psychological assessment", "psychological treatment", "psychological therapy", "psychological degree", "psychological career"],
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
        "keywords": ["international", "diplomacy", "politics", "global", "foreign", "policy", "government", "diplomat", "foreign service", "international development", "embassy", "consulate", "peacekeeping", "international trade", "international security", "international law", "global affairs", "foreign policy", "international organizations", "united nations", "ngo", "humanitarian", "international relations degree", "international relations career", "global politics", "international cooperation"],
        "required_subjects": ["history", "english"],
        "description": "Study of global politics, diplomacy, and international cooperation",
        "career_paths": ["Diplomat", "Policy Analyst", "International Consultant", "NGO Worker", "Foreign Service Officer", "International Development Specialist", "Global Affairs Analyst", "International Trade Specialist", "Peacekeeping Officer"]
    },
    "Architecture": {
        "keywords": ["architecture", "architect", "building design", "buildings", "sustainable", "green", "cad", "drawing", "blueprint", "creative", "visual", "space", "urban planning", "interior design", "landscape architecture", "architectural design", "building design", "historic preservation", "commercial architecture", "residential architecture", "architectural visualization", "3d modeling", "architectural degree", "architectural career", "architectural profession", "real estate", "housing", "skyscraper", "monument", "facade", "floor plan"],
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
        "keywords": ["law", "legal", "lawyer", "justice", "court", "rights", "legal system", "jurisprudence", "advocate", "attorney", "legal practice", "litigation", "legal advice", "legal research", "constitutional", "criminal law", "civil law", "legal profession", "criminal defense", "corporate law", "family law", "environmental law", "intellectual property", "international law", "immigration law", "human rights law", "legal aid", "contract law", "legal degree", "legal career", "legal profession"],
        "required_subjects": ["english", "history"],
        "description": "Study of legal systems, jurisprudence, and legal practice",
        "career_paths": ["Lawyer", "Judge", "Legal Advisor", "Prosecutor", "Legal Researcher", "Corporate Counsel", "Public Defender", "Legal Consultant", "Criminal Defense Attorney", "Family Lawyer", "Environmental Lawyer", "Intellectual Property Lawyer"]
    },
    "Pharmacy": {
        "keywords": ["pharmacy", "pharmacist", "medication", "drug", "medicine", "pharmaceutical", "prescription", "pharmacology", "pharmaceuticals", "drug development", "medication management", "pharmaceutical research", "drug safety", "pharmaceutical industry", "pharmacy practice", "clinical pharmacy", "pharmaceutical chemistry", "pharmaceutical technology", "pharmaceutical manufacturing", "pharmaceutical sales", "pharmaceutical marketing", "pharmaceutical regulation", "pharmaceutical quality", "pharmaceutical analysis", "pharmaceutical degree", "pharmaceutical career", "pharmaceutical profession"],
        "required_subjects": ["biology", "chemistry", "math"],
        "description": "Study of medications, drug development, and pharmaceutical care",
        "career_paths": ["Pharmacist", "Pharmaceutical Researcher", "Clinical Pharmacist", "Pharmaceutical Sales Representative", "Pharmaceutical Marketing Manager", "Pharmaceutical Quality Assurance Manager", "Pharmaceutical Regulatory Affairs Specialist", "Pharmaceutical Manufacturing Manager", "Pharmaceutical Consultant", "Pharmaceutical Analyst"]
    },
    "Business Management": {
        "keywords": ["business management", "management", "leadership", "team management", "organizational management", "business leadership", "management skills", "management degree", "management career", "management profession", "business administration", "corporate management", "strategic management", "operations management", "project management", "human resource management", "financial management", "marketing management", "management consulting", "management training", "management development", "management strategy", "management planning", "management decision", "management control", "management coordination", "management supervision", "management direction", "management guidance", "management oversight"],
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
        "keywords": ["ux", "ui", "user experience", "user interface", "ux design", "ui design", "ux/ui", "interface design", "user experience design", "user interface design", "interaction design", "product design", "digital design", "web design", "app design", "mobile design", "wireframe", "wireframing", "prototype", "prototyping", "user flow", "user journey", "usability", "usability testing", "user research", "user testing", "figma", "sketch", "adobe xd", "invision", "design system", "design thinking", "human-centered design", "user-centered design", "visual design", "information architecture", "ux research", "ux researcher", "ui designer", "ux designer", "product designer", "interaction designer", "experience designer", "design tools", "design software", "user personas", "empathy map", "user story", "design sprint", "a/b testing", "heuristic evaluation", "accessibility", "responsive design", "mobile-first", "design patterns", "micro-interactions", "user flows", "journey mapping", "design portfolio"],
        "required_subjects": ["english", "math"],
        "description": "Design of user interfaces and experiences for digital products, focusing on usability and user satisfaction",
        "career_paths": ["UX Designer", "UI Designer", "Product Designer", "UX Researcher", "Interaction Designer", "UX/UI Designer", "Digital Product Designer", "Experience Designer", "Design Lead", "UX Strategist"]
    },
    "Graphic Design": {
        "keywords": ["graphic design", "graphic designer", "visual design", "visual designer", "design", "designer", "creative design", "branding", "brand identity", "logo", "logo design", "poster", "poster design", "illustration", "illustrator", "photoshop", "adobe creative suite", "adobe illustrator", "adobe photoshop", "adobe indesign", "typography", "typeface", "font design", "color theory", "layout", "layout design", "composition", "visual communication", "print design", "digital design", "marketing design", "advertising design", "social media design", "graphics", "visual content", "creative", "art direction", "creative direction", "design portfolio", "vector graphics", "raster graphics", "image editing", "photo editing", "design principles", "design elements", "visual hierarchy", "brand guidelines", "style guide", "mockup", "packaging design", "editorial design", "publication design", "infographic", "icon design", "web graphics", "digital graphics", "visual identity", "corporate identity"],
        "required_subjects": ["english", "history"],
        "description": "Visual communication and design for print and digital media, including branding, marketing materials, and digital graphics",
        "career_paths": ["Graphic Designer", "Brand Designer", "Visual Designer", "Art Director", "Creative Director", "Marketing Designer", "Illustrator", "Digital Designer", "Print Designer", "Packaging Designer"]
    }
}
