"""
Comprehensive ML Service Test Script
Tests all majors with realistic human-like inputs

FRONTEND STRUCTURE (GradeInputForm.tsx):
  - grades: [{subject, score}]
  - interest_text: Combined "Interests & Strengths" field (single textarea)
  - career_goals: Optional career goals field

This test uses the FRONTEND /analyze endpoint format.
"""
import requests
import json
from typing import Dict, List, Any

BASE_URL = "http://localhost:8000"

def test_analyze(test_name: str, data: Dict[str, Any]) -> Dict:
    """Send analyze request (frontend format) and return results"""
    print(f"\n{'='*60}")
    print(f"TEST: {test_name}")
    print(f"{'='*60}")
    
    # Show input summary
    interests = data.get('interest_text', 'N/A')
    career = data.get('career_goals', '')
    print(f"Interests: {interests[:80]}..." if len(interests) > 80 else f"Interests: {interests}")
    print(f"Career Goal: {career[:80] if career else 'None'}")
    
    try:
        # Use /api/analyze endpoint (frontend format)
        response = requests.post(f"{BASE_URL}/api/analyze", json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        # Show top recommendations (frontend format: majors[].name, majors[].score)
        print(f"\nTop 5 Major Recommendations:")
        for i, major in enumerate(result.get("majors", [])[:5], 1):
            score = major.get("score", 0) * 100
            print(f"  {i}. {major['name']}: {score:.1f}%")
        
        # Show career paths for top recommendation
        careers = result.get("careers", [])
        if careers:
            print(f"\nCareer Paths (Top Major):")
            for i, career in enumerate(careers[:3], 1):
                print(f"  {i}. {career}")
        
        # Show recommended universities
        universities = result.get("universities", [])
        if universities:
            print(f"\nRecommended Universities ({len(universities)} total):")
            for i, uni in enumerate(universities, 1):
                name = uni.get("name", uni) if isinstance(uni, dict) else uni
                fit = uni.get("fit", "") if isinstance(uni, dict) else ""
                programs = uni.get("programs", []) if isinstance(uni, dict) else []
                fit_str = f" ({fit})" if fit else ""
                print(f"  {i}. {name}{fit_str} - Programs: {', '.join(programs)}")
        
        # Show skill gaps
        print(f"\nSkill Gaps:")
        for gap in result.get("skill_gaps", [])[:3]:
            print(f"  - {gap['skill']}: {gap['current_level']:.1f} → {gap['required_level']:.1f}")
        
        # Show subject analysis summary
        print(f"\nSubject Analysis:")
        for subj, analysis in result.get("subject_analysis", {}).items():
            print(f"  - {subj}: {analysis['score']} ({analysis['strength']})")
        
        return result
    except requests.exceptions.HTTPError as e:
        print(f"HTTP ERROR: {e}")
        print(f"Response: {e.response.text[:500] if e.response else 'No response'}")
        return {}
    except Exception as e:
        print(f"ERROR: {e}")
        return {}


def run_all_tests():
    """Run comprehensive tests for all major types"""
    
    # =========================================================================
    # TEST 1: SOFTWARE ENGINEERING - With Career Goal
    # =========================================================================
    test_analyze(
        "SOFTWARE ENGINEERING Student (WITH Career Goal)",
        {
            "grades": [
                {"subject": "math", "score": 110},
                {"subject": "physics", "score": 65},
                {"subject": "chemistry", "score": 55},
                {"subject": "biology", "score": 50},
                {"subject": "english", "score": 35},
                {"subject": "khmer", "score": 55},
                {"subject": "history", "score": 30}
            ],
            "interest_text": "I love programming and building apps. I enjoy solving complex coding problems and learning new technologies like Python and JavaScript. My strengths are logic, problem-solving, and analytical thinking.",
            "career_goals": "I want to become a software engineer and work at a tech company like Google or Microsoft"
        }
    )
    
    # =========================================================================
    # TEST 2: SOFTWARE ENGINEERING - Without Career Goal
    # =========================================================================
    test_analyze(
        "SOFTWARE ENGINEERING Student (WITHOUT Career Goal)",
        {
            "grades": [
                {"subject": "math", "score": 115},
                {"subject": "physics", "score": 60},
                {"subject": "chemistry", "score": 50},
                {"subject": "biology", "score": 45},
                {"subject": "english", "score": 40},
                {"subject": "khmer", "score": 50},
                {"subject": "history", "score": 35}
            ],
            "interest_text": "I really enjoy coding and creating websites. I spend my free time learning programming languages and building small projects. I'm good at technical stuff and analytical thinking.",
            "career_goals": ""
        }
    )
    
    # =========================================================================
    # TEST 3: MEDICINE Student - With Career Goal
    # =========================================================================
    test_analyze(
        "MEDICINE Student (WITH Career Goal)",
        {
            "grades": [
                {"subject": "math", "score": 85},
                {"subject": "physics", "score": 55},
                {"subject": "chemistry", "score": 70},
                {"subject": "biology", "score": 72},
                {"subject": "english", "score": 40},
                {"subject": "khmer", "score": 60},
                {"subject": "history", "score": 35}
            ],
            "interest_text": "I am fascinated by the human body and how it works. I want to help people who are sick and make them healthy again. I have strong empathy, patience, and memorization skills.",
            "career_goals": "I dream of becoming a doctor and working in a hospital to save lives"
        }
    )
    
    # =========================================================================
    # TEST 4: MEDICINE Student - Without Career Goal
    # =========================================================================
    test_analyze(
        "MEDICINE Student (WITHOUT Career Goal)",
        {
            "grades": [
                {"subject": "math", "score": 80},
                {"subject": "physics", "score": 50},
                {"subject": "chemistry", "score": 68},
                {"subject": "biology", "score": 70},
                {"subject": "english", "score": 38},
                {"subject": "khmer", "score": 55},
                {"subject": "history", "score": 30}
            ],
            "interest_text": "I love biology and learning about health. I enjoy helping sick people and understanding diseases. I'm caring, patient, and detail-oriented.",
            "career_goals": ""
        }
    )
    
    # =========================================================================
    # TEST 5: BUSINESS ADMINISTRATION - With Career Goal
    # =========================================================================
    test_analyze(
        "BUSINESS ADMINISTRATION Student (WITH Career Goal)",
        {
            "grades": [
                {"subject": "math", "score": 75},
                {"subject": "physics", "score": 45},
                {"subject": "chemistry", "score": 40},
                {"subject": "biology", "score": 42},
                {"subject": "english", "score": 45},
                {"subject": "khmer", "score": 65},
                {"subject": "history", "score": 40}
            ],
            "interest_text": "I am interested in running a business and making money. I like learning about marketing, finance, and how companies operate. My strengths are leadership, communication, and strategic thinking.",
            "career_goals": "I want to start my own company and become a successful entrepreneur or CEO"
        }
    )
    
    # =========================================================================
    # TEST 6: BUSINESS - Without Career Goal
    # =========================================================================
    test_analyze(
        "BUSINESS Student (WITHOUT Career Goal)",
        {
            "grades": [
                {"subject": "math", "score": 70},
                {"subject": "physics", "score": 40},
                {"subject": "chemistry", "score": 38},
                {"subject": "biology", "score": 40},
                {"subject": "english", "score": 42},
                {"subject": "khmer", "score": 60},
                {"subject": "history", "score": 38}
            ],
            "interest_text": "I enjoy learning about how businesses work and I like the idea of managing teams and making important decisions. I'm a natural leader and good at teamwork.",
            "career_goals": ""
        }
    )
    
    # =========================================================================
    # TEST 7: LAW Student - With Career Goal
    # =========================================================================
    test_analyze(
        "LAW Student (WITH Career Goal)",
        {
            "grades": [
                {"subject": "math", "score": 60},
                {"subject": "physics", "score": 35},
                {"subject": "chemistry", "score": 40},
                {"subject": "biology", "score": 38},
                {"subject": "english", "score": 45},
                {"subject": "khmer", "score": 70},
                {"subject": "history", "score": 48}
            ],
            "interest_text": "I love debating and arguing about justice and rights. I am fascinated by the legal system and how laws protect people. My strengths are critical thinking, communication, and persuasion.",
            "career_goals": "I want to become a lawyer and fight for justice in court"
        }
    )
    
    # =========================================================================
    # TEST 8: LAW Student - Without Career Goal
    # =========================================================================
    test_analyze(
        "LAW Student (WITHOUT Career Goal)",
        {
            "grades": [
                {"subject": "math", "score": 55},
                {"subject": "physics", "score": 30},
                {"subject": "chemistry", "score": 35},
                {"subject": "biology", "score": 35},
                {"subject": "english", "score": 43},
                {"subject": "khmer", "score": 68},
                {"subject": "history", "score": 45}
            ],
            "interest_text": "I enjoy reading about laws and human rights. I like understanding rules and how society works. I'm good at logic, reading, and writing.",
            "career_goals": ""
        }
    )
    
    # =========================================================================
    # TEST 9: PSYCHOLOGY Student - With Career Goal
    # =========================================================================
    test_analyze(
        "PSYCHOLOGY Student (WITH Career Goal)",
        {
            "grades": [
                {"subject": "math", "score": 65},
                {"subject": "physics", "score": 40},
                {"subject": "chemistry", "score": 45},
                {"subject": "biology", "score": 55},
                {"subject": "english", "score": 42},
                {"subject": "khmer", "score": 60},
                {"subject": "history", "score": 40}
            ],
            "interest_text": "I am fascinated by human behavior and the mind. I love understanding why people act the way they do and helping them with their problems. I have strong empathy and listening skills.",
            "career_goals": "I want to become a psychologist or counselor to help people with mental health issues"
        }
    )
    
    # =========================================================================
    # TEST 10: PSYCHOLOGY - Without Career Goal
    # =========================================================================
    test_analyze(
        "PSYCHOLOGY Student (WITHOUT Career Goal)",
        {
            "grades": [
                {"subject": "math", "score": 60},
                {"subject": "physics", "score": 38},
                {"subject": "chemistry", "score": 42},
                {"subject": "biology", "score": 52},
                {"subject": "english", "score": 40},
                {"subject": "khmer", "score": 58},
                {"subject": "history", "score": 38}
            ],
            "interest_text": "I enjoy learning about the human mind and behavior. I like talking to people and understanding their feelings. I'm empathetic and a good communicator.",
            "career_goals": ""
        }
    )
    
    # =========================================================================
    # TEST 11: ELECTRICAL ENGINEERING - With Career Goal
    # =========================================================================
    test_analyze(
        "ELECTRICAL ENGINEERING Student (WITH Career Goal)",
        {
            "grades": [
                {"subject": "math", "score": 105},
                {"subject": "physics", "score": 70},
                {"subject": "chemistry", "score": 50},
                {"subject": "biology", "score": 45},
                {"subject": "english", "score": 35},
                {"subject": "khmer", "score": 50},
                {"subject": "history", "score": 30}
            ],
            "interest_text": "I love working with electronics and circuits. I enjoy building electronic devices and understanding how electrical systems work. I'm technical and good at problem-solving and mathematics.",
            "career_goals": "I want to become an electrical engineer and design electronic systems"
        }
    )
    
    # =========================================================================
    # TEST 12: DATA SCIENCE - With Career Goal
    # =========================================================================
    test_analyze(
        "DATA SCIENCE Student (WITH Career Goal)",
        {
            "grades": [
                {"subject": "math", "score": 115},
                {"subject": "physics", "score": 60},
                {"subject": "chemistry", "score": 50},
                {"subject": "biology", "score": 48},
                {"subject": "english", "score": 38},
                {"subject": "khmer", "score": 52},
                {"subject": "history", "score": 32}
            ],
            "interest_text": "I love working with data and finding patterns. I enjoy statistics, machine learning, and using Python to analyze large datasets. My strengths are analytical and statistical thinking.",
            "career_goals": "I want to become a data scientist and use AI to solve real-world problems"
        }
    )
    
    # =========================================================================
    # TEST 13: ARCHITECTURE - With Career Goal
    # =========================================================================
    test_analyze(
        "ARCHITECTURE Student (WITH Career Goal)",
        {
            "grades": [
                {"subject": "math", "score": 90},
                {"subject": "physics", "score": 55},
                {"subject": "chemistry", "score": 45},
                {"subject": "biology", "score": 42},
                {"subject": "english", "score": 35},
                {"subject": "khmer", "score": 55},
                {"subject": "history", "score": 40}
            ],
            "interest_text": "I love designing buildings and creating beautiful spaces. I enjoy drawing floor plans and thinking about how people live in buildings. I'm creative with strong spatial thinking and design skills.",
            "career_goals": "I want to become an architect and design modern buildings"
        }
    )
    
    # =========================================================================
    # TEST 14: CYBERSECURITY - With Career Goal
    # =========================================================================
    test_analyze(
        "CYBERSECURITY Student (WITH Career Goal)",
        {
            "grades": [
                {"subject": "math", "score": 100},
                {"subject": "physics", "score": 58},
                {"subject": "chemistry", "score": 48},
                {"subject": "biology", "score": 45},
                {"subject": "english", "score": 36},
                {"subject": "khmer", "score": 50},
                {"subject": "history", "score": 32}
            ],
            "interest_text": "I am fascinated by hacking and computer security. I love finding vulnerabilities in systems and learning about encryption. I'm good at problem-solving and analytical thinking.",
            "career_goals": "I want to become a cybersecurity expert and protect companies from hackers"
        }
    )
    
    # =========================================================================
    # TEST 15: GRAPHIC DESIGN - With Career Goal
    # =========================================================================
    test_analyze(
        "GRAPHIC DESIGN Student (WITH Career Goal)",
        {
            "grades": [
                {"subject": "math", "score": 55},
                {"subject": "physics", "score": 35},
                {"subject": "chemistry", "score": 38},
                {"subject": "biology", "score": 40},
                {"subject": "english", "score": 40},
                {"subject": "khmer", "score": 60},
                {"subject": "history", "score": 42}
            ],
            "interest_text": "I love creating visual designs, logos, and posters. I enjoy using Photoshop and Illustrator to make beautiful graphics. I'm creative with strong visual thinking and artistic skills.",
            "career_goals": "I want to become a graphic designer and work in advertising or branding"
        }
    )
    
    # =========================================================================
    # TEST 16: EDUCATION/TEACHING - With Career Goal
    # =========================================================================
    test_analyze(
        "EDUCATION Student (WITH Career Goal)",
        {
            "grades": [
                {"subject": "math", "score": 70},
                {"subject": "physics", "score": 45},
                {"subject": "chemistry", "score": 42},
                {"subject": "biology", "score": 48},
                {"subject": "english", "score": 42},
                {"subject": "khmer", "score": 65},
                {"subject": "history", "score": 40}
            ],
            "interest_text": "I love teaching and helping students learn. I enjoy explaining difficult concepts in simple ways and seeing students succeed. My strengths are patience and communication.",
            "career_goals": "I want to become a teacher and inspire young students"
        }
    )
    
    # =========================================================================
    # TEST 17: INTERNATIONAL RELATIONS - With Career Goal
    # =========================================================================
    test_analyze(
        "INTERNATIONAL RELATIONS Student (WITH Career Goal)",
        {
            "grades": [
                {"subject": "math", "score": 60},
                {"subject": "physics", "score": 35},
                {"subject": "chemistry", "score": 38},
                {"subject": "biology", "score": 40},
                {"subject": "english", "score": 45},
                {"subject": "khmer", "score": 62},
                {"subject": "history", "score": 48}
            ],
            "interest_text": "I am interested in global politics and diplomacy. I enjoy learning about different countries and international organizations like the UN. I'm good at communication and have cultural awareness.",
            "career_goals": "I want to become a diplomat and represent my country abroad"
        }
    )
    
    # =========================================================================
    # TEST 18: PHARMACY - With Career Goal
    # =========================================================================
    test_analyze(
        "PHARMACY Student (WITH Career Goal)",
        {
            "grades": [
                {"subject": "math", "score": 80},
                {"subject": "physics", "score": 50},
                {"subject": "chemistry", "score": 68},
                {"subject": "biology", "score": 65},
                {"subject": "english", "score": 38},
                {"subject": "khmer", "score": 55},
                {"subject": "history", "score": 32}
            ],
            "interest_text": "I am interested in medications and how drugs work in the body. I enjoy chemistry and want to help people through pharmaceutical care. I have good attention to detail.",
            "career_goals": "I want to become a pharmacist and work in a pharmacy or hospital"
        }
    )
    
    # =========================================================================
    # TEST 19: DENTISTRY - With Career Goal
    # =========================================================================
    test_analyze(
        "DENTISTRY Student (WITH Career Goal)",
        {
            "grades": [
                {"subject": "math", "score": 78},
                {"subject": "physics", "score": 48},
                {"subject": "chemistry", "score": 65},
                {"subject": "biology", "score": 68},
                {"subject": "english", "score": 36},
                {"subject": "khmer", "score": 55},
                {"subject": "history", "score": 30}
            ],
            "interest_text": "I am interested in oral health and dental care. I want to help people have healthy teeth and beautiful smiles. I have manual dexterity and attention to detail.",
            "career_goals": "I want to become a dentist and open my own dental clinic"
        }
    )
    
    # =========================================================================
    # TEST 20: LOW MATH STUDENT - Should NOT get Engineering
    # =========================================================================
    test_analyze(
        "LOW MATH Student (Should NOT recommend Engineering/CS)",
        {
            "grades": [
                {"subject": "math", "score": 40},  # Below threshold
                {"subject": "physics", "score": 30},
                {"subject": "chemistry", "score": 35},
                {"subject": "biology", "score": 45},
                {"subject": "english", "score": 38},
                {"subject": "khmer", "score": 60},
                {"subject": "history", "score": 42}
            ],
            "interest_text": "I want to study software engineering and become a programmer. I enjoy coding.",
            "career_goals": "I want to be a software engineer"
        }
    )
    
    # =========================================================================
    # TEST 21: BALANCED STUDENT - No Clear Interest
    # =========================================================================
    test_analyze(
        "BALANCED Student (No Clear Interest - Grade-Based Inference)",
        {
            "grades": [
                {"subject": "math", "score": 85},
                {"subject": "physics", "score": 55},
                {"subject": "chemistry", "score": 55},
                {"subject": "biology", "score": 55},
                {"subject": "english", "score": 40},
                {"subject": "khmer", "score": 55},
                {"subject": "history", "score": 40}
            ],
            "interest_text": "",
            "career_goals": ""
        }
    )
    
    # =========================================================================
    # TEST 22: FINANCE Student - With Career Goal
    # =========================================================================
    test_analyze(
        "FINANCE Student (WITH Career Goal)",
        {
            "grades": [
                {"subject": "math", "score": 95},
                {"subject": "physics", "score": 45},
                {"subject": "chemistry", "score": 42},
                {"subject": "biology", "score": 40},
                {"subject": "english", "score": 42},
                {"subject": "khmer", "score": 55},
                {"subject": "history", "score": 38}
            ],
            "interest_text": "I love working with numbers and analyzing financial data. I enjoy learning about stock markets, investments, and banking. I'm analytical and detail-oriented.",
            "career_goals": "I want to become a financial analyst or work in investment banking"
        }
    )
    
    # =========================================================================
    # TEST 23: SUBJECT INTEREST - "I love chemistry"
    # =========================================================================
    test_analyze(
        "SUBJECT INTEREST: 'I love chemistry' (Should boost Chemistry-related majors)",
        {
            "grades": [
                {"subject": "math", "score": 80},
                {"subject": "physics", "score": 50},
                {"subject": "chemistry", "score": 65},
                {"subject": "biology", "score": 60},
                {"subject": "english", "score": 38},
                {"subject": "khmer", "score": 55},
                {"subject": "history", "score": 35}
            ],
            "interest_text": "I love chemistry and want to learn more about chemical reactions. I enjoy experiments in the lab.",
            "career_goals": ""
        }
    )
    
    # =========================================================================
    # TEST 24: SUBJECT INTEREST - "I love biology"
    # =========================================================================
    test_analyze(
        "SUBJECT INTEREST: 'I love biology' (Should boost Medicine/Pharmacy)",
        {
            "grades": [
                {"subject": "math", "score": 75},
                {"subject": "physics", "score": 45},
                {"subject": "chemistry", "score": 60},
                {"subject": "biology", "score": 68},
                {"subject": "english", "score": 40},
                {"subject": "khmer", "score": 55},
                {"subject": "history", "score": 35}
            ],
            "interest_text": "I love biology and the human body. I want to understand how living things work.",
            "career_goals": ""
        }
    )
    
    # =========================================================================
    # TEST 25: SUBJECT INTEREST - "I love math"
    # =========================================================================
    test_analyze(
        "SUBJECT INTEREST: 'I love math' (Should boost Engineering/Data Science)",
        {
            "grades": [
                {"subject": "math", "score": 100},
                {"subject": "physics", "score": 55},
                {"subject": "chemistry", "score": 45},
                {"subject": "biology", "score": 40},
                {"subject": "english", "score": 35},
                {"subject": "khmer", "score": 50},
                {"subject": "history", "score": 30}
            ],
            "interest_text": "I love math and solving mathematical problems. Numbers are my passion.",
            "career_goals": ""
        }
    )
    
    print("\n" + "="*60)
    print("ALL TESTS COMPLETED")
    print("="*60)


if __name__ == "__main__":
    print("="*60)
    print("  ML SERVICE COMPREHENSIVE TEST SUITE")
    print("  Testing all majors with human-like inputs")
    print("  Using FRONTEND format (interest_text, career_goals)")
    print("="*60)
    
    # Check if service is running
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"\n[OK] ML Service is running: {response.json()}")
    except:
        print("\n[ERROR] ML Service is not running!")
        print("  Start it with: uvicorn app.main:app --reload --port 8000")
        exit(1)
    
    run_all_tests()
