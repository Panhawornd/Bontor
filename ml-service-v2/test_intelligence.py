
import requests
import json
import time

URL = "http://localhost:8000/api/recommend"
ANALYZE_URL = "http://localhost:8000/analyze"


def log_result(text):
    with open("test_output.log", "a", encoding="utf-8") as f:
        f.write(text + "\n")
    print(text)

def test_persona(name, description, data):
    log_result("\n" + "="*60)
    log_result(f" TEST CASE: {name}")
    log_result("="*60)
    log_result(f" PROFILE: {description}")
    log_result(f" GRADES: Math {data['grades'][0]['score']}, Physics {data['grades'][1]['score']}...")
    log_result(f" INTERESTS: \"{data['interests']}\"")
    log_result("-" * 60)
    
    try:
        start_time = time.time()
        response = requests.post(URL, json=data)
        duration = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            
            # Print Match Percentage
            log_result(f"\n SUCCESS ({duration:.2f}s) - Match Confidence: {result['match_percentage']}%")
            
            # Get top major for validation
            top_major = result['major_recommendations'][0]['major'] if result['major_recommendations'] else None
            
            # Print Top Recommendations
            log_result("\n TOP RECOMMENDED MAJORS:")
            for i, major in enumerate(result['major_recommendations'][:3], 1):
                rule_note = " (Rule Penalty Applied)" if major.get('rule_applied') else ""
                log_result(f"   {i}. {major['major']} (Conf: {major['confidence']:.1%}) {rule_note}")
                
            # Print Career Matches with validation
            log_result("\n CAREER SUGGESTIONS:")
            careers_match = False
            for i, career in enumerate(result['career_recommendations'][:2], 1):
                related = career.get('related_major', '')
                match_indicator = "✓" if related == top_major else ""
                log_result(f"   {i}. {career['name']} (Salary: {career['avg_salary']}) {match_indicator}")
                if related == top_major:
                    careers_match = True
            
            if not careers_match:
                log_result("   ⚠ Warning: Top careers don't match top major")

            # Print University with validation
            log_result("\n UNIVERSITIES (matching programs):")
            uni_match = False
            for i, uni in enumerate(result['universities'][:2], 1):
                programs = uni.get('matching_programs', [])
                has_top_major = top_major in programs
                match_indicator = "✓" if has_top_major else ""
                log_result(f"   {i}. {uni['name']} - {uni['fit']} {match_indicator}")
                log_result(f"      Programs: {', '.join(programs[:3])}")
                if has_top_major:
                    uni_match = True
            
            if not uni_match:
                log_result("   ⚠ Warning: Top universities don't offer top major")
            
            # Print Skill Gaps if any
            if result['skill_gaps']:
                log_result("\n SKILL GAP ANALYSIS (Current → Required):")
                for gap in result['skill_gaps'][:4]:
                    current = gap.get('current_level', 0)
                    required = gap.get('required_level', 0)
                    importance = gap.get('importance', 'medium')
                    skill_type = gap.get('skill_type', 'fundamental')
                    bar_current = "█" * int(current)
                    bar_required = "░" * int(required - current) if required > current else ""
                    log_result(f"   [{importance.upper():8}] {gap['skill']}")
                    log_result(f"            Current: {current:.1f}/10 {bar_current}{bar_required}")
                    log_result(f"            Goal:    {required:.1f}/10 | Type: {skill_type}")
        else:
            log_result(f" ERROR: {response.status_code}")
            log_result(response.text)
            
    except Exception as e:
        log_result(f" FAILED: Is the server running? {e}")

# ==========================================
# TEST CASE 1: THE SOFTWARE ENGINEER
# ==========================================
student_tech = {
    "grades": [
        {"subject": "math", "score": 115},      # High Math
        {"subject": "physics", "score": 70},    # High Physics
        {"subject": "chemistry", "score": 50},
        {"subject": "biology", "score": 40},
        {"subject": "english", "score": 45},
        {"subject": "khmer", "score": 50},
        {"subject": "history", "score": 30}
    ],
    "interests": "I love building backend systems, python, and solving algorithms.",
    "career_goals": "Software Engineer or AI Researcher",
    "strengths": "logical thinking, coding",
    "preferences": "building, innovation"
}

# ==========================================
# TEST CASE 2: THE DOCTOR
# ==========================================
student_med = {
    "grades": [
        {"subject": "math", "score": 90},
        {"subject": "physics", "score": 50},
        {"subject": "chemistry", "score": 75},  # Max Chem
        {"subject": "biology", "score": 75},    # Max Bio
        {"subject": "english", "score": 40},
        {"subject": "khmer", "score": 60},
        {"subject": "history", "score": 40}
    ],
    "interests": "I want to help patients and study human anatomy.",
    "career_goals": "Doctor or Surgeon",
    "strengths": "empathy, memorization",
    "preferences": "helping people, healthcare"
}

# ==========================================
# TEST CASE 3: THE UNQALIFIED DREAMER (Rule Check)
# ==========================================
# Wants Engineering but fails Math threshold (< 50%)
# Math Max is 125. 50% is 62.5. Student has 40.
student_fail_math = {
    "grades": [
        {"subject": "math", "score": 40},       # <--- FAILS RULE for Engineering
        {"subject": "physics", "score": 40},
        {"subject": "chemistry", "score": 40},
        {"subject": "biology", "score": 40},
        {"subject": "english", "score": 45},    # High English
        {"subject": "khmer", "score": 70},      # High Khmer
        {"subject": "history", "score": 45}     # High History
    ],
    "interests": "I love robots and civil engineering and building bridges.",
    "career_goals": "Civil Engineer",
    "strengths": "creativity",
    "preferences": "design"
}


def test_analyze_endpoint():
    """Test the /analyze endpoint used by the frontend"""
    log_result("\n" + "="*60)
    log_result(" TESTING /analyze ENDPOINT (Frontend Compatible)")
    log_result("="*60)
    
    # Frontend-style request format
    data = {
        "grades": [
            {"subject": "math", "score": 100},
            {"subject": "physics", "score": 65},
            {"subject": "chemistry", "score": 50},
            {"subject": "biology", "score": 45},
            {"subject": "english", "score": 40},
            {"subject": "khmer", "score": 55},
            {"subject": "history", "score": 35}
        ],
        "interest_text": "I enjoy creating mobile apps and learning about AI",
        "career_goals": "App Developer"
    }
    
    try:
        start_time = time.time()
        response = requests.post(ANALYZE_URL, json=data)
        duration = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            
            log_result(f"\n SUCCESS ({duration:.2f}s)")
            
            # Validate response format
            log_result("\n RESPONSE STRUCTURE VALIDATION:")
            log_result(f"   ✓ majors: {len(result.get('majors', []))} items")
            log_result(f"   ✓ careers: {len(result.get('careers', []))} items")
            log_result(f"   ✓ universities: {len(result.get('universities', []))} items")
            log_result(f"   ✓ skill_gaps: {len(result.get('skill_gaps', []))} items")
            log_result(f"   ✓ subject_analysis: {len(result.get('subject_analysis', {}))} subjects")
            
            # Show skill gaps with chart-ready format
            log_result("\n SKILL GAPS (Chart-Ready Format):")
            for gap in result.get('skill_gaps', [])[:4]:
                log_result(f"   {gap['skill']}: {gap['current_level']:.1f} → {gap['required_level']:.1f}")
            
            # Validate frontend requirements
            if result.get('skill_gaps'):
                gap = result['skill_gaps'][0]
                assert isinstance(gap['current_level'], (int, float)), "current_level should be numeric"
                assert isinstance(gap['required_level'], (int, float)), "required_level should be numeric"
                log_result("\n ✓ Skill gap levels are numeric (chart-compatible)")
        else:
            log_result(f" ERROR: {response.status_code}")
            log_result(response.text)
            
    except Exception as e:
        log_result(f" FAILED: {e}")


def test_minimal_input(name, description, data, expected_categories):
    """Test with minimal/sparse user input
    
    Args:
        expected_categories: list of acceptable major categories (any match = pass)
    """
    log_result("\n" + "="*60)
    log_result(f" MINIMAL INPUT TEST: {name}")
    log_result("="*60)
    log_result(f" SCENARIO: {description}")
    log_result(f" INTERESTS: \"{data.get('interests', data.get('interest_text', ''))}\"")
    log_result(f" CAREER GOALS: \"{data.get('career_goals', '')}\"")
    log_result(f" EXPECTED: Should recommend {'/'.join(expected_categories)}")
    log_result("-" * 60)
    
    try:
        start_time = time.time()
        # Use analyze endpoint for frontend-style requests
        response = requests.post(ANALYZE_URL, json=data)
        duration = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            
            top_major = result['majors'][0]['name'] if result['majors'] else "None"
            top_score = result['majors'][0]['score'] if result['majors'] else 0
            
            log_result(f"\n SUCCESS ({duration:.2f}s)")
            log_result(f"\n TOP RECOMMENDATION: {top_major} ({top_score:.1%})")
            
            # Check if TOP recommendation matches any expected category
            top_match = any(cat.lower() in top_major.lower() for cat in expected_categories)
            
            # Also check if ANY of top-4 recommendations match expected
            top4_majors = [m['name'] for m in result['majors'][:4]]
            any_match = any(
                any(cat.lower() in major.lower() for cat in expected_categories)
                for major in top4_majors
            )
            
            if top_match:
                status = "✓ CORRECT (Top-1)"
                is_correct = True
            elif any_match:
                status = "✓ ACCEPTABLE (in Top-4)"
                is_correct = True
            else:
                status = "⚠ UNEXPECTED"
                is_correct = False
                
            log_result(f" {status}")
            
            # Show all recommendations
            log_result("\n ALL MAJORS:")
            for i, major in enumerate(result['majors'][:4], 1):
                log_result(f"   {i}. {major['name']} ({major['score']:.1%})")
            
            # Show skill gaps
            if result['skill_gaps']:
                log_result("\n SKILL ANALYSIS:")
                for gap in result['skill_gaps'][:3]:
                    log_result(f"   • {gap['skill']}: {gap['current_level']:.1f} → {gap['required_level']:.1f}")
            
            return is_correct
        else:
            log_result(f" ERROR: {response.status_code}")
            log_result(response.text)
            return False
            
    except Exception as e:
        log_result(f" FAILED: {e}")
        return False


# ==========================================
# MINIMAL INPUT TEST CASES
# ==========================================

# Test 1: Only grades, no interests
minimal_grades_only = {
    "grades": [
        {"subject": "math", "score": 120},      # Very high math
        {"subject": "physics", "score": 70},    # High physics
        {"subject": "chemistry", "score": 40},
        {"subject": "biology", "score": 35},
        {"subject": "english", "score": 30},
        {"subject": "khmer", "score": 45},
        {"subject": "history", "score": 25}
    ],
    "interest_text": "",  # Empty!
    "career_goals": ""    # Empty!
}

# Test 2: Vague one-word interest
minimal_vague_interest = {
    "grades": [
        {"subject": "math", "score": 60},
        {"subject": "physics", "score": 50},
        {"subject": "chemistry", "score": 70},
        {"subject": "biology", "score": 75},    # Highest
        {"subject": "english", "score": 40},
        {"subject": "khmer", "score": 55},
        {"subject": "history", "score": 35}
    ],
    "interest_text": "health",  # Just one word
    "career_goals": ""
}

# Test 3: Only career goal, no interests
minimal_career_only = {
    "grades": [
        {"subject": "math", "score": 80},
        {"subject": "physics", "score": 55},
        {"subject": "chemistry", "score": 45},
        {"subject": "biology", "score": 40},
        {"subject": "english", "score": 45},
        {"subject": "khmer", "score": 60},
        {"subject": "history", "score": 50}
    ],
    "interest_text": "",
    "career_goals": "engineer"  # Just one word
}

# Test 4: Typos and informal language
minimal_typos = {
    "grades": [
        {"subject": "math", "score": 100},
        {"subject": "physics", "score": 60},
        {"subject": "chemistry", "score": 45},
        {"subject": "biology", "score": 40},
        {"subject": "english", "score": 35},
        {"subject": "khmer", "score": 50},
        {"subject": "history", "score": 30}
    ],
    "interest_text": "i like making apps and stuff",  # Informal
    "career_goals": "developer"
}

# Test 5: Average grades, balanced student
minimal_balanced = {
    "grades": [
        {"subject": "math", "score": 70},
        {"subject": "physics", "score": 45},
        {"subject": "chemistry", "score": 50},
        {"subject": "biology", "score": 50},
        {"subject": "english", "score": 40},
        {"subject": "khmer", "score": 55},
        {"subject": "history", "score": 40}
    ],
    "interest_text": "business",
    "career_goals": ""
}

# Test 6: Strong humanities, wants tech (contradiction)
minimal_contradiction = {
    "grades": [
        {"subject": "math", "score": 45},       # Low math
        {"subject": "physics", "score": 35},    # Low physics
        {"subject": "chemistry", "score": 40},
        {"subject": "biology", "score": 45},
        {"subject": "english", "score": 48},    # High english
        {"subject": "khmer", "score": 70},      # High khmer
        {"subject": "history", "score": 45}     # High history
    ],
    "interest_text": "coding programming",  # Wants tech but grades don't match
    "career_goals": "software developer"
}


if __name__ == "__main__":
    print("🚀 STARTING INTELLIGENCE TEST...")
    
    print("\n" + "="*70)
    print(" PART 1: DETAILED INPUT TESTS")
    print("="*70)
    test_persona("THE TECH WHIZ", "High Math/Physics + Coding Interest", student_tech)
    test_persona("THE ASPIRING DOCTOR", "High Bio/Chem + Medical Interest", student_med)
    test_persona("THE UNQUALIFIED DREAMER", "Wants Engineering but FAILS Math Rule (<50%)", student_fail_math)
    
    print("\n" + "="*70)
    print(" PART 2: MINIMAL/SPARSE INPUT TESTS")
    print("="*70)
    
    results = []
    results.append(test_minimal_input(
        "GRADES ONLY", 
        "High Math/Physics but NO interests or career goals provided",
        minimal_grades_only,
        ["Engineering", "Data Science", "Cybersecurity", "Software"]  # Any STEM field
    ))
    
    results.append(test_minimal_input(
        "ONE-WORD INTEREST", 
        "Bio/Chem student with just 'health' as interest",
        minimal_vague_interest,
        ["Medicine", "Pharmacy", "Dentistry"]  # Any health field
    ))
    
    results.append(test_minimal_input(
        "CAREER GOAL ONLY", 
        "Just says 'engineer' with no other details",
        minimal_career_only,
        ["Engineering", "Architecture"]  # Any engineering-related
    ))
    
    results.append(test_minimal_input(
        "INFORMAL/TYPOS", 
        "Says 'i like making apps and stuff' informally",
        minimal_typos,
        ["Software", "Data"]  # Tech fields
    ))
    
    results.append(test_minimal_input(
        "BALANCED STUDENT", 
        "Average grades, just says 'business'",
        minimal_balanced,
        ["Business", "Finance", "Management"]  # Business fields
    ))
    
    results.append(test_minimal_input(
        "CONTRADICTION", 
        "Wants coding but has low Math/Physics (rule violation)",
        minimal_contradiction,
        ["Law", "International Relations", "Psychology"]  # Humanities fallback
    ))
    
    print("\n" + "="*70)
    print(" PART 3: FRONTEND ENDPOINT TEST")
    print("="*70)
    test_analyze_endpoint()
    
    # Summary
    passed = sum(results)
    total = len(results)
    print("\n" + "="*70)
    print(f" MINIMAL INPUT TESTS: {passed}/{total} PASSED")
    if passed == total:
        print(" 🎉 ALL TESTS PASSED! System handles sparse input well.")
    else:
        print(" ⚠ Some tests may need review")
    print("="*70)
