#!/usr/bin/env python3
"""
ML Training Script for Grade Analyzer
This script trains recommendation models from collected user data
"""

import json
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sentence_transformers import SentenceTransformer
import joblib
import os
import psycopg2
from typing import Dict, List, Any

class RecommendationTrainer:
    def __init__(self):
        self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.major_classifier = None
        self.career_classifier = None
        
        # Domain-specific models
        self.domain_models = {
            'electrical_engineering': None,
            'mechanical_engineering': None,
            'civil_engineering': None,
            'chemical_engineering': None,
            'medicine': None,
            'business': None,
            'technology': None,
            'arts': None,
            'design': None  # New domain for UX/UI and Graphic Design
        }
        
        # Model evaluation metrics
        self.model_metrics = {}
        
        # Domain keywords for classification
        self.domain_keywords = {
            'electrical_engineering': ['electrical', 'electric', 'electronic', 'electronics', 'circuit', 'power', 'embedded', 'signal', 'voltage', 'current', 'electrical systems', 'power systems', 'control systems', 'telecommunication'],
            'mechanical_engineering': ['mechanical', 'machine', 'mechanism', 'manufacturing', 'mechatronics', 'robotics', 'automation', 'mechanical systems', 'engines', 'gears', 'building machine', 'building machines', 'constructing machine', 'constructing machines'],
            'civil_engineering': ['civil', 'infrastructure', 'bridge', 'road', 'highway', 'dam', 'tunnel', 'foundation', 'structural engineering', 'construction engineering', 'transportation', 'water systems', 'sewage', 'public works'],
            'chemical_engineering': ['chemical', 'chemistry', 'process', 'reaction', 'materials', 'chemical processes', 'petrochemical', 'pharmaceutical', 'polymer', 'biochemical', 'process engineering', 'chemical plants'],
            'medicine': ['doctor', 'medical', 'medicine', 'health', 'anatomy', 'patient', 'hospital', 'clinic', 'surgery', 'physician', 'dentist', 'dental'],
            'business': ['business', 'management', 'finance', 'marketing', 'entrepreneur', 'ceo', 'manager', 'corporate', 'startup', 'investment'],
            'technology': ['programming', 'coding', 'software', 'computer', 'tech', 'ai', 'data', 'machine learning', 'artificial intelligence', 'cybersecurity'],
            'design': ['ux', 'ui', 'user experience', 'user interface', 'wireframe', 'prototype', 'figma', 'adobe xd', 'sketch', 'usability', 'interaction design', 'product design', 'graphic design', 'visual design', 'logo', 'branding', 'photoshop', 'illustrator', 'indesign', 'typography', 'layout', 'poster', 'graphic designer', 'ux designer', 'ui designer'],  # New design domain
            'arts': ['art', 'creative', 'drawing', 'music', 'artistic', 'architecture', 'architect', 'building design', 'psychology', 'psychologist', 'mental', 'behavior', 'emotions', 'counseling', 'therapy', 'therapist', 'understanding people', 'listening', 'advice', 'mental wellbeing', 'human behavior', 'cognitive', 'psychological', 'international', 'diplomacy', 'politics', 'global', 'foreign', 'policy', 'government', 'diplomat', 'foreign service', 'international development', 'embassy', 'consulate', 'peacekeeping', 'international trade', 'international security', 'international law', 'global affairs', 'foreign policy', 'international organizations', 'united nations', 'ngo', 'humanitarian']
        }
    
    def detect_domain(self, text: str) -> str:
        """Detect the primary domain from user text"""
        if not text:
            return 'general'
        
        text_lower = text.lower()
        domain_scores = {}
        
        for domain, keywords in self.domain_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                domain_scores[domain] = score
        
        if domain_scores:
            return max(domain_scores, key=domain_scores.get)
        return 'general'
    
    def load_training_data_from_db(self) -> pd.DataFrame:
        """Load training data from PostgreSQL database"""
        try:
            # Connect to database
            conn = psycopg2.connect(
                host="localhost",
                port="5433",
                database="grade_analyzer",
                user="postgres",
                password="baboo123"
            )
            
            # Query training data
            query = """
            SELECT 
                td.id,
                td.grades,
                td.interests,
                td."careerGoals",
                td."recommendedMajor",
                td."actualMajor",
                td."feedbackScore",
                td."createdAt"
            FROM "TrainingData" td
            WHERE td."isProcessed" = false
            ORDER BY td."createdAt" DESC
            LIMIT 1000
            """
            
            df = pd.read_sql_query(query, conn)
            
            # Store the IDs of records we're processing for later update
            if not df.empty:
                self.processed_record_ids = df['id'].tolist()
            else:
                self.processed_record_ids = []
            
            conn.close()
            
            if df.empty or len(df) < 50:  # Need at least 50 samples for good training
                print(f"Not enough training data in database ({len(df) if not df.empty else 0} records). Creating sample data...")
                return self.create_sample_data()
            
            print(f"Loaded {len(df)} training records from database")
            return df
            
        except Exception as e:
            print(f"Error loading from database: {e}")
            print("Falling back to sample data...")
            return self.create_sample_data()
    
    def load_training_data(self, data_file: str = "training_data.json") -> pd.DataFrame:
        """Load training data from database or JSON file"""
        return self.load_training_data_from_db()
    
    def mark_records_as_processed(self):
        """Mark training records as processed in the database"""
        if not hasattr(self, 'processed_record_ids') or not self.processed_record_ids:
            print("No records to mark as processed")
            return
            
        try:
            conn = psycopg2.connect(
                host="localhost",
                port="5433",
                database="grade_analyzer",
                user="postgres",
                password="baboo123"
            )
            cursor = conn.cursor()
            
            # Update records to mark as processed
            placeholders = ','.join(['%s'] * len(self.processed_record_ids))
            update_query = f"""
            UPDATE "TrainingData" 
            SET "isProcessed" = true 
            WHERE id IN ({placeholders})
            """
            
            cursor.execute(update_query, self.processed_record_ids)
            conn.commit()
            
            print(f"Marked {len(self.processed_record_ids)} records as processed")
            
            cursor.close()
            conn.close()
            
        except Exception as e:
            print(f"Error marking records as processed: {e}")
    
    def create_sample_data(self) -> pd.DataFrame:
        """Create sample training data for demonstration"""
        import random
        
        majors = ["Computer Science", "Medicine", "Electrical Engineering", "Mechanical Engineering", "Civil Engineering", "Chemical Engineering", "Business Administration", "Data Science", "Psychology", "Education", "International Relations", "Law", "Architecture", "Dentistry", "UX/UI Design", "Graphic Design"]
        
        # More diverse and realistic interest samples
        interests_by_major = {
            "Computer Science": [
                "I love programming and coding",
                "I enjoy working with computers and technology",
                "I want to develop software and applications",
                "I love solving problems with code",
                "I'm interested in artificial intelligence and machine learning",
                "I love training the machine and AI models",
                "I want to train machine learning algorithms",
                "I enjoy training AI systems",
                "I want to build websites and mobile apps",
                "I enjoy working with data and algorithms",
                "I love creating digital solutions",
                "I'm passionate about software development",
                "I want to become a software engineer",
                "I love debugging and fixing code",
                "I enjoy learning new programming languages",
                "I want to work in tech companies",
                "I'm fascinated by computer systems",
                "I love building applications and software",
                "I want to specialize in cybersecurity",
                "I enjoy working with databases and data structures"
            ],
            "Medicine": [
                "I want to help people and save lives",
                "I'm passionate about healthcare and healing",
                "I want to become a doctor",
                "I'm interested in human anatomy and biology",
                "I want to work in hospitals and clinics",
                "I love helping people with their health",
                "I'm fascinated by medical science",
                "I want to make a difference in people's lives",
                "I want to become a surgeon and perform operations",
                "I'm interested in diagnosing diseases and conditions",
                "I love studying the human body and its functions",
                "I want to work in emergency medicine",
                "I'm passionate about medical research and discoveries",
                "I want to specialize in cardiology or neurology",
                "I love working with patients and providing care",
                "I'm interested in medical technology and equipment",
                "I want to work in rural areas to help underserved communities",
                "I'm fascinated by pharmacology and drug development",
                "I want to become a pediatrician and work with children",
                "I love the challenge of solving complex medical cases"
            ],
            "Electrical Engineering": [
                "I love working with electrical circuits and power systems",
                "I enjoy designing electronic devices and components",
                "I want to work with electrical systems and automation",
                "I'm fascinated by electrical power generation and distribution",
                "I love circuit design and electrical engineering",
                "I want to become an electrical engineer",
                "I'm interested in power electronics and control systems",
                "I love working with electrical motors and generators",
                "I want to design electrical infrastructure and smart grids",
                "I'm passionate about electrical safety and code compliance",
                "I love troubleshooting electrical systems and equipment",
                "I want to work in electrical manufacturing and production",
                "I'm interested in renewable energy and electrical sustainability",
                "I love working with electrical measurement and testing equipment",
                "I want to specialize in electrical automation and robotics",
                "I'm fascinated by electrical telecommunications and signal processing",
                "I love working with electrical transformers and power distribution",
                "I want to design electrical control panels and systems",
                "I'm interested in electrical project management and consulting",
                "I love the challenge of complex electrical engineering problems"
            ],
            "Mechanical Engineering": [
                "I love building and designing machines",
                "I enjoy working with mechanical systems and components",
                "I want to create innovative mechanical solutions",
                "I'm passionate about mechanical engineering and robotics",
                "I love working with mechanical design and manufacturing",
                "I want to become a mechanical engineer",
                "I'm interested in mechanical automation and control systems",
                "I love working with mechanical tools and equipment",
                "I want to design mechanical systems for various industries",
                "I'm fascinated by mechanical thermodynamics and fluid mechanics",
                "I love working with mechanical materials and manufacturing processes",
                "I want to specialize in mechanical robotics and automation",
                "I'm interested in mechanical maintenance and repair",
                "I love working with mechanical CAD software and 3D modeling",
                "I want to design mechanical products and consumer goods",
                "I'm passionate about mechanical sustainability and green engineering",
                "I love working with mechanical testing and quality control",
                "I want to work in mechanical manufacturing and production",
                "I'm interested in mechanical project management and consulting",
                "I love the challenge of complex mechanical engineering problems"
            ],
            "Civil Engineering": [
                "I love designing and building infrastructure",
                "I enjoy working on civil construction projects",
                "I want to create sustainable civil engineering solutions",
                "I'm passionate about civil engineering and public works",
                "I love working with civil structures and buildings",
                "I want to become a civil engineer",
                "I'm interested in civil infrastructure and transportation",
                "I love working with civil materials and construction methods",
                "I want to design civil systems for water and sewage",
                "I'm fascinated by civil structural engineering and analysis",
                "I love working with civil surveying and site planning",
                "I want to specialize in civil environmental engineering",
                "I'm interested in civil project management and construction",
                "I love working with civil safety and code compliance",
                "I want to design civil bridges and transportation systems",
                "I'm passionate about civil sustainability and green infrastructure",
                "I love working with civil testing and quality assurance",
                "I want to work in civil construction and development",
                "I'm interested in civil consulting and engineering services",
                "I love the challenge of complex civil engineering projects"
            ],
            "Chemical Engineering": [
                "I love working with chemical processes and reactions",
                "I enjoy designing chemical manufacturing systems",
                "I want to create innovative chemical engineering solutions",
                "I'm passionate about chemical engineering and process design",
                "I love working with chemical materials and products",
                "I want to become a chemical engineer",
                "I'm interested in chemical process optimization and efficiency",
                "I love working with chemical safety and environmental compliance",
                "I want to design chemical plants and facilities",
                "I'm fascinated by chemical thermodynamics and kinetics",
                "I love working with chemical separation and purification processes",
                "I want to specialize in chemical environmental engineering",
                "I'm interested in chemical research and development",
                "I love working with chemical testing and quality control",
                "I want to design chemical products and consumer goods",
                "I'm passionate about chemical sustainability and green processes",
                "I love working with chemical automation and control systems",
                "I want to work in chemical manufacturing and production",
                "I'm interested in chemical project management and consulting",
                "I love the challenge of complex chemical engineering problems"
            ],
            "Data Science": [
                "I love analyzing data and finding patterns",
                "I enjoy working with numbers and statistics",
                "I want to extract insights from data",
                "I'm interested in machine learning and AI",
                "I love solving problems with data",
                "I want to help businesses make data-driven decisions",
                "I enjoy programming and mathematics",
                "I'm fascinated by predictive analytics",
                "I want to become a data scientist and work with big data",
                "I love creating data visualizations and dashboards",
                "I'm passionate about statistical analysis and modeling",
                "I want to work with Python and R for data analysis",
                "I'm interested in deep learning and neural networks",
                "I love working with databases and SQL queries",
                "I want to develop predictive models and algorithms",
                "I'm fascinated by data mining and pattern recognition",
                "I want to work in business intelligence and analytics",
                "I love solving complex problems using data science",
                "I'm interested in artificial intelligence and automation",
                "I want to help organizations optimize their operations with data"
            ],
            "Psychology": [
                "I'm fascinated by human behavior and the mind",
                "I want to help people with mental health",
                "I'm interested in understanding human psychology",
                "I want to become a therapist or counselor",
                "I love studying human behavior",
                "I want to help people overcome challenges",
                "I'm interested in mental health and wellbeing",
                "I want to understand why people think and act the way they do",
                "I want to become a clinical psychologist and help patients",
                "I'm passionate about cognitive psychology and brain function",
                "I love working with children and developmental psychology",
                "I want to specialize in counseling and therapy",
                "I'm interested in social psychology and group behavior",
                "I want to work in mental health clinics and hospitals",
                "I love conducting psychological research and studies",
                "I'm fascinated by abnormal psychology and mental disorders",
                "I want to help people with anxiety and depression",
                "I'm interested in forensic psychology and criminal behavior",
                "I want to become a school psychologist and work with students",
                "I love understanding human emotions and relationships"
            ],
            "Education": [
                "I love teaching and working with students",
                "I want to make a difference in education",
                "I enjoy helping others learn and grow",
                "I want to become a teacher",
                "I'm passionate about learning and knowledge",
                "I want to inspire young minds",
                "I love working in schools and classrooms",
                "I want to improve educational systems",
                "I want to become a primary school teacher and work with children",
                "I'm passionate about curriculum development and lesson planning",
                "I love working with special needs students and inclusive education",
                "I want to become a university professor and conduct research",
                "I'm interested in educational technology and online learning",
                "I want to work in educational administration and policy",
                "I love teaching mathematics and science to students",
                "I'm fascinated by educational psychology and learning theories",
                "I want to become a school principal and lead educational institutions",
                "I'm interested in early childhood education and development",
                "I want to work in teacher training and professional development",
                "I love creating innovative teaching methods and educational programs"
            ],
            "Business Administration": [
                "I want to manage businesses and lead teams",
                "I'm interested in entrepreneurship",
                "I want to start my own business",
                "I enjoy working with people and organizations",
                "I want to become a business leader",
                "I'm interested in marketing and finance",
                "I want to help companies grow and succeed",
                "I love strategic planning and management",
                "I want to become a CEO and lead major corporations",
                "I'm passionate about digital marketing and social media",
                "I love working with financial analysis and investments",
                "I want to work in human resources and talent management",
                "I'm interested in supply chain management and operations",
                "I want to become a business consultant and help companies",
                "I love working with startups and new business ventures",
                "I'm fascinated by international business and global markets",
                "I want to work in project management and team coordination",
                "I'm interested in business analytics and data-driven decisions",
                "I want to become a sales manager and drive revenue growth",
                "I love working with customer relations and service excellence"
            ],
            "International Relations": [
                "I'm passionate about global issues and diplomacy",
                "I want to work in international organizations",
                "I'm interested in politics and foreign affairs",
                "I want to promote peace and cooperation",
                "I love learning about different cultures",
                "I want to work for the government or UN",
                "I'm interested in international law and policy",
                "I want to make a global impact",
                "I want to become a diplomat and represent my country",
                "I'm passionate about international development and aid work",
                "I love working with embassies and consulates",
                "I want to specialize in conflict resolution and peacekeeping",
                "I'm interested in international trade and economic relations",
                "I want to work in international security and counterterrorism",
                "I love studying international history and global politics",
                "I want to become a foreign policy analyst and researcher",
                "I'm fascinated by international organizations like the UN and WTO",
                "I want to work in international human rights and advocacy",
                "I love working with international NGOs and humanitarian work",
                "I want to become an international relations professor and researcher"
            ],
            "Law": [
                "I want to become a lawyer and help people with legal issues",
                "I'm passionate about justice and fairness",
                "I want to defend people's rights",
                "I'm interested in the legal system and law",
                "I want to work in courts and legal practice",
                "I love analyzing legal cases and precedents",
                "I want to become a judge or prosecutor",
                "I'm interested in constitutional law and civil rights",
                "I want to become a criminal defense attorney and protect rights",
                "I'm passionate about corporate law and business legal matters",
                "I love working with family law and helping families",
                "I want to specialize in environmental law and sustainability",
                "I'm interested in intellectual property law and patents",
                "I want to work in international law and cross-border issues",
                "I love working with immigration law and helping immigrants",
                "I'm fascinated by constitutional law and government structure",
                "I want to become a legal researcher and law professor",
                "I'm interested in human rights law and social justice",
                "I want to work in legal aid and help underserved communities",
                "I love working with contract law and business agreements"
            ],
            "Architecture": [
                "I love designing buildings and structures",
                "I want to become an architect",
                "I'm passionate about sustainable design",
                "I love creating beautiful and functional spaces",
                "I want to design homes and buildings",
                "I'm interested in urban planning and development",
                "I love working with CAD and design software",
                "I want to create innovative architectural solutions",
                "I want to design sustainable and eco-friendly buildings",
                "I'm passionate about interior design and space planning",
                "I love working with architectural visualization and 3D modeling",
                "I want to specialize in residential architecture and home design",
                "I'm interested in commercial architecture and office buildings",
                "I want to work on historic preservation and restoration projects",
                "I love designing public spaces and community buildings",
                "I'm fascinated by landscape architecture and outdoor design",
                "I want to work in urban design and city planning",
                "I'm interested in architectural engineering and structural design",
                "I want to become a project architect and lead design teams",
                "I love working with building codes and construction regulations"
            ],
            "Dentistry": [
                "I want to become a dentist and help people with oral health",
                "I'm interested in dental care and treatment",
                "I want to work in dental clinics and hospitals",
                "I love helping people with their teeth and gums",
                "I'm fascinated by oral anatomy and dental procedures",
                "I want to specialize in orthodontics or oral surgery",
                "I love working with dental tools and equipment",
                "I want to improve people's smiles and oral health",
                "I want to become an orthodontist and straighten teeth",
                "I'm passionate about cosmetic dentistry and smile makeovers",
                "I love working with dental implants and prosthetics",
                "I want to specialize in pediatric dentistry and work with children",
                "I'm interested in oral and maxillofacial surgery",
                "I want to work in dental public health and community care",
                "I love working with dental technology and digital dentistry",
                "I'm fascinated by periodontics and gum disease treatment",
                "I want to become a dental hygienist and preventive care specialist",
                "I'm interested in endodontics and root canal treatment",
                "I want to work in dental research and oral health studies",
                "I love working with dental materials and restoration techniques"
            ],
            "UX/UI Design": [
                "I love designing user interfaces and creating digital experiences",
                "I want to become a UX designer and work on user experience",
                "I'm passionate about wireframing and prototyping with Figma",
                "I enjoy creating intuitive interfaces for mobile apps and websites",
                "I want to work in product design and user research",
                "I'm fascinated by usability testing and user feedback",
                "I love working with Adobe XD and Sketch for interface design",
                "I want to create beautiful and functional user experiences",
                "I'm interested in interaction design and user flows",
                "I want to become a product designer at a tech company",
                "I love conducting user research and understanding user needs",
                "I want to design mobile apps and responsive web interfaces",
                "I'm passionate about accessibility and inclusive design",
                "I love creating design systems and UI component libraries",
                "I want to work on UX strategy and information architecture",
                "I'm fascinated by human-computer interaction and psychology",
                "I love prototyping interactive designs and animations",
                "I want to specialize in web design and digital products",
                "I'm interested in UX writing and microcopy",
                "I want to work at startups designing innovative digital products"
            ],
            "Graphic Design": [
                "I love creating visual designs and brand identities",
                "I want to become a graphic designer and work with brands",
                "I'm passionate about logo design and branding projects",
                "I enjoy working with Photoshop and Illustrator for design work",
                "I want to create posters, flyers, and marketing materials",
                "I'm fascinated by typography and layout design",
                "I love working with colors, fonts, and visual compositions",
                "I want to design brand identities and corporate branding",
                "I'm interested in print design and publishing",
                "I want to become a brand designer and create visual systems",
                "I love working on packaging design and product branding",
                "I want to design social media graphics and digital content",
                "I'm passionate about illustration and creative artwork",
                "I love creating visual content for advertising campaigns",
                "I want to work in creative agencies as an art director",
                "I'm fascinated by motion graphics and animation",
                "I love designing editorial layouts for magazines and books",
                "I want to specialize in brand strategy and visual identity",
                "I'm interested in infographic design and data visualization",
                "I want to work as a freelance designer and creative director"
            ]
        }
        
        career_goals_by_major = {
            "Computer Science": ["Software Engineer", "Web Developer", "Data Scientist", "AI Engineer", "Machine Learning Engineer", "Cybersecurity Expert", "Mobile App Developer", "DevOps Engineer", "Full Stack Developer", "Game Developer"],
            "Medicine": ["Doctor", "Surgeon", "Medical Researcher", "Pharmacist", "Healthcare Administrator", "Pediatrician", "Cardiologist", "Neurologist", "Emergency Medicine Physician", "Medical Specialist"],
            "Electrical Engineering": ["Electrical Engineer", "Electronics Engineer", "Power Systems Engineer", "Control Systems Engineer", "Embedded Systems Engineer", "Telecommunications Engineer", "Electrical Designer", "Electrical Project Manager"],
            "Mechanical Engineering": ["Mechanical Engineer", "Design Engineer", "Manufacturing Engineer", "Robotics Engineer", "Automotive Engineer", "Aerospace Engineer", "Mechanical Designer", "Mechanical Project Manager"],
            "Civil Engineering": ["Civil Engineer", "Structural Engineer", "Transportation Engineer", "Water Resources Engineer", "Environmental Engineer", "Geotechnical Engineer", "Construction Engineer", "Civil Project Manager"],
            "Chemical Engineering": ["Chemical Engineer", "Process Engineer", "Plant Engineer", "Environmental Engineer", "Materials Engineer", "Petroleum Engineer", "Biochemical Engineer", "Chemical Project Manager"],
            "Data Science": ["Data Scientist", "Data Analyst", "Machine Learning Engineer", "Business Intelligence Analyst", "Research Scientist", "Data Engineer", "Statistician", "Quantitative Analyst", "Data Visualization Specialist", "Predictive Analytics Expert"],
            "Psychology": ["Psychologist", "Counselor", "Therapist", "Research Psychologist", "Clinical Psychologist", "School Psychologist", "Forensic Psychologist", "Sports Psychologist", "Industrial Psychologist", "Mental Health Counselor"],
            "Education": ["Teacher", "Principal", "Educational Consultant", "Curriculum Developer", "Education Administrator", "University Professor", "Special Education Teacher", "Educational Technology Specialist", "School Counselor", "Training and Development Manager"],
            "Business Administration": ["Business Manager", "Entrepreneur", "Financial Analyst", "Marketing Manager", "Operations Manager", "CEO", "Business Consultant", "Project Manager", "Sales Manager", "Human Resources Manager"],
            "International Relations": ["Diplomat", "Policy Analyst", "International Consultant", "Government Official", "NGO Worker", "Foreign Service Officer", "International Development Specialist", "Global Affairs Analyst", "International Trade Specialist", "Peacekeeping Officer"],
            "Law": ["Lawyer", "Judge", "Legal Advisor", "Prosecutor", "Legal Researcher", "Corporate Counsel", "Criminal Defense Attorney", "Family Lawyer", "Environmental Lawyer", "Intellectual Property Lawyer"],
            "Architecture": ["Architect", "Urban Planner", "Interior Designer", "Construction Manager", "Landscape Architect", "Project Architect", "Sustainable Design Specialist", "Historic Preservation Architect", "Commercial Architect", "Residential Architect"],
            "Dentistry": ["Dentist", "Orthodontist", "Oral Surgeon", "Dental Hygienist", "Dental Assistant", "Periodontist", "Endodontist", "Prosthodontist", "Pediatric Dentist", "Cosmetic Dentist"],
            "UX/UI Design": ["UX Designer", "UI Designer", "Product Designer", "UX Researcher", "Interaction Designer", "User Experience Architect", "UX Strategist", "Digital Product Designer", "Mobile App Designer", "Web Designer"],
            "Graphic Design": ["Graphic Designer", "Brand Designer", "Visual Designer", "Art Director", "Creative Director", "Logo Designer", "Marketing Designer", "Print Designer", "Packaging Designer", "Motion Graphics Designer"]
        }
        
        
        sample_data = []
        
        # Calculate samples per major for balanced distribution
        samples_per_major = 1000 // len(majors)  # ~71 samples per major
        remaining_samples = 1000 % len(majors)   # Distribute remainder
        
        # Generate balanced samples for each major
        for major in majors:
            # Add extra samples to first few majors if there's a remainder
            extra_samples = 1 if remaining_samples > 0 else 0
            if remaining_samples > 0:
                remaining_samples -= 1
            
            major_samples = samples_per_major + extra_samples
            
            for i in range(major_samples):
                # Generate realistic grades based on major
                if major in ["Computer Science", "Electrical Engineering", "Mechanical Engineering", "Civil Engineering", "Chemical Engineering", "Data Science"]:
                    math_grade = random.randint(80, 95)
                    physics_grade = random.randint(75, 90)
                    chemistry_grade = random.randint(70, 85)
                    biology_grade = random.randint(65, 80)
                elif major == "Medicine":
                    math_grade = random.randint(75, 90)
                    physics_grade = random.randint(70, 85)
                    chemistry_grade = random.randint(80, 95)
                    biology_grade = random.randint(85, 95)
                elif major in ["Psychology", "Education"]:
                    math_grade = random.randint(65, 80)
                    physics_grade = random.randint(60, 75)
                    chemistry_grade = random.randint(60, 75)
                    biology_grade = random.randint(70, 85)
                elif major == "Law":
                    math_grade = random.randint(70, 85)
                    physics_grade = random.randint(60, 75)
                    chemistry_grade = random.randint(60, 75)
                    biology_grade = random.randint(60, 75)
                elif major == "Architecture":
                    math_grade = random.randint(80, 90)
                    physics_grade = random.randint(75, 85)
                    chemistry_grade = random.randint(65, 80)
                    biology_grade = random.randint(60, 75)
                elif major == "Dentistry":
                    math_grade = random.randint(75, 90)
                    physics_grade = random.randint(70, 85)
                    chemistry_grade = random.randint(80, 95)
                    biology_grade = random.randint(85, 95)
                else:  # Business, International Relations
                    math_grade = random.randint(70, 85)
                    physics_grade = random.randint(60, 80)
                    chemistry_grade = random.randint(60, 80)
                    biology_grade = random.randint(60, 80)
                
                # Add some variation to make it more realistic
                math_grade += random.randint(-5, 5)
                physics_grade += random.randint(-5, 5)
                chemistry_grade += random.randint(-5, 5)
                biology_grade += random.randint(-5, 5)
                
                # Generate language grades based on major requirements
                if major in ["Law", "International Relations", "Education"]:
                    english_grade = random.randint(40, 50)  # Higher English for language-heavy majors
                    khmer_grade = random.randint(55, 75)
                    history_grade = random.randint(35, 50)  # Higher history for law/IR
                elif major in ["Architecture", "Dentistry"]:
                    english_grade = random.randint(35, 45)
                    khmer_grade = random.randint(50, 70)
                    history_grade = random.randint(30, 45)
                else:  # Default for other majors
                    english_grade = random.randint(35, 50)
                    khmer_grade = random.randint(50, 75)
                    history_grade = random.randint(30, 50)
                
                # Ensure grades stay within subject-specific max ranges
                math_grade = max(0, min(125, math_grade))
                physics_grade = max(0, min(75, physics_grade))
                chemistry_grade = max(0, min(75, chemistry_grade))
                biology_grade = max(0, min(75, biology_grade))
                english_grade = max(0, min(50, english_grade))
                khmer_grade = max(0, min(75, khmer_grade))
                history_grade = max(0, min(50, history_grade))
                
                sample_data.append({
                    "grades": {
                        "math": math_grade,
                        "physics": physics_grade,
                        "chemistry": chemistry_grade,
                        "biology": biology_grade,
                        "english": english_grade,
                        "khmer": khmer_grade,
                        "history": history_grade
                    },
                    "interests": random.choice(interests_by_major[major]),
                    "careerGoals": random.choice(career_goals_by_major[major]),
                    "studyPreference": "local",
                    "recommendedMajor": major,
                    "actualMajor": major,
                    "feedbackScore": random.randint(4, 5)  # Higher scores for better training
                })
        
        # Save sample data for future use
        with open("training_data.json", 'w') as f:
            json.dump(sample_data, f, indent=2)
        
        return pd.DataFrame(sample_data)
    
    def extract_features(self, df: pd.DataFrame) -> np.ndarray:
        """Extract enhanced features from training data including domain detection"""
        features = []
        
        for _, row in df.iterrows():
            # Grade features (normalized to 0-1) - handle both dict and JSON string formats
            grade_features = []
            subjects = ["math", "physics", "chemistry", "biology", "english", "khmer", "history"]
            subject_max_scores = {
                "math": 125,
                "physics": 75,
                "chemistry": 75,
                "biology": 75,
                "english": 50,
                "khmer": 75,
                "history": 50
            }
            
            grades = row["grades"]
            if isinstance(grades, str):
                grades = json.loads(grades)
            
            for subject in subjects:
                grade = grades.get(subject, 0)
                max_score = subject_max_scores.get(subject, 100)
                grade_features.append(grade / max_score)  # Normalize to 0-1 using subject-specific max scores
        
            # Text embedding features
            interests = row.get('interests', '') or ''
            career_goals = row.get('careerGoals', '') or ''
            combined_text = f"{interests} {career_goals}"
            text_embedding = self.sentence_model.encode([combined_text])[0]
            
            # Domain detection features
            detected_domain = self.detect_domain(combined_text)
            domain_features = [1 if domain == detected_domain else 0 for domain in ['electrical_engineering', 'mechanical_engineering', 'civil_engineering', 'chemical_engineering', 'medicine', 'business', 'technology', 'arts', 'general']]
            
            # Study preference (always local)
            study_features = [1, 0, 0]  # local, abroad, both
            
            # Additional engineered features for better accuracy
            # Grade statistics
            grade_values = [grades.get(subject, 0) for subject in subjects]
            grade_stats = [
                np.mean(grade_values),  # Average grade
                np.std(grade_values),   # Grade standard deviation
                max(grade_values),      # Highest grade
                min(grade_values),      # Lowest grade
                sum(1 for g in grade_values if g >= 80),  # Number of high grades
                sum(1 for g in grade_values if g < 60)    # Number of low grades
            ]
            
            # Text length and complexity features
            text_features = [
                len(interests.split()),      # Interest text length
                len(career_goals.split()),   # Career goals text length
                len(combined_text.split()),  # Total text length
                combined_text.count('love'), # Emotional words
                combined_text.count('want'),
                combined_text.count('passionate')
            ]
            
            # Combine all features
            feature_vector = np.concatenate([
                grade_features, 
                text_embedding, 
                study_features, 
                grade_stats, 
                text_features,
                domain_features
            ])
            features.append(feature_vector)
        
        return np.array(features)
    
    def train_domain_specific_models(self, df: pd.DataFrame) -> None:
        """Train domain-specific models for better accuracy"""
        print("Training domain-specific models...")
        
        for domain in self.domain_models.keys():
            # Filter data for this domain
            domain_data = df[df.apply(lambda row: self.detect_domain(f"{row.get('interests', '')} {row.get('careerGoals', '')}") == domain, axis=1)]
            
            if len(domain_data) < 10:  # Need minimum data
                print(f"Not enough data for {domain} domain ({len(domain_data)} samples)")
                continue
            
            print(f"Training {domain} model with {len(domain_data)} samples")
            
            # Extract features and labels
            X_domain = self.extract_features(domain_data)
            y_domain = domain_data['recommendedMajor'].tolist()
            
            # Train domain-specific model
            from sklearn.ensemble import RandomForestClassifier
            from sklearn.model_selection import cross_val_score
            
            domain_model = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                class_weight='balanced'
            )
            
            # Cross-validation
            cv_scores = cross_val_score(domain_model, X_domain, y_domain, cv=3, scoring='accuracy')
            print(f"{domain} model CV accuracy: {cv_scores.mean():.3f} (+/- {cv_scores.std() * 2:.3f})")
            
            # Train final model
            domain_model.fit(X_domain, y_domain)
            self.domain_models[domain] = domain_model
            
            # Save domain model
            os.makedirs("models", exist_ok=True)
            joblib.dump(domain_model, f"models/{domain}_classifier.pkl")
            print(f"{domain} model saved to models/{domain}_classifier.pkl")
    
    def evaluate_model(self, model, X_test: np.ndarray, y_test: List[str], model_name: str) -> Dict[str, float]:
        """Evaluate model performance with comprehensive metrics"""
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
        
        y_pred = model.predict(X_test)
        
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision_macro': precision_score(y_test, y_pred, average='macro', zero_division=0),
            'recall_macro': recall_score(y_test, y_pred, average='macro', zero_division=0),
            'f1_macro': f1_score(y_test, y_pred, average='macro', zero_division=0),
            'precision_weighted': precision_score(y_test, y_pred, average='weighted', zero_division=0),
            'recall_weighted': recall_score(y_test, y_pred, average='weighted', zero_division=0),
            'f1_weighted': f1_score(y_test, y_pred, average='weighted', zero_division=0)
        }
        
        print(f"\n{model_name} Model Evaluation:")
        print(f"Accuracy: {metrics['accuracy']:.3f}")
        print(f"Precision (macro): {metrics['precision_macro']:.3f}")
        print(f"Recall (macro): {metrics['recall_macro']:.3f}")
        print(f"F1-score (macro): {metrics['f1_macro']:.3f}")
        print(f"Precision (weighted): {metrics['precision_weighted']:.3f}")
        print(f"Recall (weighted): {metrics['recall_weighted']:.3f}")
        print(f"F1-score (weighted): {metrics['f1_weighted']:.3f}")
        
        # Detailed classification report
        print(f"\nDetailed Classification Report for {model_name}:")
        print(classification_report(y_test, y_pred, zero_division=0))
        
        return metrics
    
    def train_major_classifier(self, X: np.ndarray, y: List[str]) -> None:
        """Train major recommendation classifier"""
        print("Training major classifier...")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train Random Forest with probability calibration for better confidence estimates
        base_rf = RandomForestClassifier(
            n_estimators=500, 
            max_depth=20, 
            min_samples_split=5,
            min_samples_leaf=2,
            max_features='sqrt',
            random_state=42
        )
        calibrated = CalibratedClassifierCV(base_rf, method="isotonic", cv=5)
        calibrated.fit(X_train, y_train)
        self.major_classifier = calibrated
        
        # Evaluate with comprehensive metrics
        metrics = self.evaluate_model(self.major_classifier, X_test, y_test, "Major Classifier")
        self.model_metrics['major_classifier'] = metrics
        
        # Save model
        joblib.dump(self.major_classifier, "models/major_classifier.pkl")
        print("Major classifier saved to models/major_classifier.pkl")
    
    def train_career_classifier(self, X: np.ndarray, y: List[str]) -> None:
        """Train career recommendation classifier"""
        print("Training career classifier...")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train Logistic Regression with better parameters
        self.career_classifier = LogisticRegression(
            random_state=42, 
            max_iter=2000,
            C=1.0,
            solver='liblinear',
            class_weight='balanced'
        )
        self.career_classifier.fit(X_train, y_train)
        
        # Evaluate with comprehensive metrics
        metrics = self.evaluate_model(self.career_classifier, X_test, y_test, "Career Classifier")
        self.model_metrics['career_classifier'] = metrics
        
        # Save model
        joblib.dump(self.career_classifier, "models/career_classifier.pkl")
        print("Career classifier saved to models/career_classifier.pkl")
    
    
    def train_all_models(self, data_file: str = "training_data.json") -> None:
        """Train all recommendation models"""
        print("Starting ML model training...")
        
        # Create models directory
        os.makedirs("models", exist_ok=True)
        
        # Load data
        df = self.load_training_data(data_file)
        print(f"Loaded {len(df)} training samples")
        
        # Extract features
        X = self.extract_features(df)
        print(f"Extracted {X.shape[1]} features per sample")
        
        # Prepare labels - use actual major if available, otherwise recommended major
        major_labels = []
        for _, row in df.iterrows():
            actual_major = row.get('actualMajor') or row.get('recommendedMajor', 'Computer Science')
            major_labels.append(actual_major)
        
        # Train domain-specific models first
        self.train_domain_specific_models(df)
        
        # Train models
        self.train_major_classifier(X, major_labels)
        self.train_career_classifier(X, major_labels)  # Using major as career proxy
        
        # Mark records as processed in the database
        self.mark_records_as_processed()
        
        # Print model performance summary
        print("\n" + "="*50)
        print("MODEL TRAINING SUMMARY")
        print("="*50)
        for model_name, metrics in self.model_metrics.items():
            print(f"{model_name}:")
            print(f"  Accuracy: {metrics.get('accuracy', 0):.3f}")
            print(f"  F1-score: {metrics.get('f1_macro', 0):.3f}")
        
        print("All models trained successfully!")
    
    def predict_recommendations(self, grades: Dict[str, float], interests: str, career_goals: str = "") -> Dict[str, Any]:
        """Make predictions using trained models"""
        if not all([self.major_classifier, self.career_classifier]):
            print("Models not trained yet. Run train_all_models() first.")
            return {}
        
        # Extract features for prediction (must match training subjects)
        grade_features = []
        subjects = ["math", "physics", "chemistry", "biology", "english", "khmer", "history"]
        subject_max_scores = {
            "math": 125,
            "physics": 75,
            "chemistry": 75,
            "biology": 75,
            "english": 50,
            "khmer": 75,
            "history": 50
        }
        
        for subject in subjects:
            grade = grades.get(subject, 0)
            max_score = subject_max_scores.get(subject, 100)
            grade_features.append(grade / max_score)  # Normalize using same max scores as training
        
        combined_text = f"{interests} {career_goals}"
        text_embedding = self.sentence_model.encode([combined_text])[0]
        
        study_features = [1, 0, 0]  # local, abroad, both
        
        # Additional engineered features (must match training)
        grade_values = [grades.get(subject, 0) for subject in subjects]
        grade_stats = [
            np.mean(grade_values),  # Average grade
            np.std(grade_values),   # Grade standard deviation
            max(grade_values),      # Highest grade
            min(grade_values),      # Lowest grade
            sum(1 for g in grade_values if g >= 80),  # Number of high grades
            sum(1 for g in grade_values if g < 60)    # Number of low grades
        ]
        
        # Text length and complexity features
        text_features = [
            len(interests.split()),      # Interest text length
            len(career_goals.split()),   # Career goals text length
            len(combined_text.split()),  # Total text length
            combined_text.count('love'), # Emotional words
            combined_text.count('want'),
            combined_text.count('passionate')
        ]
        
        # Domain detection features
        detected_domain = self.detect_domain(combined_text)
        domain_features = [1 if domain == detected_domain else 0 for domain in ['electrical_engineering', 'mechanical_engineering', 'civil_engineering', 'chemical_engineering', 'medicine', 'business', 'technology', 'arts', 'general']]
        
        feature_vector = np.concatenate([
            grade_features, 
            text_embedding, 
            study_features, 
            grade_stats, 
            text_features,
            domain_features
        ]).reshape(1, -1)
        
        # Make predictions
        major_pred = self.major_classifier.predict(feature_vector)[0]
        career_pred = self.career_classifier.predict(feature_vector)[0]
        
        return {
            "predicted_major": major_pred,
            "predicted_career": career_pred,
            "predicted_university_preference": "local"  # Always local since we only have Cambodian universities
        }

def main():
    """Main training function"""
    trainer = RecommendationTrainer()
    trainer.train_all_models()
    
    # Test prediction
    print("\nTesting prediction...")
    test_grades = {"math": 85, "physics": 80, "chemistry": 75, "biology": 70, "english": 90, "khmer": 85, "history": 80, "geography": 75}
    test_interests = "I love programming and want to work with computers"
    test_career_goals = "Become a software engineer"
    
    prediction = trainer.predict_recommendations(test_grades, test_interests, test_career_goals)
    print(f"Prediction: {prediction}")

if __name__ == "__main__":
    main()
