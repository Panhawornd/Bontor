"""
Major database with keywords, descriptions, career paths, and fundamental skills
"""
MAJOR_DATABASE = {
    "Software Engineering": {
        "keywords": ["software engineering", "software developer", "coding", "programming", "code", "apps", "python", "javascript", "backend", "frontend", "algorithm", "software development", "build apps", "web development", "mobile development", "technology", "computer science", "tech", "logic", "math", "mathematics", "critical thinking"],
        "required_subjects": ["math", "physics"],
        "description": "Professional study of building software systems, applications, and digital solutions using code.",
        "career_paths": ["Software Engineer", "Full Stack Developer", "Backend Developer", "Frontend Developer", "App Developer", "System Architect"],
        "fundamental_skills": {
            "Programming": {"importance": "critical", "description": "Writing clean, efficient code"},
            "Problem Solving": {"importance": "critical", "description": "Breaking down complex problems"},
            "Mathematics": {"importance": "critical", "description": "Logical and computational thinking"},
            "Algorithms": {"importance": "critical", "description": "Data structures and algorithm design"},
            "System Design": {"importance": "high", "description": "Architecting scalable systems"},
            "Version Control": {"importance": "medium", "description": "Git and collaboration tools"}
        }
    },
    "Medicine": {
        "keywords": ["doctor", "medical", "health", "biology", "anatomy", "patient", "hospital", "clinic", "helping people", "saving lives", "help people", "save lives", "care", "healing", "treatment", "cure", "medicine", "healthcare", "surgeon", "physician", "medical research", "diagnosis", "surgery", "pharmacology", "cardiology", "neurology", "pediatrics", "emergency medicine", "medical technology", "clinical", "therapeutic", "medical practice", "healthcare provider", "medical specialist", "medical school", "medical degree", "medical profession", "biology", "life sciences", "chemistry"],
        "required_subjects": ["biology", "chemistry", "math"],
        "description": "Study of human health, diseases, and medical treatment",
        "career_paths": ["Doctor", "Surgeon", "Medical Researcher", "Pharmacist", "Pediatrician", "Cardiologist", "Neurologist", "Emergency Medicine Physician", "Medical Specialist"],
        "fundamental_skills": {
            "Biology": {"importance": "critical", "description": "Understanding human anatomy and physiology"},
            "Chemistry": {"importance": "critical", "description": "Chemical processes in the body"},
            "Patient Care": {"importance": "critical", "description": "Empathy and bedside manner"},
            "Critical Thinking": {"importance": "high", "description": "Diagnostic reasoning"},
            "Communication": {"importance": "high", "description": "Explaining conditions to patients"},
            "Memorization": {"importance": "medium", "description": "Medical terminology and procedures"}
        }
    },
    "Electrical Engineering": {
        "keywords": ["physics", "math", "electricity", "electrical", "electronics", "circuit", "power", "signal", "electronics engineer", "electrical systems", "power systems", "automation", "embedded systems", "robotics", "mechatronics"],
        "required_subjects": ["math", "physics"],
        "description": "Design and development of electrical systems, electronics, and power systems",
        "career_paths": ["Electrical Engineer", "Electronics Engineer", "Power Systems Engineer", "Control Systems Engineer", "Embedded Systems Engineer", "Telecommunications Engineer"],
        "fundamental_skills": {
            "Circuit Design": {"importance": "critical", "description": "Designing electrical circuits"},
            "Mathematics": {"importance": "critical", "description": "Calculus and linear algebra"},
            "Physics": {"importance": "critical", "description": "Electromagnetism and mechanics"},
            "Electronics": {"importance": "high", "description": "Component selection and integration"},
            "Programming": {"importance": "medium", "description": "Embedded systems coding"},
            "CAD Tools": {"importance": "medium", "description": "Circuit simulation software"}
        }
    },
    "Mechanical Engineering": {
        "keywords": ["mechanical", "machines", "robotics", "engine", "automotive", "thermodynamics", "manufacturing", "mechatronics", "physics", "math", "mathematics", "mechanics", "building machines", "fixing stuff", "handy", "mechanical systems"],
        "required_subjects": ["math", "physics"],
        "description": "Design, analysis, and manufacturing of mechanical systems and machines",
        "career_paths": ["Mechanical Engineer", "Design Engineer", "Manufacturing Engineer", "Robotics Engineer", "Automotive Engineer"],
        "fundamental_skills": {
            "Mechanics": {"importance": "critical", "description": "Understanding forces and motion"},
            "Mathematics": {"importance": "critical", "description": "Calculus and differential equations"},
            "Thermodynamics": {"importance": "high", "description": "Heat and energy transfer"},
            "CAD Design": {"importance": "high", "description": "3D modeling and drafting"},
            "Materials Science": {"importance": "medium", "description": "Material properties and selection"},
            "Manufacturing": {"importance": "medium", "description": "Production processes"}
        }
    },
    "Civil Engineering": {
        "keywords": ["civil", "civil engineering", "infrastructure", "bridges", "roads", "highways", "transportation", "construction", "structural", "public works", "structural analysis", "surveying", "urban planning", "civil project"],
        "required_subjects": ["math", "physics"],
        "description": "Design and construction of infrastructure, buildings, and public works",
        "career_paths": ["Civil Engineer", "Structural Engineer", "Transportation Engineer", "Water Resources Engineer", "Environmental Engineer", "Geotechnical Engineer", "Construction Engineer", "Civil Project Manager"],
        "fundamental_skills": {
            "Structural Analysis": {"importance": "critical", "description": "Load and stress calculations"},
            "Mathematics": {"importance": "critical", "description": "Engineering mathematics"},
            "Physics": {"importance": "high", "description": "Mechanics and materials"},
            "CAD Design": {"importance": "high", "description": "AutoCAD and structural modeling"},
            "Project Management": {"importance": "medium", "description": "Construction planning"},
            "Surveying": {"importance": "medium", "description": "Land measurement techniques"}
        }
    },
    "Chemical Engineering": {
        "keywords": ["chemical", "chemical engineering", "chemical engineer", "chemical reactions", "chemical manufacturing", "chemical processing", "industrial plants", "chemical reactors", "chemistry labs", "chemical synthesis", "petroleum", "chemistry", "math", "physics"],
        "required_subjects": ["math", "physics", "chemistry"],
        "description": "Design and operation of chemical processes and industrial systems",
        "career_paths": ["Chemical Engineer", "Process Engineer", "Plant Engineer", "Petroleum Engineer"],
        "fundamental_skills": {
            "Chemistry": {"importance": "critical", "description": "Chemical reactions and processes"},
            "Mathematics": {"importance": "critical", "description": "Differential equations"},
            "Process Design": {"importance": "high", "description": "Industrial process optimization"},
            "Thermodynamics": {"importance": "high", "description": "Heat and mass transfer"},
            "Safety Protocols": {"importance": "medium", "description": "Industrial safety standards"},
            "Lab Skills": {"importance": "medium", "description": "Laboratory techniques"}
        }
    },
    "Business Administration": {
        "keywords": ["business administration", "accounting", "entrepreneurship", "run a company", "startup", "operating a business", "finance", "marketing", "business economics", "corporate strategy", "company leader", "business degree", "math", "finance", "english"],
        "required_subjects": ["math", "english"],
        "description": "Study of business operations, management, and organizational behavior",
        "career_paths": ["Manager", "Entrepreneur", "Financial Analyst", "Marketing Manager", "CEO", "Business Consultant", "Project Manager", "Sales Manager", "Human Resources Manager"],
        "fundamental_skills": {
            "Leadership": {"importance": "critical", "description": "Team management and decision making"},
            "Communication": {"importance": "critical", "description": "Business writing and presentations"},
            "Financial Literacy": {"importance": "high", "description": "Understanding financial statements"},
            "Strategic Thinking": {"importance": "high", "description": "Business planning and strategy"},
            "Marketing": {"importance": "medium", "description": "Market analysis and branding"},
            "Analytics": {"importance": "medium", "description": "Data-driven decisions"}
        }
    },
    "Data Science": {
        "keywords": ["data science", "data", "data analysis", "big data", "data patterns", "analytics", "statistics", "python", "r", "sql", "data mining", "predictive modeling", "intelligence", "datasets", "coding", "programming", "machine learning", "artificial intelligence", "deep learning", "neural networks", "algorithm", "math", "mathematics", "statistics"],
        "required_subjects": ["math", "physics"],
        "description": "Advanced field focusing on extracting knowledge and insights from structured and unstructured data using scientific methods, algorithms, and systems.",
        "career_paths": ["Data Scientist", "Data Analyst", "Machine Learning Engineer", "Data Engineer"],
        "fundamental_skills": {
            "Data Science": {"importance": "critical", "description": "Core data analysis and modeling"},
            "Statistics": {"importance": "critical", "description": "Statistical analysis and inference"},
            "Programming": {"importance": "critical", "description": "Python, R, and SQL"},
            "Mathematics": {"importance": "critical", "description": "Linear algebra and calculus"},
            "Machine Learning": {"importance": "high", "description": "ML algorithms and models"},
            "Data Visualization": {"importance": "high", "description": "Charts and dashboards"}
        }
    },
    "Psychology": {
        "keywords": ["psychology", "mental", "behavior", "counseling", "therapy", "human", "mind", "helping people", "help people", "understanding people", "understand people", "human behavior", "people", "mental health", "support", "care", "psychologist", "counselor", "therapist", "clinical psychology", "cognitive psychology", "social psychology", "developmental psychology", "forensic psychology", "sports psychology", "industrial psychology", "mental health counselor", "psychological research", "behavioral analysis", "psychological assessment", "psychological treatment", "psychological therapy", "psychological degree", "psychological career", "biology", "english"],
        "required_subjects": ["biology", "english"],
        "description": "Study of human behavior, cognition, and mental processes",
        "career_paths": ["Psychologist", "Counselor", "Therapist", "Researcher", "School Psychologist", "Forensic Psychologist", "Sports Psychologist", "Industrial Psychologist", "Mental Health Counselor"],
        "fundamental_skills": {
            "Empathy": {"importance": "critical", "description": "Understanding emotions and feelings"},
            "Communication": {"importance": "critical", "description": "Active listening and counseling"},
            "Critical Thinking": {"importance": "high", "description": "Analyzing behavioral patterns"},
            "Research Skills": {"importance": "high", "description": "Psychological research methods"},
            "Ethics": {"importance": "medium", "description": "Professional ethical standards"},
            "Writing": {"importance": "medium", "description": "Case documentation and reports"}
        }
    },
    "Education": {
        "keywords": ["teaching", "education", "teacher", "school", "learning", "students", "classroom", "helping people", "help people", "teach", "mentor", "guide", "educator", "professor", "principal", "curriculum", "educational technology", "special education", "early childhood education", "educational administration", "educational policy", "teacher training", "educational research", "academic", "pedagogy", "instructional design", "educational leadership", "school counselor", "educational consultant", "education degree", "education career", "english", "math", "explaining things", "mentoring", "explaining concepts"],
        "required_subjects": ["english", "math"],
        "description": "Preparation for teaching and educational leadership roles",
        "career_paths": ["Teacher", "Principal", "Educational Consultant", "Curriculum Developer", "University Professor", "Special Education Teacher", "Educational Technology Specialist", "School Counselor", "Training and Development Manager"],
        "fundamental_skills": {
            "Communication": {"importance": "critical", "description": "Explaining concepts clearly"},
            "Patience": {"importance": "critical", "description": "Working with diverse learners"},
            "Creativity": {"importance": "high", "description": "Engaging lesson design"},
            "Organization": {"importance": "high", "description": "Classroom management"},
            "Empathy": {"importance": "medium", "description": "Understanding student needs"},
            "Technology": {"importance": "medium", "description": "Educational technology tools"}
        }
    },
    "International Relations": {
        "keywords": ["international", "diplomacy", "politics", "global", "foreign", "policy", "government", "diplomat", "foreign service", "international development", "embassy", "consulate", "peacekeeping", "international trade", "international security", "international law", "global affairs", "foreign policy", "international organizations", "united nations", "ngo", "humanitarian", "international relations degree", "international relations career", "global politics", "international cooperation", "debating", "world affairs", "global issues", "history", "english"],
        "required_subjects": ["history", "english"],
        "description": "Study of global politics, diplomacy, and international cooperation",
        "career_paths": ["Diplomat", "Policy Analyst", "International Consultant", "NGO Worker", "Foreign Service Officer", "International Development Specialist", "Global Affairs Analyst", "International Trade Specialist", "Peacekeeping Officer"],
        "fundamental_skills": {
            "Communication": {"importance": "critical", "description": "Diplomatic communication"},
            "Critical Thinking": {"importance": "critical", "description": "Policy analysis"},
            "Languages": {"importance": "high", "description": "Foreign language proficiency"},
            "Research Skills": {"importance": "high", "description": "Geopolitical research"},
            "Cultural Awareness": {"importance": "medium", "description": "Understanding diverse cultures"},
            "Negotiation": {"importance": "medium", "description": "Diplomatic negotiation skills"}
        }
    },
    "Architecture": {
        "keywords": ["architecture", "buildings", "floor plans", "blueprint", "urban planning", "construction design", "structural aesthetics", "spatial design", "math", "mathematics", "physics", "design", "art"],
        "required_subjects": ["math", "physics"],
        "description": "Art and science of designing buildings and structures",
        "career_paths": ["Architect", "Urban Planner", "Interior Designer", "Construction Manager", "Landscape Architect", "Project Architect", "Sustainable Design Specialist", "Historic Preservation Architect", "Commercial Architect", "Residential Architect"],
        "fundamental_skills": {
            "Design Thinking": {"importance": "critical", "description": "Spatial and aesthetic design"},
            "CAD Skills": {"importance": "critical", "description": "AutoCAD and 3D modeling"},
            "Mathematics": {"importance": "high", "description": "Geometric calculations"},
            "Creativity": {"importance": "high", "description": "Innovative building concepts"},
            "Technical Drawing": {"importance": "medium", "description": "Blueprints and plans"},
            "Sustainability": {"importance": "medium", "description": "Green building practices"}
        }
    },
    "Dentistry": {
        "keywords": ["dentistry", "dentist", "dental", "teeth", "oral", "health", "mouth", "tooth", "gum", "dental care", "orthodontist", "oral surgery", "dental hygiene", "dental clinic", "oral health", "dental treatment", "dental procedures", "dental technology", "cosmetic dentistry", "dental implants", "periodontics", "endodontics", "prosthodontics", "pediatric dentistry", "dental research", "dental materials", "dental degree", "dental career", "dental profession", "biology", "chemistry", "math"],
        "required_subjects": ["biology", "chemistry", "math"],
        "description": "Study of oral health, dental care, and treatment of teeth and gums",
        "career_paths": ["Dentist", "Orthodontist", "Oral Surgeon", "Dental Hygienist", "Dental Assistant", "Periodontist", "Endodontist", "Prosthodontist", "Pediatric Dentist", "Cosmetic Dentist"],
        "fundamental_skills": {
            "Manual Dexterity": {"importance": "critical", "description": "Precision hand skills"},
            "Biology": {"importance": "critical", "description": "Oral anatomy knowledge"},
            "Patient Care": {"importance": "high", "description": "Chairside manner"},
            "Chemistry": {"importance": "high", "description": "Dental materials science"},
            "Communication": {"importance": "medium", "description": "Patient education"},
            "Attention to Detail": {"importance": "medium", "description": "Precise dental work"}
        }
    },
    "Law": {
        "keywords": ["law", "legal", "lawyer", "justice", "court", "rights", "legal system", "jurisprudence", "advocate", "attorney", "legal practice", "litigation", "legal advice", "legal research", "constitutional", "criminal law", "civil law", "legal profession", "criminal defense", "corporate law", "family law", "environmental law", "intellectual property", "international law", "immigration law", "human rights law", "legal aid", "contract law", "legal degree", "legal career", "legal profession", "arguing", "debating", "rules", "logic", "persuasion", "history", "english"],
        "required_subjects": ["english", "history"],
        "description": "Study of legal systems, jurisprudence, and legal practice",
        "career_paths": ["Lawyer", "Judge", "Legal Advisor", "Prosecutor", "Legal Researcher", "Corporate Counsel", "Public Defender", "Legal Consultant", "Criminal Defense Attorney", "Family Lawyer", "Environmental Lawyer", "Intellectual Property Lawyer"],
        "fundamental_skills": {
            "Critical Thinking": {"importance": "critical", "description": "Legal analysis and reasoning"},
            "Communication": {"importance": "critical", "description": "Oral arguments and writing"},
            "Research Skills": {"importance": "high", "description": "Legal research methods"},
            "Writing": {"importance": "high", "description": "Legal document drafting"},
            "Negotiation": {"importance": "medium", "description": "Settlement discussions"},
            "Ethics": {"importance": "medium", "description": "Legal ethics and standards"}
        }
    },
    "Pharmacy": {
        "keywords": ["pharmacy", "pharmacist", "medication", "drugs", "pharmaceutical", "prescription", "pharmacology", "dispensing", "dosage", "medical drugs", "chemists", "pharmacy practice", "clinical pharmacy", "pharmaceutical chemistry", "pharmaceutical technology", "pharmaceutical manufacturing", "chemistry", "biology", "math"],
        "required_subjects": ["biology", "chemistry", "math"],
        "description": "Study of medications, drug development, and pharmaceutical care",
        "career_paths": ["Pharmacist", "Pharmaceutical Researcher", "Clinical Pharmacist", "Pharmaceutical Sales Representative", "Pharmaceutical Marketing Manager", "Pharmaceutical Quality Assurance Manager", "Pharmaceutical Regulatory Affairs Specialist", "Pharmaceutical Manufacturing Manager", "Pharmaceutical Consultant", "Pharmaceutical Analyst"],
        "fundamental_skills": {
            "Chemistry": {"importance": "critical", "description": "Drug chemistry and interactions"},
            "Attention to Detail": {"importance": "critical", "description": "Accurate dispensing"},
            "Biology": {"importance": "high", "description": "Pharmacology knowledge"},
            "Communication": {"importance": "high", "description": "Patient counseling"},
            "Mathematics": {"importance": "medium", "description": "Dosage calculations"},
            "Regulations": {"importance": "medium", "description": "Pharmaceutical laws"}
        }
    },
    "Business Management": {
        "keywords": ["business management", "leadership", "team management", "operations management", "organizational leadership", "supervision", "managing teams", "business operations", "resource management", "strategic leadership", "team leader", "management skills", "english", "math"],
        "required_subjects": ["math", "english"],
        "description": "Study of business management, leadership, and organizational behavior",
        "career_paths": ["Business Manager", "Operations Manager", "Project Manager", "Team Leader", "Department Manager", "General Manager", "Management Consultant", "Business Analyst", "Management Trainee", "Executive Manager"],
        "fundamental_skills": {
            "Leadership": {"importance": "critical", "description": "Team leadership and motivation"},
            "Communication": {"importance": "critical", "description": "Business communication"},
            "Decision Making": {"importance": "high", "description": "Strategic decisions"},
            "Organization": {"importance": "high", "description": "Resource management"},
            "Problem Solving": {"importance": "medium", "description": "Business problem resolution"},
            "Analytics": {"importance": "medium", "description": "Performance metrics"}
        }
    },
    "Finance": {
        "keywords": ["finance", "financial", "investment", "banking", "financial analysis", "financial planning", "financial management", "financial services", "financial markets", "financial instruments", "financial modeling", "financial reporting", "financial accounting", "financial risk", "financial strategy", "financial consulting", "financial advisor", "financial analyst", "financial manager", "financial controller", "financial director", "financial executive", "financial degree", "financial career", "financial profession", "corporate finance", "personal finance", "public finance", "international finance", "quantitative finance", "financial engineering", "math", "mathematics", "numbers", "statistics", "calculating", "equations", "analytics", "quantitative", "numerical analysis", "data analysis", "english"],
        "required_subjects": ["math", "english"],
        "description": "Study of financial systems, investment, quantitative analysis, numeric modeling, and math-driven financial management",
        "career_paths": ["Financial Analyst", "Investment Banker", "Financial Advisor", "Financial Manager", "Financial Controller", "Investment Manager", "Risk Manager", "Financial Consultant", "Corporate Finance Manager", "Portfolio Manager"],
        "fundamental_skills": {
            "Financial Analysis": {"importance": "critical", "description": "Analyzing financial data"},
            "Mathematics": {"importance": "critical", "description": "Quantitative analysis"},
            "Excel/Modeling": {"importance": "high", "description": "Financial modeling tools"},
            "Economics": {"importance": "high", "description": "Economic principles"},
            "Communication": {"importance": "medium", "description": "Client presentations"},
            "Risk Assessment": {"importance": "medium", "description": "Risk evaluation"}
        }
    },
    "UX/UI Design": {
        "keywords": ["ux design", "ui design", "user interface", "user experience", "interface design", "figma", "wireframe", "prototype", "usability", "interaction design", "adobe xd", "product design", "ux designer", "ui designer", "english", "math", "design"],
        "required_subjects": ["english", "math"],
        "description": "Design of user interfaces and experiences for digital products, focusing on usability and user satisfaction",
        "career_paths": ["UX Designer", "UI Designer", "Product Designer", "UX Researcher", "Interaction Designer"],
        "fundamental_skills": {
            "Design Thinking": {"importance": "critical", "description": "User-centered design process"},
            "Prototyping": {"importance": "critical", "description": "Figma/Adobe XD skills"},
            "User Research": {"importance": "high", "description": "Understanding user needs"},
            "Visual Design": {"importance": "high", "description": "Typography and color theory"},
            "Communication": {"importance": "medium", "description": "Presenting design decisions"},
            "Usability Testing": {"importance": "medium", "description": "Testing and iteration"}
        }
    },
    "Graphic Design": {
        "keywords": ["graphic design", "graphic designer", "visual design", "branding", "logo", "poster", "illustrator", "photoshop", "indesign", "typography", "layout", "print design", "marketing design", "visual identity", "art director", "history", "english", "design", "art"],
        "required_subjects": ["english", "history"],
        "description": "Visual communication and design for print and digital media, including branding, marketing materials, and digital graphics",
        "career_paths": ["Graphic Designer", "Brand Designer", "Visual Designer", "Art Director", "Creative Director", "Marketing Designer", "Illustrator", "Digital Designer", "Print Designer", "Packaging Designer"],
        "fundamental_skills": {
            "Visual Design": {"importance": "critical", "description": "Composition and aesthetics"},
            "Adobe Suite": {"importance": "critical", "description": "Photoshop, Illustrator, InDesign"},
            "Typography": {"importance": "high", "description": "Font selection and layout"},
            "Creativity": {"importance": "high", "description": "Original visual concepts"},
            "Branding": {"importance": "medium", "description": "Brand identity design"},
            "Communication": {"importance": "medium", "description": "Client collaboration"}
        }
    },
    "Cybersecurity": {
        "keywords": ["cybersecurity", "cyber security", "hacking", "ethical hacking", "encryption", "network security", "privacy", "information security", "firewall", "security analyst", "coding", "programming", "python", "scripting", "penetration testing", "vulnerability", "math", "digital safety"],
        "required_subjects": ["math", "physics"],
        "description": "Specialized field dedicated to protecting systems and networks from digital attacks, unauthorized access, and data breaches.",
        "career_paths": ["Cybersecurity Analyst", "Security Engineer", "Ethical Hacker", "Information Security Manager", "Network Security Architect", "Incident Responder"],
        "fundamental_skills": {
            "Cybersecurity": {"importance": "critical", "description": "Security principles and defense"},
            "Network Security": {"importance": "critical", "description": "Network protocols and defense"},
            "Programming": {"importance": "critical", "description": "Security scripting and tools"},
            "Cryptography": {"importance": "high", "description": "Encryption methods"},
            "Problem Solving": {"importance": "high", "description": "Threat analysis"},
            "Linux/Systems": {"importance": "medium", "description": "OS security"}
        }
    },
    "Telecommunication and Networking": {
        "keywords": ["telecommunication", "networking", "network", "network engineer", "cisco", "routing", "switching", "internet protocol", "ip", "transmission", "signals", "5g", "wireless", "telecom", "infrastructure", "connectivity", "fiber optics", "network administration", "programming", "coding", "python", "automation", "scripting", "devops", "cloud", "backend", "server", "technology", "router", "switch", "lan", "wan", "tcp", "dns", "vpn", "wifi", "internet", "math", "physics"],
        "required_subjects": ["math", "physics"],
        "description": "Study of network architecture, data transmission, and communication systems with programming for network automation",
        "career_paths": ["Network Engineer", "Telecom Engineer", "Network Administrator", "Systems Engineer", "Connectivity Specialist", "DevOps Engineer", "Cloud Engineer"],
        "fundamental_skills": {
            "Networking": {"importance": "critical", "description": "TCP/IP and routing protocols"},
            "Programming": {"importance": "critical", "description": "Python and network automation"},
            "Mathematics": {"importance": "high", "description": "Signal processing"},
            "Problem Solving": {"importance": "high", "description": "Network troubleshooting"},
            "Hardware": {"importance": "medium", "description": "Network equipment"},
            "Wireless Tech": {"importance": "medium", "description": "5G and wireless systems"}
        }
    },
    "Logistic": {
        "keywords": ["logistic", "logistics", "supply chain", "plans trips", "organizes deliveries", "route optimization", "enjoys organizing tasks", "delivery tracking", "transportation", "warehouse", "operations"],
        "required_subjects": ["math", "english"],
        "description": "Study of the complex operations involved in the flow of goods, services, and information, including route optimization and delivery organization",
        "career_paths": ["Logistics Manager", "Supply Chain Analyst", "Transportation Manager", "Operations Manager"],
        "fundamental_skills": {
            "Route Optimization": {"importance": "critical", "description": "Planning efficient delivery routes"},
            "Organization": {"importance": "critical", "description": "Managing complex task schedules"},
            "Data Analysis": {"importance": "high", "description": "Tracking and improving delivery metrics"},
            "Communication": {"importance": "high", "description": "Coordinating with teams and clients"}
        }
    }
}
