
import requests
import json

# Terminal colors
GREEN = "\033[92m"
RED = "\033[91m"
BOLD = "\033[1m"
END = "\033[0m"

API_URL = "http://localhost:8000/api/recommend"

test_cases = [
    {"major": "Software Engineering", "grades": [{"subject": "math", "score": 110}, {"subject": "physics", "score": 60}], "interests": "I love building software and coding in Python."},
    {"major": "Medicine", "grades": [{"subject": "biology", "score": 70}, {"subject": "chemistry", "score": 70}], "interests": "I want to save lives and understand human anatomy."},
    {"major": "Electrical Engineering", "grades": [{"subject": "math", "score": 110}, {"subject": "physics", "score": 70}], "interests": "I'm interested in circuits and power systems."},
    {"major": "Mechanical Engineering", "grades": [{"subject": "math", "score": 110}, {"subject": "physics", "score": 70}], "interests": "I enjoy building machines and robotics."},
    {"major": "Civil Engineering", "grades": [{"subject": "math", "score": 110}, {"subject": "physics", "score": 70}], "interests": "I want to design bridges and infrastructure."},
    {"major": "Chemical Engineering", "grades": [{"subject": "math", "score": 110}, {"subject": "chemistry", "score": 70}], "interests": "I love chemical reactions and industrial plants."},
    {"major": "Business Administration", "grades": [{"subject": "math", "score": 90}], "interests": "I want to run a company and learn entrepreneurship."},
    {"major": "Data Science", "grades": [{"subject": "math", "score": 110}], "interests": "I like finding patterns in big data datasets."},
    {"major": "Psychology", "grades": [{"subject": "biology", "score": 65}], "interests": "I want to understand human behavior and mental health."},
    {"major": "Education", "grades": [{"subject": "english", "score": 45}], "interests": "I love teaching children and working in classrooms."},
    {"major": "International Relations", "grades": [{"subject": "history", "score": 45}], "interests": "I'm interested in diplomacy and world affairs."},
    {"major": "Architecture", "grades": [{"subject": "math", "score": 100}, {"subject": "physics", "score": 60}], "interests": "I want to design buildings and draw floor plans."},
    {"major": "Dentistry", "grades": [{"subject": "biology", "score": 70}, {"subject": "chemistry", "score": 70}], "interests": "I'm interested in oral health and helping people with their teeth."},
    {"major": "Law", "grades": [{"subject": "history", "score": 45}, {"subject": "english", "score": 45}], "interests": "I am passionate about justice and legal rights."},
    {"major": "Pharmacy", "grades": [{"subject": "biology", "score": 70}, {"subject": "chemistry", "score": 70}], "interests": "I want to study medications and drug development."},
    {"major": "Business Management", "grades": [{"subject": "math", "score": 90}], "interests": "I want to focus on leadership and team management."},
    {"major": "Finance", "grades": [{"subject": "math", "score": 110}], "interests": "I am interested in investments and banking."},
    {"major": "UX/UI Design", "grades": [{"subject": "math", "score": 80}], "interests": "I want to create beautiful interface designs and user experiences."},
    {"major": "Graphic Design", "grades": [{"subject": "history", "score": 40}], "interests": "I love branding, logos, and typography."},
    {"major": "Cybersecurity", "grades": [{"subject": "math", "score": 110}, {"subject": "physics", "score": 60}], "interests": "I want to protect data and learn ethical hacking."},
    {"major": "Telecommunication and Networking", "grades": [{"subject": "math", "score": 100}, {"subject": "physics", "score": 65}], "interests": "I'm interested in 5G technology and internet connectivity."}
]

def run_tests():
    print(f"\n{BOLD}🤖 ML SERVICE V2: COMPREHENSIVE INTELLIGENCE TEST (No Career Goals){END}")
    print("="*80)
    
    passed = 0
    total = len(test_cases)
    
    for case in test_cases:
        target = case["major"]
        payload = {
            "grades": case["grades"],
            "interests": case["interests"],
            "career_goals": "" # Explicitly empty
        }
        
        try:
            response = requests.post(API_URL, json=payload)
            response.raise_for_status()
            data = response.json()
            
            majors = data.get("majors", [])
            top_prediction = majors[0]["major"] if majors else "NONE"
            prob = majors[0]["probability"] if majors else 0
            
            if top_prediction == target:
                print(f"{GREEN}PASS{END} | Target: {target:<30} | Predicted: {top_prediction:<30} | Prob: {prob:.4f}")
                passed += 1
            else:
                # Check if it's in top 2 for close matches
                second = majors[1]["major"] if len(majors) > 1 else "NONE"
                if second == target:
                    print(f"{GREEN}PASS (Rank 2){END} | Target: {target:<30} | Top: {top_prediction:<30} | Prob: {prob:.4f}")
                    passed += 1
                else:
                    print(f"{RED}FAIL{END} | Target: {target:<30} | Predicted: {top_prediction:<30} | Prob: {prob:.4f}")
        
        except Exception as e:
            print(f"{RED}ERROR{END} | Target: {target:<30} | {str(e)}")
            
    print("="*80)
    print(f"RESULT: {passed}/{total} instances were successfully identified semantically.")
    print("="*80)

if __name__ == "__main__":
    run_tests()
