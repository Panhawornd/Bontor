"""
Recommendation logic for majors, careers, and universities
"""
from typing import List, Dict, Any, Tuple
import numpy as np
from .text_processing import (
    enhanced_preprocess_text, calculate_similarity, recognize_user_intent,
    context_aware_text_processing, zero_shot_major_scores, 
    enhanced_calculate_text_similarity, infer_preferences_from_text
)
from .constants import SCIENCE_SUBJECTS, LANG_SUBJECTS, SOCIAL_SUBJECTS, SUBJECT_MAX_SCORES, DOMAIN_KEYWORDS
from ..databases.majors import MAJOR_DATABASE
from ..databases.universities import UNIVERSITY_DATABASE

def analyze_subject_performance(grades: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """Analyze performance in each subject category"""
    subject_analysis = {
        "science": {"subjects": [], "average": 0, "strength": False},
        "language": {"subjects": [], "average": 0, "strength": False},
        "social": {"subjects": [], "average": 0, "strength": False}
    }
    
    for grade in grades:
        subject = grade["subject"]
        score = grade["score"]
        
        if subject in SCIENCE_SUBJECTS:
            subject_analysis["science"]["subjects"].append({"subject": subject, "score": score})
        elif subject in LANG_SUBJECTS:
            subject_analysis["language"]["subjects"].append({"subject": subject, "score": score})
        elif subject in SOCIAL_SUBJECTS:
            subject_analysis["social"]["subjects"].append({"subject": subject, "score": score})
    
    # Calculate averages and determine strengths
    for category in subject_analysis:
        subjects = subject_analysis[category]["subjects"]
        if subjects:
            avg_score = sum(s["score"] for s in subjects) / len(subjects)
            subject_analysis[category]["average"] = avg_score
            subject_analysis[category]["strength"] = avg_score >= 75  # 75% threshold
    
    return subject_analysis

def calculate_subject_match_score(subject_scores: Dict[str, float], required_subjects: List[str]) -> float:
    """Calculate how well student's subjects match major requirements"""
    if not required_subjects:
        return 0.5  # Neutral score if no requirements specified
    
    total_score = 0.0
    for subject in required_subjects:
        if subject in subject_scores:
            total_score += subject_scores[subject]
    
    return total_score / len(required_subjects)

def calculate_personalization_score(major_name: str, user_preferences: Dict[str, str] = None) -> float:
    """Calculate personalization score based on user preferences"""
    if not user_preferences:
        return 0.5  # Neutral score if no preferences
    
    score = 0.5  # Base score
    major_lower = major_name.lower()
    
    # Work style preferences
    work_style = user_preferences.get("workStyle", "")
    if work_style == "teamwork" and any(term in major_lower for term in ["business", "education", "psychology", "international"]):
        score += 0.1
    elif work_style == "solo" and any(term in major_lower for term in ["computer", "data", "engineering"]):
        score += 0.1
    
    # Learning style preferences
    learning_style = user_preferences.get("learningStyle", "")
    if learning_style == "practical" and any(term in major_lower for term in ["engineering", "computer", "business"]):
        score += 0.1
    elif learning_style == "theory" and any(term in major_lower for term in ["psychology", "mathematics", "physics"]):
        score += 0.1
    
    # Career focus preferences
    career_focus = user_preferences.get("careerFocus", "")
    if career_focus == "research" and any(term in major_lower for term in ["psychology", "physics", "chemistry", "biology"]):
        score += 0.1
    elif career_focus == "industry" and any(term in major_lower for term in ["computer", "engineering", "business", "data"]):
        score += 0.1
    elif career_focus == "entrepreneurship" and any(term in major_lower for term in ["business", "computer", "data"]):
        score += 0.1
    
    return min(1.0, score)

def intelligent_major_recommendations(subject_scores: Dict[str, float], interests: str, career_goals: str = "", user_preferences: Dict[str, str] = None, original_interests: str = None) -> List[Dict[str, Any]]:
    """Generate intelligent major recommendations using weighted scoring formula (with zero-shot + description alignment)."""
    # Weights
    ALPHA = 0.35  # skills (subjects)
    BETA = 0.35   # preferences (keywords + personalization)
    GAMMA = 0.10  # career goals alignment
    DELTA = 0.20  # description alignment (semantic)

    recommendations: List[Dict[str, Any]] = []

    interests_text = interests or ""
    goals_text = career_goals or ""
    original_interests_text = original_interests or interests_text
    combined_user_text = f"{interests_text} {goals_text}".strip()
    original_combined_text = f"{original_interests_text} {goals_text}".strip()

    # Zero-shot mapping from free text to majors
    zs_scores = zero_shot_major_scores(combined_user_text) if combined_user_text else {}
    
    # Smart domain detection with guardrails
    from .text_processing import detect_primary_domain, get_domain_guardrails
    domain_info = detect_primary_domain(combined_user_text)
    primary_domain = domain_info.get("domain")
    domain_confidence = domain_info.get("confidence", 0.0)
    guardrails = get_domain_guardrails(primary_domain) if primary_domain else {}
    
    # Special handling for ambiguous "design" input
    is_ambiguous_design = (
        len(combined_user_text.strip().split()) <= 5 and  # Very short text
        "design" in combined_user_text.lower() and
        not any(specific in combined_user_text.lower() for specific in ["graphic", "ux", "ui", "logo", "branding", "photoshop", "figma", "building", "architecture", "infrastructure", "software", "web", "app", "code"])
    )
    
    if is_ambiguous_design:
        print("DETECTED AMBIGUOUS 'design' - will boost all design-related majors")
        primary_domain = None  # Disable domain filtering for ambiguous case
        domain_confidence = 0.0
    
    print(f"Detected domain: {primary_domain} (confidence: {domain_confidence:.2f})")
    if primary_domain:
        print(f"Applying guardrails: boost {guardrails.get('boost_majors', [])}, demote {guardrails.get('demote_majors', [])}")

    # Additional business-specific filtering
    if primary_domain == "business" or any(keyword in combined_user_text.lower() for keyword in ["business", "finance", "management", "commerce", "entrepreneur"]):
        print("Applying business-specific filtering to remove unrelated majors")

    for major_name, major_data in MAJOR_DATABASE.items():
        # DEBUG: Print every major being evaluated
        if major_name in ["Graphic Design", "UX/UI Design"]:
            print(f"DEBUG: ===== Evaluating major '{major_name}' =====")
        
        # Skills
        skill_score = calculate_subject_match_score(subject_scores, major_data["required_subjects"])

        # Preferences
        text_similarity = enhanced_calculate_text_similarity(interests_text, major_data["keywords"])
        personalization_score = calculate_personalization_score(major_name, user_preferences)
        zs_score = zs_scores.get(major_name, 0.0)
        preference_score = (text_similarity * 0.6) + (personalization_score * 0.2) + (zs_score * 0.2)

        # Goals
        goal_score = enhanced_calculate_text_similarity(goals_text, major_data["career_paths"]) if goals_text else 0.0

        # Description alignment
        desc = f"{major_name}. {major_data.get('description', '')}"
        desc_alignment = enhanced_calculate_text_similarity(combined_user_text, [desc]) if combined_user_text else 0.0

        # Strict relevance gate - only recommend if there's actual interest/relevance
        try:
            interests_clean = enhanced_preprocess_text(interests_text.lower()) if interests_text else ""
            exact_keyword_hit = any(kw.lower() in interests_clean for kw in major_data["keywords"])
        except Exception:
            exact_keyword_hit = False

        # STRICTER GATE: Require meaningful interest alignment, not just good grades
        # High skill scores alone shouldn't pass the gate
        # BUT: Be more lenient for very short inputs (< 5 words)
        is_very_short = len(interests_text.split()) < 5 if interests_text else True
        
        if is_very_short:
            # Lower thresholds for very short inputs
            has_interest_signal = (
                exact_keyword_hit or 
                text_similarity >= 0.20 or
                zs_score >= 0.30 or
                desc_alignment >= 0.20
            )
        else:
            # Higher thresholds for longer, more detailed inputs
            has_interest_signal = (
                exact_keyword_hit or 
                text_similarity >= 0.25 or
                zs_score >= 0.4 or
                desc_alignment >= 0.25
            )
        
        # Only allow high skill score bypass if there's SOME interest signal
        skill_bypass = skill_score >= 0.85 and (text_similarity >= 0.10 or zs_score >= 0.15)
        
        passes_gate = has_interest_signal or skill_bypass
        
        # SPECIAL GATE OVERRIDE for design majors - force pass if SPECIFIC design keywords detected
        # More strict criteria: only force pass if there are SPECIFIC tools or explicit mentions
        is_graphic_design_interest = any(keyword in combined_user_text.lower() for keyword in ["graphic design", "visual design", "logo", "branding", "photoshop", "illustrator", "indesign", "typography", "poster", "graphic designer"])
        is_uxui_design_interest = any(keyword in combined_user_text.lower() for keyword in ["ux design", "ui design", "user experience design", "user interface design", "wireframe", "prototype", "figma", "adobe xd", "sketch app", "ux designer", "ui designer"])
        
        # Only force pass for design majors if there's a STRONG signal (not just "design")
        # BUT: Actively reject design majors if user clearly wants something else
        is_clearly_non_digital_design = any(keyword in combined_user_text.lower() for keyword in [
            "circuit", "electronic", "electrical", "machine", "mechanical", "engine", 
            "software", "coding", "programming", "algorithm", "database",
            "bridge", "road", "infrastructure", "construction", "structural",
            "medicine", "doctor", "patient", "hospital", "clinic",
            "business", "management", "entrepreneur", "finance", "investment",
            "building", "buildings", "architect", "architecture", "architectural"  # Architecture-related
        ])
        
        if major_name == "Graphic Design":
            if is_graphic_design_interest:
                passes_gate = True
                print(f"DEBUG: FORCED GATE PASS for Graphic Design (detected specific graphic design keywords)")
            elif is_clearly_non_digital_design and not is_ambiguous_design:
                passes_gate = False
                print(f"DEBUG: REJECTED Graphic Design (user wants something else)")
        
        if major_name == "UX/UI Design":
            if is_uxui_design_interest:
                passes_gate = True
                print(f"DEBUG: FORCED GATE PASS for UX/UI Design (detected specific UX/UI keywords)")
            elif is_clearly_non_digital_design and not is_ambiguous_design:
                passes_gate = False
                print(f"DEBUG: REJECTED UX/UI Design (user wants something else)")
        
        # Business-specific filtering: Remove unrelated majors for business users
        # Only apply this filtering if the user explicitly mentions business keywords AND is not in an engineering domain
        is_business_interest = (
            primary_domain == "business" or 
            any(keyword in combined_user_text.lower() for keyword in ["business", "finance", "management", "commerce", "entrepreneur"])
        )
        is_engineering_interest = primary_domain in ["mechanical_engineering", "electrical_engineering", "civil_engineering", "chemical_engineering"]
        
        if is_business_interest and not is_engineering_interest:
            # Skip engineering majors for business users (but not for engineering users)
            if any(eng_keyword in major_name.lower() for eng_keyword in ["engineering", "civil", "mechanical", "electrical", "chemical"]):
                continue
            # Skip health majors for business users
            if any(health_keyword in major_name.lower() for health_keyword in ["medicine", "health", "dental", "nursing"]):
                continue
            # Skip arts majors for business users unless explicitly mentioned
            if any(arts_keyword in major_name.lower() for arts_keyword in ["arts", "fine arts", "architecture"]) and not any(arts_mention in combined_user_text.lower() for arts_mention in ["art", "design", "creative", "architecture"]):
                continue

        # Domain guardrail adjustments with mixed interest awareness
        domain_boost = 1.0
        domain_penalty = 1.0
        
        # Check if user has mixed interests (multiple domains mentioned)
        from .text_processing import detect_primary_domain
        all_domain_info = detect_primary_domain(combined_user_text)
        all_domain_scores = all_domain_info.get("all_scores", {})
        has_mixed_interests = len([score for score in all_domain_scores.values() if score >= 2]) > 1
        
        # Check if this major matches one of the secondary domains
        major_matches_secondary_domain = False
        for domain, score in all_domain_scores.items():
            if score >= 2 and domain != primary_domain:
                secondary_guardrails = get_domain_guardrails(domain)
                if major_name in secondary_guardrails.get("boost_majors", []):
                    major_matches_secondary_domain = True
                    break
        
        if primary_domain and domain_confidence > 0.3:  # Only apply if confident
            # Boost majors that match the detected domain
            if major_name in guardrails.get("boost_majors", []):
                domain_boost = 1.5  # 50% boost
                print(f"Boosting {major_name} for domain {primary_domain}")
            
            # Demote majors that don't match the detected domain
            # BUT: If user has mixed interests and major matches secondary domain, don't demote
            elif major_name in guardrails.get("demote_majors", []):
                if has_mixed_interests and major_matches_secondary_domain:
                    # Don't demote if major matches a secondary domain
                    print(f"NOT demoting {major_name} for domain {primary_domain} (matches secondary interest)")
                elif has_mixed_interests:
                    domain_penalty = 0.7  # Only 30% penalty for mixed interests
                    print(f"Soft demoting {major_name} for domain {primary_domain} (mixed interests)")
                else:
                    domain_penalty = 0.3  # 70% penalty for single-domain users
                    print(f"Demoting {major_name} for domain {primary_domain}")

        # Final score with domain adjustments
        base_score = (
            ALPHA * skill_score +
            BETA * preference_score +
            GAMMA * goal_score +
            DELTA * desc_alignment
        )
        
        final_score = base_score * domain_boost * domain_penalty
        
        # SMART BOOSTS for specific majors based on interests (not forced overrides)
        # Only boost if already has reasonable base score
        
        # Ambiguous "design" boost - boost all design-related majors
        if is_ambiguous_design and major_name in ["UX/UI Design", "Graphic Design", "Architecture"]:
            final_score = min(1.0, final_score * 1.4)  # 40% boost for ambiguous design
            print(f"DEBUG: BOOSTED {major_name} for ambiguous design: {final_score}")
        
        # Pharmacy boost for drug/medicine interests
        if major_name == "Pharmacy" and base_score > 0.3 and any(keyword in combined_user_text.lower() for keyword in ["pharmacy", "pharmacist", "pharmaceutical", "medication", "new drugs", "drug development"]):
            final_score = min(1.0, final_score * 1.2)  # 20% boost
            print(f"DEBUG: BOOSTED Pharmacy: {final_score}")
        
        # Business Management boost for management interests
        if major_name == "Business Management" and base_score > 0.3 and any(keyword in combined_user_text.lower() for keyword in ["business management", "team management", "managing teams", "lead teams", "leadership"]):
            final_score = min(1.0, final_score * 1.2)  # 20% boost
            print(f"DEBUG: BOOSTED Business Management: {final_score}")
        
        # Finance boost for financial interests
        if major_name == "Finance" and base_score > 0.3 and any(keyword in combined_user_text.lower() for keyword in ["finance", "financial", "investment", "banking", "financial analysis", "financial planning"]):
            final_score = min(1.0, final_score * 1.2)  # 20% boost
            print(f"DEBUG: BOOSTED Finance: {final_score}")
        
        # UX/UI Design boost for interface/UX design interests (SPECIFIC keywords only)
        if major_name == "UX/UI Design" and base_score > 0.3 and any(keyword in combined_user_text.lower() for keyword in ["ux design", "ui design", "user experience", "user interface", "wireframe", "prototype", "figma", "adobe xd", "sketch app", "ux designer", "ui designer"]):
            final_score = min(1.0, final_score * 1.3)  # 30% boost (stronger for specific tools)
            print(f"DEBUG: BOOSTED UX/UI Design: {final_score}")
        
        # Graphic Design boost for visual/graphic design interests (SPECIFIC keywords only)
        if major_name == "Graphic Design" and base_score > 0.3 and any(keyword in combined_user_text.lower() for keyword in ["graphic design", "visual design", "logo design", "branding design", "photoshop", "illustrator", "indesign", "typography", "poster design", "graphic designer"]):
            final_score = min(1.0, final_score * 1.3)  # 30% boost (stronger for specific tools)
            print(f"DEBUG: BOOSTED Graphic Design: {final_score}")
        
        # Debug output for engineering majors
        if "Engineering" in major_name:
            pass  # Debug output removed for production

        # Domain disambiguation (Medicine vs Dentistry)
        try:
            text_all = combined_user_text.lower()
            dentistry_terms = ["dentist", "dentistry", "dental", "teeth", "tooth", "oral", "orthodont", "gingiva", "cavity", "enamel"]
            medicine_terms = ["doctor", "medicine", "medical", "hospital", "clinic", "surgery", "physician", "patient", "anatomy", "pharmacology"]
            mentions_dentistry = any(t in text_all for t in dentistry_terms)
            mentions_medicine = any(t in text_all for t in medicine_terms)
            if mentions_dentistry and "Medicine" in major_name and "Dentistry" not in major_name:
                if skill_score < 0.85 and text_similarity < 0.4:
                    passes_gate = False
                else:
                    final_score -= 0.15
            if mentions_medicine and "Dentistry" in major_name and "Medicine" not in major_name:
                if skill_score < 0.85 and text_similarity < 0.4:
                    passes_gate = False
                else:
                    final_score -= 0.15
        except Exception:
            pass

        # Aggressive filtering for mechanical engineering inputs
        print(f"DEBUG: Checking major {major_name} against original text: '{original_combined_text.lower()}'")
        if ("building machine" in original_combined_text.lower() or "building machines" in original_combined_text.lower() or "constructing machine" in original_combined_text.lower()):
            print(f"BUILDING MACHINE DETECTED: Filtering major {major_name}")
            # Only allow Engineering major for building machine inputs
            if not any(eng_type in major_name for eng_type in ["Electrical Engineering", "Mechanical Engineering", "Civil Engineering", "Chemical Engineering"]):
                print(f"REJECTING non-Engineering major: {major_name}")
                passes_gate = False

        # STRICTER THRESHOLD: Only recommend if score is meaningful
        # This ensures we only show truly relevant majors, not just "passable" ones
        # BUT: Lower threshold if we have strong domain detection and keyword matches
        has_strong_domain = primary_domain and domain_confidence > 0.4
        has_exact_keywords = exact_keyword_hit
        
        if has_strong_domain and has_exact_keywords:
            min_score_threshold = 0.25  # Lower threshold for strong matches
        else:
            min_score_threshold = 0.30  # Standard threshold
        
        if passes_gate and final_score >= min_score_threshold:
            # Cap the score at 1.0 (100%) to prevent >100% display
            print(f"DEBUG: {major_name} - final_score: {final_score:.3f}")
            capped_score = min(1.0, final_score)
            # Major added to recommendations
            recommendations.append({
                "name": major_name,
                "score": capped_score,
                "raw_score": final_score,  # Keep raw score for sorting
                "description": major_data["description"],
                "career_paths": major_data["career_paths"],
                "breakdown": {
                    "skill_score": round(float(skill_score), 3),
                    "preference_score": round(float(preference_score), 3),
                    "goal_score": round(float(goal_score), 3),
                    "desc_alignment": round(float(desc_alignment), 3),
                    "weights": {"α": ALPHA, "β": BETA, "γ": GAMMA, "δ": DELTA}
                }
            })
        elif passes_gate and final_score < min_score_threshold:
            print(f"DEBUG: {major_name} FILTERED OUT - score too low ({final_score:.3f} < {min_score_threshold})")

    recommendations.sort(key=lambda x: x["raw_score"], reverse=True)
    return recommendations[:5]

def intelligent_career_recommendations(major_recommendations: List[Dict[str, Any]], interests: str, original_interests: str = None) -> List[Dict[str, Any]]:
    """Generate career recommendations based on major recommendations and interests with enhanced text understanding."""
    # Process interests with enhanced text understanding
    context_info = context_aware_text_processing(interests)
    enhanced_interests = context_info['processed_text']
    intent = context_info['intent']
    
    careers: List[Dict[str, Any]] = []
    career_scores = {}

    # Smart domain detection for careers
    from .text_processing import detect_primary_domain, get_domain_guardrails
    domain_info = detect_primary_domain(interests)
    primary_domain = domain_info.get("domain")
    domain_confidence = domain_info.get("confidence", 0.0)
    guardrails = get_domain_guardrails(primary_domain) if primary_domain else {}
    
    print(f"Career domain detection: {primary_domain} (confidence: {domain_confidence:.2f})")
    
    # Legacy domain detection for backward compatibility
    interests_l = (interests or "").lower()
    target_domains = {k for k, kws in DOMAIN_KEYWORDS.items() if any(w in interests_l for w in kws)}
    
    print(f"Target domains: {target_domains}")
    print(f"DEBUG: Interest text: '{interests}'")
    print(f"DEBUG: Interest text lower: '{interests_l}'")
    
    # Prioritize careers from top recommended majors
    for i, major in enumerate(major_recommendations):
        major_weight = 1.0 - (i * 0.1)  # Higher weight for top majors (1.0, 0.9, 0.8, etc.)
        
        for career in major["career_paths"]:
            career_title = career.get("title", career) if isinstance(career, dict) else career
            if career_title not in career_scores:
                # Create comprehensive career keywords for better matching
                career_keywords = [
                    career_title.lower(),
                    career_title.lower().replace(" ", ""),
                    career_title.lower().replace(" ", "_"),
                    career_title.lower().replace(" ", "-")
                ]
                
                # Add related terms for electrical/mechanical careers FIRST (most specific)
                if "electrical" in career_title.lower() or "electronics" in career_title.lower():
                    career_keywords.extend(["electrical", "electronics", "circuit", "power", "signal", "embedded"])
                elif "mechanical" in career_title.lower():
                    career_keywords.extend(["mechanical", "machine", "mechanic", "manufacturing", "industrial"])
                elif "civil" in career_title.lower():
                    career_keywords.extend(["civil", "infrastructure", "construction", "structural"])
                # Add related terms for software careers
                elif "software" in career_title.lower() or "developer" in career_title.lower():
                    career_keywords.extend(["software", "programming", "coding", "developer", "programmer"])
                elif "data" in career_title.lower():
                    career_keywords.extend(["data", "analytics", "statistics", "analysis"])
                elif "ai" in career_title.lower() or "artificial" in career_title.lower():
                    career_keywords.extend(["ai", "artificial intelligence", "machine learning", "ml"])
                elif "cyber" in career_title.lower() or "security" in career_title.lower():
                    career_keywords.extend(["cybersecurity", "security", "hacking", "protection"])
                
                text_similarity = enhanced_calculate_text_similarity(enhanced_interests, career_keywords)

                # Domain boost if interests explicitly mention domain matching the career title
                domain_boost = 1.0
                c_low = career_title.lower()
                print(f"DEBUG: Career '{career}' (lower: '{c_low}') - Target domains: {target_domains}")
                if target_domains:
                    if ("electrical" in c_low and "electrical_engineering" in target_domains) or ("electronics" in c_low and "electrical_engineering" in target_domains):
                        domain_boost = 1.5  # Stronger boost for electrical
                    elif "mechanical" in c_low and "mechanical_engineering" in target_domains:
                        domain_boost = 1.4
                    elif "civil" in c_low and "civil_engineering" in target_domains:
                        domain_boost = 1.3
                    elif "chemical" in c_low and "chemical_engineering" in target_domains:
                        domain_boost = 1.3
                    elif ("software" in c_low and "software_engineering" in target_domains):
                        domain_boost = 1.5  # Increased boost for software
                        print(f"DEBUG: Boosting {career} for software_engineering domain")
                    elif ("data" in c_low and "data_science" in target_domains) or ("scientist" in c_low and "data_science" in target_domains):
                        domain_boost = 1.2
                    elif ("ai" in c_low and "data_science" in target_domains) or ("machine learning" in c_low and "data_science" in target_domains):
                        domain_boost = 1.5  # Strong boost for AI/ML careers
                        print(f"DEBUG: Boosting {career} for data_science domain")
                    elif ("engineer" in c_low and "software_engineering" in target_domains) and ("software" in c_low or "ai" in c_low):
                        domain_boost = 1.5  # Strong boost for software/AI engineers
                        print(f"DEBUG: Boosting {career} for software_engineering domain")
                    # Enhanced matching for Software Engineer and AI Engineer
                    elif "software engineer" in c_low and ("software_engineering" in target_domains or "data_science" in target_domains):
                        domain_boost = 1.8  # Very strong boost for Software Engineer
                        print(f"DEBUG: Strong boost for Software Engineer")
                    elif "ai engineer" in c_low and ("data_science" in target_domains or "software_engineering" in target_domains):
                        domain_boost = 1.8  # Very strong boost for AI Engineer
                        print(f"DEBUG: Strong boost for AI Engineer")
                    elif ("doctor" in c_low and "medicine" in target_domains) or ("medical" in c_low and "medicine" in target_domains):
                        domain_boost = 1.2
                    elif ("psychologist" in c_low and "psychology" in target_domains) or ("psychology" in c_low and "psychology" in target_domains):
                        domain_boost = 1.2
                    elif ("architect" in c_low and "architecture" in target_domains) or ("architecture" in c_low and "architecture" in target_domains):
                        domain_boost = 1.2
                    elif ("business" in c_low and "business" in target_domains) or ("entrepreneur" in c_low and "business" in target_domains):
                        domain_boost = 1.15

                # Weighted score with domain boost
                base_score = (major.get("match_score", 0.5) * major_weight * 0.8) + (text_similarity * 0.2)
                
                # SPECIAL BOOST for Software Engineer and AI Engineer (ONLY for programming/ML interests)
                # Check for explicit programming/tech keywords and exclude medical contexts
                is_programming_interest = (
                    "programming" in enhanced_interests.lower() or 
                    "software" in enhanced_interests.lower() or 
                    "coding" in enhanced_interests.lower() or 
                    "program" in enhanced_interests.lower() or 
                    "code" in enhanced_interests.lower() or
                    "computer" in enhanced_interests.lower() or
                    "tech" in enhanced_interests.lower() or
                    "artificial intelligence" in enhanced_interests.lower() or
                    "machine learning" in enhanced_interests.lower() or
                    "ai" in enhanced_interests.lower() or
                    "ml" in enhanced_interests.lower()
                )
                
                # Exclude medical contexts
                is_medical_context = (
                    "medical" in enhanced_interests.lower() or
                    "doctor" in enhanced_interests.lower() or
                    "patient" in enhanced_interests.lower() or
                    "hospital" in enhanced_interests.lower() or
                    "clinical" in enhanced_interests.lower() or
                    "microscope" in enhanced_interests.lower() or
                    "sample" in enhanced_interests.lower()
                )
                
                if "software engineer" in c_low and is_programming_interest and not is_medical_context:
                    base_score = 0.95  # Force very high score for Software Engineer
                    print(f"DEBUG: FORCED HIGH SCORE for Software Engineer: {base_score}")
                elif "ai engineer" in c_low and is_programming_interest and not is_medical_context:
                    base_score = 0.95  # Force very high score for AI Engineer
                    print(f"DEBUG: FORCED HIGH SCORE for AI Engineer: {base_score}")
                elif "machine learning engineer" in c_low and is_programming_interest and not is_medical_context:
                    base_score = 0.9  # Force high score for Machine Learning Engineer
                    print(f"DEBUG: FORCED HIGH SCORE for Machine Learning Engineer: {base_score}")
                # Block inappropriate tech careers for medical contexts
                elif is_medical_context and ("software engineer" in c_low or "ai engineer" in c_low or "machine learning engineer" in c_low):
                    base_score = 0.1  # Force low score for tech careers in medical contexts
                    print(f"DEBUG: BLOCKING TECH CAREER for medical context: {career_title}")
                
                # SPECIAL BOOST for Pharmacist (for drug/medicine interests)
                is_drug_interest = (
                    "medicine" in enhanced_interests.lower() or
                    "drug" in enhanced_interests.lower() or
                    "pharmaceutical" in enhanced_interests.lower() or
                    "pharmacy" in enhanced_interests.lower() or
                    "medication" in enhanced_interests.lower() or
                    "made and tested" in enhanced_interests.lower() or
                    "new drugs" in enhanced_interests.lower()
                )
                
                if "pharmacist" in c_low and is_drug_interest:
                    base_score = 0.8  # Force high score for Pharmacist
                    print(f"DEBUG: FORCED HIGH SCORE for Pharmacist: {base_score}")
                
                # SPECIAL BOOST for Medical Researcher (for medical research interests)
                is_medical_research_interest = (
                    "research" in enhanced_interests.lower() or
                    "testing" in enhanced_interests.lower() or
                    "examining" in enhanced_interests.lower() or
                    "microscope" in enhanced_interests.lower() or
                    "sample" in enhanced_interests.lower() or
                    "behind-the-scenes" in enhanced_interests.lower() or
                    "supporting doctors" in enhanced_interests.lower() or
                    "analytical tools" in enhanced_interests.lower()
                )
                
                if "medical researcher" in c_low and is_medical_research_interest:
                    base_score = 0.9  # Force high score for Medical Researcher
                    print(f"DEBUG: FORCED HIGH SCORE for Medical Researcher: {base_score}")
                
                # SPECIAL BOOST for Aerospace Engineer (for aerospace interests)
                is_aerospace_interest = (
                    "flight" in enhanced_interests.lower() or
                    "space" in enhanced_interests.lower() or
                    "aircraft" in enhanced_interests.lower() or
                    "rocket" in enhanced_interests.lower() or
                    "rockets" in enhanced_interests.lower() or
                    "aerospace" in enhanced_interests.lower() or
                    "aviation" in enhanced_interests.lower() or
                    "airplane" in enhanced_interests.lower() or
                    "helicopter" in enhanced_interests.lower() or
                    "satellite" in enhanced_interests.lower() or
                    "spacecraft" in enhanced_interests.lower() or
                    "engineering challenges" in enhanced_interests.lower()
                )
                
                if "aerospace engineer" in c_low and is_aerospace_interest:
                    base_score = 0.95  # Force very high score for Aerospace Engineer
                    print(f"DEBUG: FORCED HIGH SCORE for Aerospace Engineer: {base_score}")
                
                # SPECIAL BOOST for Diplomat (for international relations interests)
                is_international_interest = (
                    "international" in enhanced_interests.lower() or
                    "diplomacy" in enhanced_interests.lower() or
                    "politics" in enhanced_interests.lower() or
                    "global" in enhanced_interests.lower() or
                    "foreign" in enhanced_interests.lower() or
                    "policy" in enhanced_interests.lower() or
                    "government" in enhanced_interests.lower() or
                    "diplomat" in enhanced_interests.lower() or
                    "foreign service" in enhanced_interests.lower() or
                    "international development" in enhanced_interests.lower() or
                    "embassy" in enhanced_interests.lower() or
                    "consulate" in enhanced_interests.lower() or
                    "peacekeeping" in enhanced_interests.lower() or
                    "international trade" in enhanced_interests.lower() or
                    "international security" in enhanced_interests.lower() or
                    "international law" in enhanced_interests.lower() or
                    "global affairs" in enhanced_interests.lower() or
                    "foreign policy" in enhanced_interests.lower() or
                    "international organizations" in enhanced_interests.lower() or
                    "united nations" in enhanced_interests.lower() or
                    "ngo" in enhanced_interests.lower() or
                    "humanitarian" in enhanced_interests.lower()
                )
                
                if "diplomat" in c_low and is_international_interest:
                    base_score = 0.95  # Force very high score for Diplomat
                    print(f"DEBUG: FORCED HIGH SCORE for Diplomat: {base_score}")
                
                # SPECIAL BOOST for Business Manager (for business management interests)
                is_business_management_interest = (
                    "management" in enhanced_interests.lower() or
                    "leadership" in enhanced_interests.lower() or
                    "team management" in enhanced_interests.lower() or
                    "business management" in enhanced_interests.lower() or
                    "managing" in enhanced_interests.lower() or
                    "lead" in enhanced_interests.lower() or
                    "supervise" in enhanced_interests.lower() or
                    "organizational management" in enhanced_interests.lower() or
                    "business leadership" in enhanced_interests.lower() or
                    "management skills" in enhanced_interests.lower() or
                    "corporate management" in enhanced_interests.lower() or
                    "strategic management" in enhanced_interests.lower() or
                    "operations management" in enhanced_interests.lower() or
                    "project management" in enhanced_interests.lower()
                )
                
                if "business manager" in c_low and is_business_management_interest:
                    base_score = 0.95  # Force very high score for Business Manager
                    print(f"DEBUG: FORCED HIGH SCORE for Business Manager: {base_score}")
                
                # SPECIAL BOOST for Financial Analyst (for finance interests)
                is_finance_interest = (
                    "finance" in enhanced_interests.lower() or
                    "financial" in enhanced_interests.lower() or
                    "investment" in enhanced_interests.lower() or
                    "banking" in enhanced_interests.lower() or
                    "money" in enhanced_interests.lower() or
                    "financial analysis" in enhanced_interests.lower() or
                    "financial planning" in enhanced_interests.lower() or
                    "financial management" in enhanced_interests.lower() or
                    "financial services" in enhanced_interests.lower() or
                    "financial markets" in enhanced_interests.lower() or
                    "financial instruments" in enhanced_interests.lower() or
                    "financial modeling" in enhanced_interests.lower() or
                    "financial reporting" in enhanced_interests.lower() or
                    "financial accounting" in enhanced_interests.lower() or
                    "financial risk" in enhanced_interests.lower() or
                    "financial strategy" in enhanced_interests.lower() or
                    "financial consulting" in enhanced_interests.lower() or
                    "financial advisor" in enhanced_interests.lower() or
                    "corporate finance" in enhanced_interests.lower() or
                    "personal finance" in enhanced_interests.lower() or
                    "public finance" in enhanced_interests.lower() or
                    "international finance" in enhanced_interests.lower() or
                    "quantitative finance" in enhanced_interests.lower() or
                    "financial engineering" in enhanced_interests.lower()
                )
                
                if "financial analyst" in c_low and is_finance_interest:
                    base_score = 1.0  # Force maximum score for Financial Analyst
                    print(f"DEBUG: FORCED MAXIMUM SCORE for Financial Analyst: {base_score}")
                    # Skip ALL domain logic for Financial Analyst when finance interest is detected
                    career_domain_boost = 1.0  # No boost needed, already maximum
                    career_domain_penalty = 1.0  # No penalty for Financial Analyst
                    print(f"DEBUG: SKIPPING DOMAIN LOGIC for Financial Analyst")
                
                # Demote Entrepreneur and Business Consultant when finance interest is detected (Financial Analyst should be preferred)
                if "entrepreneur" in c_low and is_finance_interest:
                    base_score = 0.3  # Demote Entrepreneur for finance interests
                    print(f"DEBUG: DEMOTING Entrepreneur for finance interests: {base_score}")
                
                if "business consultant" in c_low and is_finance_interest:
                    base_score = 0.4  # Demote Business Consultant for finance interests
                    print(f"DEBUG: DEMOTING Business Consultant for finance interests: {base_score}")

                # Smart domain guardrails for careers
                career_domain_boost = 1.0
                career_domain_penalty = 1.0
                
                # Skip domain logic for Financial Analyst when finance interest is detected
                if not ("financial analyst" in c_low and is_finance_interest) and primary_domain and domain_confidence > 0.3:
                    # Boost careers that match the detected domain
                    if career in guardrails.get("boost_careers", []):
                        career_domain_boost = 1.8  # 80% boost for exact matches
                        print(f"Boosting career {career} for domain {primary_domain}")
                    
                    # Demote careers that don't match the detected domain
                    elif career in guardrails.get("demote_careers", []):
                        # Extra strong penalty for mechanical engineering domain
                        if primary_domain == "mechanical_engineering":
                            career_domain_penalty = 0.1  # 90% penalty for mechanical engineering mismatches
                    else:
                            career_domain_penalty = 0.2  # 80% penalty for other mismatches
                    print(f"Demoting career {career} for domain {primary_domain}")

                # Cross-domain penalty: if user intent has clear domains and this career doesn't match any, demote slightly
                cross_domain_penalty = 1.0
                if target_domains:
                    matches_any_domain = (
                        ("electrical" in c_low and "electrical" in target_domains) or
                        ("electronics" in c_low and "electrical" in target_domains) or
                        ("mechanical" in c_low and "mechanical" in target_domains) or
                        ("civil" in c_low and "civil" in target_domains) or
                        ("chemical" in c_low and "chemical" in target_domains) or
                        (("software" in c_low or "engineer" in c_low or "developer" in c_low) and "software" in target_domains) or
                        (("data" in c_low or "scientist" in c_low or "analyst" in c_low) and "data" in target_domains) or
                        (("doctor" in c_low or "medical" in c_low) and "medical" in target_domains) or
                        ("psycholog" in c_low and "psychology" in target_domains) or
                        (("architect" in c_low or "architecture" in c_low) and "architecture" in target_domains) or
                        (("business" in c_low or "entrepreneur" in c_low) and "business" in target_domains)
                    )
                    if not matches_any_domain:
                        cross_domain_penalty = 0.85

                # Civil vs Architecture separation: if interests imply civil, boost civil and slightly penalize architecture
                civil_arch_factor = 1.0
                if ("civil" in target_domains) and any(k in interests_l for k in ["bridge", "bridges", "infrastructure", "structural", "structure", "road", "roads"]):
                    if "civil" in c_low:
                        civil_arch_factor = 1.12
                    elif "architect" in c_low or "architecture" in c_low:
                        civil_arch_factor = 0.93

                career_scores[career_title] = base_score * domain_boost * cross_domain_penalty * civil_arch_factor * career_domain_boost * career_domain_penalty
            else:
                # If career appears in multiple majors, take the higher score
                career_keywords = [
                    career_title.lower(),
                    career_title.lower().replace(" ", ""),
                    career_title.lower().replace(" ", "_"),
                    career_title.lower().replace(" ", "-")
                ]
                
                # Add related terms for software careers
                if "software" in career_title.lower() or "engineer" in career_title.lower() or "developer" in career_title.lower():
                    career_keywords.extend(["software", "programming", "coding", "developer", "engineer", "programmer"])
                elif "data" in career_title.lower():
                    career_keywords.extend(["data", "analytics", "statistics", "analysis"])
                elif "ai" in career_title.lower() or "artificial" in career_title.lower():
                    career_keywords.extend(["ai", "artificial intelligence", "machine learning", "ml"])
                elif "cyber" in career_title.lower() or "security" in career_title.lower():
                    career_keywords.extend(["cybersecurity", "security", "hacking", "protection"])
                
                text_similarity = enhanced_calculate_text_similarity(enhanced_interests, career_keywords)
                domain_boost = 1.0
                c_low = career_title.lower()
                if target_domains:
                    if ("electrical" in c_low and "electrical" in target_domains) or ("electronics" in c_low and "electrical" in target_domains):
                        domain_boost = 1.25
                    elif "mechanical" in c_low and "mechanical" in target_domains:
                        domain_boost = 1.15
                    elif "civil" in c_low and "civil" in target_domains:
                        domain_boost = 1.1
                    elif "chemical" in c_low and "chemical" in target_domains:
                        domain_boost = 1.1
                # Cross-domain penalty (same as above branch)
                cross_domain_penalty = 1.0
                if target_domains:
                    matches_any_domain = (
                        ("electrical" in c_low and "electrical" in target_domains) or
                        ("electronics" in c_low and "electrical" in target_domains) or
                        ("mechanical" in c_low and "mechanical" in target_domains) or
                        ("civil" in c_low and "civil" in target_domains) or
                        ("chemical" in c_low and "chemical" in target_domains) or
                        (("software" in c_low or "engineer" in c_low or "developer" in c_low) and "software" in target_domains) or
                        (("data" in c_low or "scientist" in c_low or "analyst" in c_low) and "data" in target_domains) or
                        (("doctor" in c_low or "medical" in c_low) and "medical" in target_domains) or
                        ("psycholog" in c_low and "psychology" in target_domains) or
                        (("architect" in c_low or "architecture" in c_low) and "architecture" in target_domains) or
                        (("business" in c_low or "entrepreneur" in c_low) and "business" in target_domains)
                    )
                    if not matches_any_domain:
                        cross_domain_penalty = 0.85

                civil_arch_factor = 1.0
                if ("civil" in target_domains) and any(k in interests_l for k in ["bridge", "bridges", "infrastructure", "structural", "structure", "road", "roads"]):
                    if "civil" in c_low:
                        civil_arch_factor = 1.12
                    elif "architect" in c_low or "architecture" in c_low:
                        civil_arch_factor = 0.93

                new_score = ((major["score"] * major_weight * 0.8) + (text_similarity * 0.2)) * domain_boost * cross_domain_penalty * civil_arch_factor * career_domain_boost * career_domain_penalty
                career_scores[career] = max(career_scores[career], new_score)
    
    # Convert to list and sort
    for career, score in career_scores.items():
        if score > 0.1:
            # Aggressive filtering for mechanical engineering inputs
            original_interests_l = (original_interests or interests or "").lower()
            if ("building machine" in original_interests_l or "building machines" in original_interests_l or "constructing machine" in original_interests_l):
                c_low = career_title.lower()
                print(f"BUILDING MACHINE DETECTED: Checking career {career}")
                # Only allow mechanical engineering related careers
                if not any(k in c_low for k in ["mechanical", "robotics", "manufacturing", "industrial", "automation", "machine", "engineer"]):
                    print(f"REJECTING non-mechanical career: {career}")
                    continue  # Skip non-mechanical careers completely
            c_low = career_title.lower()
            group = "related"
            if target_domains:
                if ("electrical" in c_low and "electrical" in target_domains) or ("electronics" in c_low and "electrical" in target_domains):
                    group = "primary"
                elif "mechanical" in c_low and "mechanical" in target_domains:
                    group = "primary"
                elif ("building machine" in interests_l or "building machines" in interests_l) and "mechanical" in c_low:
                    group = "primary"  # Special case for building machine input
                elif "civil" in c_low and "civil" in target_domains:
                    group = "primary"
                elif "chemical" in c_low and "chemical" in target_domains:
                    group = "primary"
                elif ("software" in c_low and "software" in target_domains) or ("engineer" in c_low and "software" in target_domains):
                    group = "primary"
                elif ("data" in c_low and "data" in target_domains) or ("scientist" in c_low and "data" in target_domains):
                    group = "primary"
                elif ("doctor" in c_low and "medical" in target_domains) or ("medical" in c_low and "medical" in target_domains) or ("pharmacist" in c_low and "medical" in target_domains):
                    group = "primary"
                elif ("psychologist" in c_low and "psychology" in target_domains) or ("psychology" in c_low and "psychology" in target_domains):
                    group = "primary"
                elif ("architect" in c_low and "architecture" in target_domains) or ("architecture" in c_low and "architecture" in target_domains):
                    group = "primary"
                elif ("business" in c_low and "business" in target_domains) or ("entrepreneur" in c_low and "business" in target_domains):
                    group = "primary"
            
            # Apply stricter electrical gating to demote confusing cross-domain titles
            if "electrical" in target_domains:
                if not any(k in c_low for k in ["electrical", "electronics", "power", "embedded", "circuit", "signal"]):
                    # Demote non-electrical careers more aggressively
                    score *= 0.7

            # Clamp displayed score to 1.0 (100%) to avoid >100% after boosts
            display_score = min(1.0, float(score))
            careers.append({
                "title": career,
                "match_score": display_score,
                "raw_score": float(score),  # Keep raw score for sorting
                "description": f"Career in {career} based on your academic profile and interests",
                "group": group
            })
    
    # Sort primary careers first, then by raw score
    careers.sort(key=lambda x: (0 if x.get("group") == "primary" else 1, -x["raw_score"]))
    return careers[:6]

def intelligent_university_recommendations(subject_scores: Dict[str, float], major_recommendations: List[Dict[str, Any]], study_preference: str, career_goals: str = "") -> List[Dict[str, Any]]:
    """Generate university recommendations based on grades, majors, and study preference"""
    universities = []
    avg_grade = sum(subject_scores.values()) / len(subject_scores) if subject_scores else 0
    
    # Convert average grade to percentage for comparison
    avg_grade_percent = avg_grade * 100
    
    print(f"DEBUG University: Top major = {major_recommendations[0]['name'] if major_recommendations else 'None'}")
    
    # Derive career keywords to align universities with career goals
    career_keywords = []
    if career_goals:
        cg = enhanced_preprocess_text(career_goals.lower())
        # Simple keyword expansions for common careers
        if any(k in cg for k in ["software", "developer", "programmer", "engineer", "it", "computer"]):
            career_keywords += ["computer", "software", "technology", "information", "ai", "data", "cybersecurity", "network"]
        if any(k in cg for k in ["data", "analyst", "scientist", "ml", "ai", "machine"]):
            career_keywords += ["data", "analytics", "statistics", "machine", "ai"]
        if any(k in cg for k in ["doctor", "medical", "nurse", "health"]):
            career_keywords += ["medicine", "medical", "health", "clinical"]
        if any(k in cg for k in ["lawyer", "law", "legal", "judge", "prosecutor"]):
            career_keywords += ["law", "legal"]
        if any(k in cg for k in ["architect", "architecture", "design"]):
            career_keywords += ["architecture", "design"]
        if any(k in cg for k in ["electrical", "electronic", "electronics", "circuit", "power"]):
            career_keywords += ["electrical", "electronics", "power", "telecommunication"]
        if any(k in cg for k in ["mechanical", "machine", "mechanic"]):
            career_keywords += ["mechanical", "industrial", "manufacturing"]

    for uni_name, uni_data in UNIVERSITY_DATABASE.items():
        # Check if student meets minimum requirements (be more flexible)
        min_required = uni_data["requirements"]["min_grade"]
        if avg_grade_percent < (min_required - 10):  # Allow 10 points below minimum
            continue
        
        # All universities in database are Cambodian, so no filtering needed
        
        # Filter out unrelated universities for business users
        if major_recommendations and "Business" in major_recommendations[0]["name"]:
            # Skip health universities for business users
            if any(keyword in uni_name.lower() for keyword in ["health", "medical", "medicine"]):
             continue
            # Skip engineering-focused universities for business users unless they have business programs
            if any(keyword in uni_name.lower() for keyword in ["technology", "engineering", "polytechnic"]):
                # Only include if they have business programs
                if not any("business" in prog.lower() or "management" in prog.lower() or "commerce" in prog.lower() 
                          for prog in uni_data["programs"]):
                 continue
        
        # Find matching programs - focus only on TOP major for better relevance
        matching_programs = []
        if major_recommendations:
            # Only consider the top 1 major for more focused recommendations
            top_major = major_recommendations[0]
            major_name = top_major["name"]
            
            # Check for exact match or partial match with top major only
            for program in uni_data["programs"]:
                if (major_name.lower() in program.lower() or 
                    program.lower() in major_name.lower() or
                    major_name == program):
                    if program not in matching_programs:  # Avoid duplicates
                        matching_programs.append(program)
        
        # If no exact matches, include universities with related programs to TOP major only
        if not matching_programs and major_recommendations:
            top_major = major_recommendations[0]["name"]
            # Get keywords specific to the top major
            major_keywords = {
                "Computer Science": ["computer", "technology", "digital", "cybersecurity", "ai", "data", "software"],
                "Medicine": ["medical", "health", "medicine", "healthcare", "clinical"],
                "Electrical Engineering": ["electrical", "electronics", "electronic", "circuit", "power", "signal"],
                "Mechanical Engineering": ["mechanical", "machine", "robotics", "automation", "manufacturing"],
                "Civil Engineering": ["civil", "infrastructure", "construction", "structural", "bridge", "road"],
                "Chemical Engineering": ["chemical", "process", "manufacturing", "plant", "materials"],
                "Business Administration": ["business", "management", "commerce", "administration", "finance", "accounting", "marketing", "economics"],
                "Data Science": ["data", "analytics", "statistics", "machine learning"],
                "Psychology": ["psychology", "behavioral", "mental health", "counseling"],
                "Education": ["education", "teaching", "pedagogy", "learning"],
                "International Relations": ["international", "relations", "diplomacy", "policy"],
                "Architecture": ["architecture", "architectural", "urban planning", "landscape"],
                "Dentistry": ["dental", "dentistry", "oral", "orthodontics"],
                "Law": ["law", "legal", "jurisprudence", "legal system", "justice", "court", "legal practice"]
            }
            
            # Check for programs related to the top major
            relevant_keywords = major_keywords.get(top_major, [top_major.lower()])
            for program in uni_data["programs"]:
                if any(keyword in program.lower() for keyword in relevant_keywords):
                    matching_programs.append(program)
                    # Don't break - collect ALL matching programs for better scoring
        
        if matching_programs:
            # Calculate university score based on grade match and program availability
            grade_bonus = min(0.3, max(0, (avg_grade_percent - min_required) / 100))
            program_bonus = len(matching_programs) * 0.1
            
            # Give extra bonus for exact match with top recommended major
            top_major_bonus = 0.0
            if major_recommendations and matching_programs:
                top_major = major_recommendations[0]["name"]
                if any(top_major.lower() in prog.lower() or prog.lower() in top_major.lower() 
                       for prog in matching_programs):
                    top_major_bonus = 0.2  # Significant bonus for top major match
            
            # Career alignment bonus
            career_bonus = 0.0
            if career_keywords:
                # Boost if any career keyword appears in university name or matching programs
                if any(kw in uni_name.lower() for kw in career_keywords) or any(
                    any(kw in prog.lower() for kw in career_keywords) for prog in matching_programs
                ):
                    career_bonus = 0.2

            # Special bonus for CADT and IT-focused universities
            it_specialization_bonus = 0.0
            if "CADT" in uni_name:
                # CADT gets higher base score and bonus for IT programs
                base_score = 0.7  # Higher base score for CADT
                if any(keyword in uni_name.lower() or any(keyword in prog.lower() 
                      for prog in matching_programs) 
                      for keyword in ["computer", "technology", "digital", "cybersecurity", "ai", "data"]):
                    it_specialization_bonus = 0.3  # Extra bonus for IT specialization
            elif any(keyword in uni_name.lower() for keyword in ["technology", "digital", "computer"]):
                # Other IT-focused universities get bonus too
                base_score = 0.6
                it_specialization_bonus = 0.2
            else:
                base_score = 0.5  # Standard base score
            
            total_score = base_score + grade_bonus + program_bonus + top_major_bonus + it_specialization_bonus + career_bonus
            
            # Cap university score at 1.0 (100%) for display
            display_score = min(1.0, total_score)
            
            universities.append({
                "name": uni_name,
                "country": uni_data["country"],
                "programs": matching_programs,
                "score": display_score,
                "raw_score": total_score  # Keep raw score for sorting
            })
    
    # Sort and return ALL matching universities, prioritizing exact program matches first, then related
    universities.sort(key=lambda x: x["raw_score"], reverse=True)
    if major_recommendations:
        top_major = major_recommendations[0]["name"]
        exact_matches = [uni for uni in universities 
                         if any(top_major.lower() in prog.lower() or prog.lower() in top_major.lower() 
                                for prog in uni["programs"])]
        related_matches = [uni for uni in universities 
                           if not any(top_major.lower() in prog.lower() or prog.lower() in top_major.lower() 
                                      for prog in uni["programs"])]
        # Return all, exact first then related
        return exact_matches + related_matches
    return universities

def get_major_specific_skills(major: str, career: str) -> Dict[str, Dict[str, Any]]:
    """Get skills specific to a major"""
    
    # Computer Science & IT Skills
    if "Computer Science" in major or "Data Science" in major or "Software" in career or "Developer" in career:
        return {
            "Programming Logic": {"subjects": ["math"], "weight": 1.0, "required": 8.5},
            "Mathematical Analysis": {"subjects": ["math", "physics"], "weight": 0.9, "required": 8.0},
            "Problem Solving": {"subjects": ["math", "physics"], "weight": 0.8, "required": 8.5},
            "Technical Communication": {"subjects": ["english"], "weight": 0.7, "required": 7.5},
            "Data Analysis": {"subjects": ["math", "chemistry"], "weight": 0.8, "required": 8.0}
        }
    
    # Medicine & Health Sciences
    elif "Medicine" in major or "Health" in major or "Doctor" in career or "Medical" in career:
        return {
            "Biological Sciences": {"subjects": ["biology", "chemistry"], "weight": 1.0, "required": 9.0},
            "Chemical Analysis": {"subjects": ["chemistry"], "weight": 0.9, "required": 8.5},
            "Mathematical Precision": {"subjects": ["math"], "weight": 0.8, "required": 8.0},
            "Medical Communication": {"subjects": ["english"], "weight": 0.9, "required": 8.5},
            "Critical Analysis": {"subjects": ["biology", "chemistry"], "weight": 0.8, "required": 8.5},
            "Clinical Skills": {"subjects": ["biology", "chemistry"], "weight": 1.0, "required": 9.0},
            "Anatomy & Physiology": {"subjects": ["biology"], "weight": 0.9, "required": 8.8},
            "Patient Care": {"subjects": ["english", "biology"], "weight": 0.9, "required": 8.7},
            "Diagnostics & Imaging": {"subjects": ["physics", "biology"], "weight": 0.8, "required": 8.3},
            "Pharmacology": {"subjects": ["chemistry", "biology"], "weight": 0.85, "required": 8.6},
            "Bioethics & Professionalism": {"subjects": ["english", "history"], "weight": 0.8, "required": 8.5},
            "Teamwork & Collaboration": {"subjects": ["english"], "weight": 0.7, "required": 8.0},
            "Stress Management & Resilience": {"subjects": ["english"], "weight": 0.6, "required": 7.8},
            "Emergency Response": {"subjects": ["biology", "physics"], "weight": 0.8, "required": 8.4},
            "Infection Control & Safety": {"subjects": ["biology", "chemistry"], "weight": 0.85, "required": 8.6}
        }
    
    # Engineering (domain-specific)
    elif "Engineering" in major or "Engineer" in career:
        c_low = (career or "").lower()
        # Electrical / Electronics / Power specific skills
        if any(k in c_low for k in ["electrical", "electronics", "power", "embedded", "circuit", "signal"]):
            return {
                "Circuit Design": {"subjects": ["physics", "math"], "weight": 1.0, "required": 8.8},
                "Power Systems": {"subjects": ["physics", "math"], "weight": 0.95, "required": 8.7},
                "Electronics": {"subjects": ["physics"], "weight": 0.9, "required": 8.5},
                "Signals & Systems": {"subjects": ["physics", "math"], "weight": 0.9, "required": 8.5},
                "Embedded Systems": {"subjects": ["physics", "math"], "weight": 0.85, "required": 8.3},
                "Technical Writing": {"subjects": ["english"], "weight": 0.7, "required": 7.8}
            }
        # Civil specific skills
        if "civil" in c_low or any(k in (major or "") for k in ["Civil"]):
            return {
                "Structural Analysis": {"subjects": ["physics", "math"], "weight": 1.0, "required": 8.8},
                "Construction Materials": {"subjects": ["physics", "chemistry"], "weight": 0.85, "required": 8.0},
                "Geotechnical Basics": {"subjects": ["physics"], "weight": 0.8, "required": 7.8},
                "Project Planning": {"subjects": ["english", "math"], "weight": 0.75, "required": 7.8},
                "Design Thinking": {"subjects": ["math", "physics"], "weight": 0.8, "required": 8.0}
            }
        # Chemical specific skills
        if "chemical" in c_low or any(k in (major or "") for k in ["Chemical"]):
            return {
                "Chemical Processes": {"subjects": ["chemistry"], "weight": 1.0, "required": 8.7},
                "Thermodynamics": {"subjects": ["physics", "chemistry"], "weight": 0.9, "required": 8.5},
                "Process Control": {"subjects": ["math", "physics"], "weight": 0.85, "required": 8.2},
                "Safety & Compliance": {"subjects": ["english"], "weight": 0.7, "required": 7.8}
            }
        # Mechanical / generic engineering (exclude chemical by default)
        return {
            "Mathematical Modeling": {"subjects": ["math", "physics"], "weight": 1.0, "required": 9.0},
            "Physics Application": {"subjects": ["physics"], "weight": 0.9, "required": 8.5},
            "Design Thinking": {"subjects": ["math", "physics"], "weight": 0.8, "required": 8.0},
            "Technical Writing": {"subjects": ["english"], "weight": 0.8, "required": 8.0}
        }
    
    # Business & Management
    elif "Business" in major or "Management" in major or "Manager" in career or "Business" in career:
        return {
            "Quantitative Analysis": {"subjects": ["math"], "weight": 0.8, "required": 7.5},
            "Communication": {"subjects": ["english", "khmer"], "weight": 1.0, "required": 8.5},
            "Critical Thinking": {"subjects": ["math", "history"], "weight": 0.8, "required": 8.0},
            "Presentation Skills": {"subjects": ["english"], "weight": 0.9, "required": 8.0},
            "Cultural Awareness": {"subjects": ["history", "khmer"], "weight": 0.7, "required": 7.5}
        }
    
    # Education & Teaching
    elif "Education" in major or "Teacher" in career or "Teaching" in career:
        return {
            "Subject Mastery": {"subjects": ["math", "english", "history"], "weight": 0.9, "required": 8.5},
            "Communication": {"subjects": ["english", "khmer"], "weight": 1.0, "required": 9.0},
            "Cultural Knowledge": {"subjects": ["history", "khmer"], "weight": 0.8, "required": 8.0},
            "Presentation Skills": {"subjects": ["english"], "weight": 0.9, "required": 8.5},
            "Patience & Empathy": {"subjects": ["english", "khmer"], "weight": 0.6, "required": 8.0}
        }
    
    # Law & Legal Practice
    elif "Law" in major or "Lawyer" in career or "Legal" in career or "Judge" in career or "Prosecutor" in career:
        return {
            "Legal Analysis": {"subjects": ["history", "english"], "weight": 1.0, "required": 9.0},
            "Critical Reading": {"subjects": ["english", "history"], "weight": 1.0, "required": 9.0},
            "Communication": {"subjects": ["english", "khmer"], "weight": 1.0, "required": 9.0},
            "Research Skills": {"subjects": ["history", "english"], "weight": 0.9, "required": 8.5},
            "Ethical Reasoning": {"subjects": ["history", "english"], "weight": 0.9, "required": 8.5},
            "Logical Argumentation": {"subjects": ["math", "english"], "weight": 0.8, "required": 8.0}
        }
    
    # International Relations & Diplomacy
    elif "International" in major or "Diplomat" in career or "Policy" in career:
        return {
            "Cultural Understanding": {"subjects": ["history", "khmer"], "weight": 1.0, "required": 8.5},
            "Communication": {"subjects": ["english", "khmer"], "weight": 1.0, "required": 9.0},
            "Political Analysis": {"subjects": ["history", "english"], "weight": 0.9, "required": 8.5},
            "Research Skills": {"subjects": ["history", "english"], "weight": 0.8, "required": 8.0},
            "Language Proficiency": {"subjects": ["english", "khmer"], "weight": 0.9, "required": 8.5}
        }
    
    # Architecture
    elif "Architecture" in major or "Architect" in career:
        return {
            "Design Thinking": {"subjects": ["math", "physics"], "weight": 0.9, "required": 8.5},
            "Mathematical Modeling": {"subjects": ["math", "physics"], "weight": 1.0, "required": 8.5},
            "Visual Communication": {"subjects": ["english", "khmer"], "weight": 0.8, "required": 8.0},
            "Technical Drawing": {"subjects": ["math", "physics"], "weight": 0.9, "required": 8.5},
            "Cultural Understanding": {"subjects": ["history", "khmer"], "weight": 0.8, "required": 8.0},
            "Environmental Awareness": {"subjects": ["biology", "chemistry"], "weight": 0.7, "required": 7.5}
        }
    
    # Dentistry
    elif "Dentistry" in major or "Dentist" in career or "Dental" in career:
        return {
            "Biological Sciences": {"subjects": ["biology", "chemistry"], "weight": 1.0, "required": 9.0},
            "Chemical Analysis": {"subjects": ["chemistry"], "weight": 0.9, "required": 8.5},
            "Mathematical Precision": {"subjects": ["math"], "weight": 0.9, "required": 8.5},
            "Manual Dexterity": {"subjects": ["physics", "chemistry"], "weight": 0.8, "required": 8.5},
            "Patient Communication": {"subjects": ["english", "khmer"], "weight": 1.0, "required": 8.5},
            "Critical Analysis": {"subjects": ["biology", "chemistry"], "weight": 0.8, "required": 8.5}
        }
    
    # Arts & Design
    elif "Arts" in major or "Design" in major or "Artist" in career or "Designer" in career:
        return {
            "Creative Expression": {"subjects": ["english", "khmer"], "weight": 0.8, "required": 8.0},
            "Cultural Heritage": {"subjects": ["history", "khmer"], "weight": 0.9, "required": 8.5},
            "Communication": {"subjects": ["english", "khmer"], "weight": 0.8, "required": 8.0},
            "Visual Analysis": {"subjects": ["math", "physics"], "weight": 0.6, "required": 7.0},
            "Cultural Awareness": {"subjects": ["history", "khmer"], "weight": 0.8, "required": 8.0}
        }
    
    # Default general skills
    else:
        return {
            "Mathematics": {"subjects": ["math"], "weight": 1.0, "required": 7.0},
            "Science": {"subjects": ["physics", "chemistry", "biology"], "weight": 0.8, "required": 7.0},
            "Language": {"subjects": ["english", "khmer"], "weight": 0.6, "required": 7.0},
            "Critical Thinking": {"subjects": ["math", "physics", "history"], "weight": 0.7, "required": 7.0},
            "Communication": {"subjects": ["english", "khmer"], "weight": 0.5, "required": 7.0}
        }

def generate_skill_gaps(subject_scores: Dict[str, float], major_recommendations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Generate skill gap analysis based on major and career requirements"""
    skill_gaps = []
    
    # Get the top recommended major and career
    top_major = major_recommendations[0]["name"] if major_recommendations else "General"
    top_career = major_recommendations[0].get("career_paths", [""])[0] if major_recommendations else "General"
    
    # Define major-specific skill categories
    skill_categories = get_major_specific_skills(top_major, top_career)
    
    for skill_name, skill_data in skill_categories.items():
        # Calculate current skill level
        current_level = 0
        total_weight = 0
        for subject in skill_data["subjects"]:
            if subject in subject_scores:
                current_level += subject_scores[subject] * skill_data["weight"]
                total_weight += skill_data["weight"]
        
        if total_weight > 0:
            current_level = (current_level / total_weight) * 10  # Scale to 0-10
            required_level = skill_data["required"]  # Use major-specific requirement
            
            # Always show skill gaps for demonstration, but adjust required level if current is higher
            if current_level < required_level:
                skill_gaps.append({
                    "skill": skill_name,
                    "current_level": round(current_level, 1),
                    "required_level": round(required_level, 1),
                    "suggestions": generate_skill_suggestions(skill_name, current_level, required_level, top_major)
                })
            elif current_level >= required_level and current_level < 9.0:  # Show areas for further improvement
                skill_gaps.append({
                    "skill": f"{skill_name} (Advanced)",
                    "current_level": round(current_level, 1),
                    "required_level": 9.0,
                    "suggestions": generate_skill_suggestions(skill_name, current_level, 9.0, top_major)
                })
    
    return skill_gaps

def generate_skill_suggestions(skill_name: str, current_level: float, required_level: float, top_major: str | None = None) -> List[str]:
    """Generate specific suggestions for skill improvement based on major and career."""
    
    # Context-aware suggestions based on major
    if top_major and "Business" in top_major:
        business_suggestions = {
            "Quantitative Analysis": [
                "Learn Excel advanced functions and pivot tables",
                "Study business statistics and data analysis",
                "Practice financial calculations and modeling",
                "Learn business intelligence tools"
            ],
            "Communication": [
                "Join public speaking clubs (Toastmasters)",
                "Practice business writing and presentations",
                "Learn negotiation and persuasion techniques",
                "Study cross-cultural communication"
            ],
            "Critical Thinking": [
                "Practice analyzing business case studies",
                "Learn strategic thinking and planning",
                "Study decision-making frameworks",
                "Practice problem-solving in business contexts"
            ],
            "Presentation Skills": [
                "Practice creating compelling presentations",
                "Learn visual design and storytelling",
                "Practice speaking to different audiences",
                "Study presentation software and tools"
            ],
            "Cultural Awareness": [
                "Study different cultures and business practices",
                "Learn a foreign language",
                "Travel or study abroad if possible",
                "Join international business groups"
            ]
        }
        if skill_name in business_suggestions:
            return business_suggestions[skill_name]
    
    suggestions = {
        # Computer Science & IT Skills
        "Programming Logic": [
            "Practice coding problems on LeetCode, HackerRank, or CodeWars",
            "Learn a programming language (Python, Java, or JavaScript)",
            "Build small projects to apply programming concepts",
            "Study algorithms and data structures online"
        ],
        "Mathematical Analysis": [
            "Practice calculus and linear algebra problems",
            "Learn discrete mathematics for computer science",
            "Study statistics and probability for data analysis",
            "Take online courses in mathematical foundations"
        ],
        "Problem Solving": [
            "Solve algorithmic puzzles and brain teasers",
            "Practice breaking down complex problems into smaller parts",
            "Learn different problem-solving methodologies",
            "Join programming competitions or hackathons"
        ],
        "Technical Communication": [
            "Write technical documentation for your projects",
            "Practice explaining complex concepts simply",
            "Join tech communities and participate in discussions",
            "Learn to create clear presentations and diagrams"
        ],
        "Data Analysis": [
            "Learn Excel/Google Sheets advanced functions",
            "Study statistics and data visualization",
            "Practice with real datasets online",
            "Learn SQL for database management"
        ],
        
        # Medicine & Health Sciences
        "Biological Sciences": [
            "Study anatomy and physiology textbooks",
            "Conduct biology experiments at home",
            "Watch medical documentaries and educational videos",
            "Join biology study groups or online forums"
        ],
        "Clinical Skills": [
            "Practice basic clinical procedures under supervision",
            "Learn patient history taking and physical examination",
            "Observe clinical rounds and case discussions",
            "Use simulation labs to practice clinical scenarios"
        ],
        "Anatomy & Physiology": [
            "Study human anatomy with atlases and 3D models",
            "Use anatomy apps and virtual dissection tools",
            "Relate physiological systems to clinical cases",
            "Practice identifying structures on imaging"
        ],
        "Patient Care": [
            "Practice empathetic communication with patients",
            "Shadow healthcare providers in clinics/hospitals",
            "Learn bedside manners and patient education",
            "Practice informed consent and confidentiality"
        ],
        "Diagnostics & Imaging": [
            "Study common imaging modalities (X-ray, CT, MRI, Ultrasound)",
            "Learn to interpret basic radiological findings",
            "Relate lab results to possible diagnoses",
            "Practice differential diagnosis reasoning"
        ],
        "Pharmacology": [
            "Study drug classes, mechanisms, and side effects",
            "Learn dosage calculations and interactions",
            "Use drug reference resources (BNF, UpToDate)",
            "Practice case-based medication selection"
        ],
        "Bioethics & Professionalism": [
            "Study medical ethics principles (autonomy, beneficence, justice)",
            "Learn confidentiality and professional boundaries",
            "Discuss ethical dilemmas using case studies",
            "Understand healthcare laws and patient rights"
        ],
        "Teamwork & Collaboration": [
            "Participate in interprofessional simulations",
            "Practice clear handovers (SBAR technique)",
            "Learn roles of different healthcare team members",
            "Develop leadership in small clinical teams"
        ],
        "Stress Management & Resilience": [
            "Practice mindfulness and stress-reduction techniques",
            "Learn time management and prioritization",
            "Build support networks and reflective practice",
            "Use debriefing after challenging cases"
        ],
        "Emergency Response": [
            "Learn basic life support (BLS) and first aid",
            "Practice triage and emergency protocols",
            "Simulate acute care scenarios (shock, trauma)",
            "Study rapid assessment and stabilization"
        ],
        "Infection Control & Safety": [
            "Learn sterile techniques and PPE use",
            "Practice hand hygiene and isolation protocols",
            "Study hospital-acquired infections and prevention",
            "Understand waste disposal and safety procedures"
        ],
        "Chemical Analysis": [
            "Practice chemistry problem-solving daily",
            "Study organic and biochemistry concepts",
            "Conduct safe chemistry experiments at home",
            "Take advanced chemistry courses online"
        ],
        # Default Mathematical Precision (generic fallback)
        "Mathematical Precision": [
            "Practice medical calculations and dosages",
            "Study statistics for medical research",
            "Learn to work with precise measurements",
            "Practice mental math for quick calculations"
        ],
        "Medical Communication": [
            "Practice explaining medical concepts to patients",
            "Study medical terminology and vocabulary",
            "Join medical discussion groups",
            "Practice writing medical reports and case studies"
        ],
        "Critical Analysis": [
            "Study medical case studies and diagnoses",
            "Practice analyzing symptoms and test results",
            "Learn to think systematically about problems",
            "Study research methodology and evidence-based medicine"
        ],
        
        # Engineering
        "Mathematical Modeling": [
            "Practice calculus and differential equations",
            "Learn mathematical software (MATLAB, Mathematica)",
            "Study engineering mathematics textbooks",
            "Practice solving real-world engineering problems"
        ],
        "Physics Application": [
            "Study mechanics, thermodynamics, and electromagnetism",
            "Practice physics problem-solving with real scenarios",
            "Learn to apply physics principles to engineering design",
            "Take advanced physics courses online"
        ],
        "Chemical Processes": [
            "Study chemical engineering principles",
            "Learn about industrial chemical processes",
            "Practice material science and chemistry problems",
            "Study environmental chemistry and safety"
        ],
        "Technical Writing": [
            "Practice writing engineering reports and proposals",
            "Learn to create technical drawings and diagrams",
            "Study engineering documentation standards",
            "Practice presenting technical information clearly"
        ],
        "Design Thinking": [
            "Learn CAD software (AutoCAD, SolidWorks)",
            "Practice engineering design methodology",
            "Study product development processes",
            "Join engineering design competitions"
        ],
        
        # Business & Management
        "Quantitative Analysis": [
            "Learn Excel advanced functions and pivot tables",
            "Study business statistics and data analysis",
            "Practice financial calculations and modeling",
            "Learn business intelligence tools"
        ],
        "Communication": [
            "Join public speaking clubs (Toastmasters)",
            "Practice business writing and presentations",
            "Learn negotiation and persuasion techniques",
            "Study cross-cultural communication"
        ],
        "Critical Thinking": [
            "Practice analyzing business case studies",
            "Learn strategic thinking and planning",
            "Study decision-making frameworks",
            "Practice problem-solving in business contexts"
        ],
        "Presentation Skills": [
            "Practice creating compelling presentations",
            "Learn visual design and storytelling",
            "Practice speaking to different audiences",
            "Study presentation software and tools"
        ],
        "Cultural Awareness": [
            "Study different cultures and business practices",
            "Learn a foreign language",
            "Travel or study abroad if possible",
            "Join international business groups"
        ],
        
        # Education & Teaching
        "Subject Mastery": [
            "Deepen knowledge in your teaching subjects",
            "Study pedagogy and teaching methods",
            "Practice explaining concepts to different age groups",
            "Take advanced courses in your subject areas"
        ],
        "Communication": [
            "Practice public speaking and presentation",
            "Learn classroom management techniques",
            "Study effective communication with students",
            "Practice writing clear lesson plans"
        ],
        "Cultural Knowledge": [
            "Study Cambodian history and culture",
            "Learn about different learning styles",
            "Study inclusive education practices",
            "Learn about student psychology and development"
        ],
        "Presentation Skills": [
            "Practice teaching in front of small groups",
            "Learn to use educational technology",
            "Study visual aids and teaching materials",
            "Practice engaging different types of learners"
        ],
        "Patience & Empathy": [
            "Volunteer with children or students",
            "Study child psychology and development",
            "Practice active listening skills",
            "Learn conflict resolution techniques"
        ],
        
        # Law & Legal Practice
        "Legal Analysis": [
            "Study Cambodian law and legal system",
            "Practice analyzing legal cases and precedents",
            "Learn legal research and writing techniques",
            "Study constitutional law and civil rights",
            "Practice case law analysis and interpretation"
        ],
        "Critical Reading": [
            "Practice analyzing complex legal documents",
            "Study legal texts and court decisions",
            "Learn to identify legal precedents and implications",
            "Practice summarizing and synthesizing legal information",
            "Study legal terminology and concepts"
        ],
        "Communication": [
            "Practice formal legal writing and documentation",
            "Study courtroom communication and presentation",
            "Learn to write legal briefs and arguments",
            "Practice public speaking and debate",
            "Study client communication and consultation"
        ],
        "Research Skills": [
            "Learn legal and academic research methods",
            "Practice using legal databases and research tools",
            "Study citation and referencing standards for law",
            "Learn to evaluate legal source credibility",
            "Practice finding and analyzing legal precedents"
        ],
        "Ethical Reasoning": [
            "Study legal ethics and professional conduct",
            "Learn about lawyer-client privilege and confidentiality",
            "Study ethical dilemmas in legal practice",
            "Learn about professional responsibility and accountability",
            "Practice ethical decision-making in legal contexts"
        ],
        "Logical Argumentation": [
            "Study logical reasoning and argument construction",
            "Practice building legal arguments and defenses",
            "Learn about evidence evaluation and presentation",
            "Study logical fallacies and how to avoid them",
            "Practice structured legal reasoning and analysis"
        ],
        
        # International Relations & Diplomacy
        "Cultural Understanding": [
            "Study different countries and cultures",
            "Learn about international relations and diplomacy",
            "Study global politics and economics",
            "Learn about cultural sensitivity and awareness",
            "Study international law and treaties"
        ],
        "Political Analysis": [
            "Study global politics and international relations",
            "Learn about diplomatic protocols and procedures",
            "Study international organizations and their roles",
            "Learn about conflict resolution and negotiation",
            "Study foreign policy analysis and development"
        ],
        "Language Proficiency": [
            "Learn multiple languages for international work",
            "Study diplomatic communication and protocol",
            "Practice cross-cultural communication skills",
            "Learn about translation and interpretation",
            "Study international business communication"
        ],
        
        # Architecture
        "Design Thinking": [
            "Learn CAD software (AutoCAD, SketchUp, Revit)",
            "Study architectural design principles and history",
            "Practice sketching and conceptual design",
            "Study sustainable design and green architecture"
        ],
        "Mathematical Modeling": [
            "Practice structural calculations and load analysis",
            "Learn building physics and environmental systems",
            "Study geometry and spatial mathematics",
            "Practice 3D modeling and visualization"
        ],
        "Visual Communication": [
            "Learn architectural drawing and presentation techniques",
            "Practice creating architectural renderings",
            "Study graphic design and visual storytelling",
            "Learn to present design concepts clearly"
        ],
        "Technical Drawing": [
            "Master architectural drafting standards",
            "Learn to read and create construction drawings",
            "Study building codes and regulations",
            "Practice technical documentation and specifications"
        ],
        "Cultural Understanding": [
            "Study architectural history and styles",
            "Learn about cultural influences on design",
            "Study traditional building methods and materials",
            "Visit historical buildings and architectural sites"
        ],
        "Environmental Awareness": [
            "Study sustainable design principles",
            "Learn about environmental impact of buildings",
            "Study renewable energy and green technology",
            "Practice designing for climate and context"
        ],
        
        # Dentistry
        "Biological Sciences": [
            "Study anatomy and physiology, especially head and neck",
            "Learn about oral biology and dental anatomy",
            "Study microbiology and infection control",
            "Practice identifying oral diseases and conditions"
        ],
        "Chemical Analysis": [
            "Study dental materials science and chemistry",
            "Learn about dental pharmacology and medications",
            "Study oral biochemistry and saliva analysis",
            "Practice understanding chemical properties of dental materials"
        ],
        # Dentistry-specific Mathematical Precision (disambiguated via top_major)
        "Mathematical Precision|Dentistry": [
            "Practice dental measurements and calculations",
            "Study dental radiography and imaging mathematics",
            "Learn about dental occlusion and bite analysis",
            "Practice precise measurements for dental procedures"
        ],
        "Manual Dexterity": [
            "Practice fine motor skills with dental tools",
            "Learn dental handpiece and instrument techniques",
            "Practice dental procedures on models and simulators",
            "Study ergonomics and proper positioning"
        ],
        "Patient Communication": [
            "Practice explaining dental procedures to patients",
            "Learn dental terminology and patient education",
            "Study psychology of dental anxiety and fear",
            "Practice building rapport with different age groups"
        ],
        "Critical Analysis": [
            "Study dental case studies and treatment planning",
            "Practice diagnosing oral health problems",
            "Learn about evidence-based dentistry",
            "Study dental research and clinical studies"
        ],
        
        # Arts & Design
        "Creative Expression": [
            "Practice your chosen art form daily",
            "Study art history and different styles",
            "Experiment with different mediums and techniques",
            "Join art communities and workshops"
        ],
        "Cultural Heritage": [
            "Study Cambodian art and cultural traditions",
            "Learn about traditional crafts and techniques",
            "Study art history from different cultures",
            "Visit museums and cultural sites"
        ],
        "Communication": [
            "Learn to present your artwork effectively",
            "Study art criticism and analysis",
            "Practice writing artist statements",
            "Learn to communicate your creative vision"
        ],
        "Visual Analysis": [
            "Study color theory and composition",
            "Learn about design principles and elements",
            "Practice analyzing and critiquing artwork",
            "Study visual communication and design"
        ],
        "Cultural Awareness": [
            "Study art from different cultures and periods",
            "Learn about cultural significance of art",
            "Study contemporary art and global trends",
            "Learn about art's role in society"
        ],
        
        # Default general skills
        "Mathematics": [
            "Practice advanced algebra and calculus problems",
            "Take online math courses (Khan Academy, Coursera)",
            "Solve math problems daily for 30 minutes",
            "Join math study groups or tutoring"
        ],
        "Science": [
            "Conduct science experiments at home",
            "Read scientific articles and journals",
            "Watch educational science videos",
            "Take additional science courses online"
        ],
        "Language": [
            "Read books and articles in the target language",
            "Practice writing essays and reports",
            "Join language exchange programs",
            "Watch movies and TV shows with subtitles"
        ],
        "Critical Thinking": [
            "Practice logical reasoning puzzles",
            "Analyze case studies and real-world problems",
            "Debate topics with friends or online",
            "Take philosophy or logic courses"
        ],
        "Communication": [
            "Join public speaking clubs (Toastmasters)",
            "Practice presenting to small groups",
            "Write blogs or articles regularly",
            "Take communication skills workshops"
        ]
    }
    # Disambiguation for overlapping skill names by domain
    if skill_name == "Mathematical Precision" and top_major:
        if "Dentistry" in top_major:
            return suggestions.get("Mathematical Precision|Dentistry", suggestions["Mathematical Precision"]) 
        if "Medicine" in top_major or "Medical" in top_major:
            return suggestions["Mathematical Precision"]

    return suggestions.get(skill_name, ["Focus on improving this skill through practice and study"])

def hybrid_major_recommendations(subject_scores: Dict[str, float], interests: str, career_goals: str = "", user_preferences: Dict[str, str] = None, ml_models: Dict = None, domain_models: Dict = None) -> List[Dict[str, Any]]:
    """Hybrid recommendation system combining ML and rule-based approaches with enhanced text understanding"""
    
    print(f"HYBRID: Processing interests: '{interests}'")
    
    # Process user input with context awareness
    context_info = context_aware_text_processing(interests)
    enhanced_interests = context_info['processed_text']
    intent = context_info['intent']
    
    # Process career goals if provided
    if career_goals:
        career_context = context_aware_text_processing(career_goals)
        enhanced_career_goals = career_context['processed_text']
    else:
        enhanced_career_goals = ""
    
    # Try domain-specific model first, then general model
    from .text_processing import detect_primary_domain
    combined_user_text = f"{interests} {career_goals}".strip()
    detected_domain = detect_primary_domain(combined_user_text).get("domain", "general")
    
    # Try domain-specific model first
    if domain_models and detected_domain in domain_models:
        try:
            # Convert subject_scores to the format expected by prepare_ml_features
            grades = [{"subject": k, "score": v*100} for k, v in subject_scores.items()]
            ml_features = prepare_ml_features(grades, interests, career_goals, 'local')

            domain_model = domain_models[detected_domain]
            ml_probabilities = domain_model.predict_proba(ml_features)[0]
            ml_classes = domain_model.classes_
            top_idx = int(np.argmax(ml_probabilities))
            top_class = ml_classes[top_idx]
            top_conf = float(ml_probabilities[top_idx])

            ml_recommendations = []
            for class_name, prob in zip(ml_classes, ml_probabilities):
                if prob > max(0.05, top_conf * 0.25):
                    from ..databases.majors import MAJOR_DATABASE
                    major_data = MAJOR_DATABASE.get(class_name, {})
                    ml_recommendations.append({
                        "name": class_name,
                        "score": float(prob),
                        "description": major_data.get("description", ""),
                        "career_paths": major_data.get("career_paths", []),
                        "source": "ML",
                        "confidence": round(top_conf, 3)
                    })

            ml_recommendations.sort(key=lambda x: x["score"], reverse=True)
            
            # Always apply safety filters
            print(f"DEBUG: Applying safety filters to {len(ml_recommendations)} ML recommendations")
            
            # Enhanced safety filter: Remove unrelated majors based on detected domain
            try:
                text_lower = combined_user_text.lower()
                
                # Define domain-specific terms
                tech_terms = ["computer science", "programming", "coding", "software", " ai ", "machine learning", "app development", "backend", "frontend", " api ", "database", "cybersecurity", "app", "apps", "website", "websites", "web development", "mobile app"]
                engineering_terms = ["electrical engineering", "circuit", "power systems", "mechanical engineering", "manufacturing", "civil engineering", "infrastructure", "chemical engineering", "aerospace", "aircraft"]
                medical_terms = ["doctor", "medicine", "medical", "hospital", "physician", "surgery", "patient", "healthcare", "dentist", "dental"]
                business_terms = ["business", "management", "finance", "marketing", "entrepreneur", "corporate", "investment", "commerce"]
                arts_terms = ["graphic design", "visual design", "ux design", "ui design", "wireframe", "figma", "architecture", "architect", "building", "painting", "music"]
                law_terms = ["law", "legal", "lawyer", "justice", "court", "attorney"]
                education_terms = ["teaching", "teacher", "education", "classroom", "educator", "professor"]
                
                # Detect what domains the user is interested in
                mentions_tech = any(t in text_lower for t in tech_terms)
                mentions_engineering = any(t in text_lower for t in engineering_terms)
                mentions_medical = any(t in text_lower for t in medical_terms)
                mentions_business = any(t in text_lower for t in business_terms)
                mentions_arts = any(t in text_lower for t in arts_terms)
                mentions_law = any(t in text_lower for t in law_terms)
                mentions_education = any(t in text_lower for t in education_terms)
                
                print(f"DEBUG SAFETY: text='{text_lower}'")
                print(f"DEBUG SAFETY: mentions_tech={mentions_tech}, mentions_engineering={mentions_engineering}")
                
                # Filter out unrelated majors based on detected interests
                filtered_recommendations = []
                for rec in ml_recommendations:
                    major_name = rec["name"].lower()
                    should_include = True
                    
                    # Tech/Data Science interests - remove non-tech majors (but NOT for engineering interests!)
                    if mentions_tech and not mentions_engineering:
                        if any(unrelated in major_name for unrelated in ["medicine", "dentistry", "law", "psychology", "education", "international relations", "architecture", "civil engineering", "mechanical engineering", "electrical engineering", "chemical engineering"]):
                            should_include = False
                            print(f"SAFETY: Filtering {rec['name']} for tech interests")
                    
                    # Engineering interests - remove non-engineering majors
                    if mentions_engineering:
                        if any(unrelated in major_name for unrelated in ["medicine", "dentistry", "law", "psychology", "education", "international relations", "business administration", "data science", "computer science"]):
                            should_include = False
                            print(f"SAFETY: Filtering {rec['name']} for engineering interests")
                    
                    # Medical interests - remove non-medical majors
                    elif mentions_medical and not mentions_tech and not mentions_engineering and not mentions_business:
                        if any(unrelated in major_name for unrelated in ["computer science", "data science", "electrical engineering", "mechanical engineering", "civil engineering", "chemical engineering", "law", "psychology", "education", "international relations", "architecture", "business administration"]):
                            should_include = False
                            print(f"SAFETY: Filtering {rec['name']} for medical interests")
                    
                    # Business interests - remove non-business majors
                    elif mentions_business and not mentions_tech and not mentions_engineering and not mentions_medical and not mentions_arts:
                        if any(unrelated in major_name for unrelated in ["medicine", "dentistry", "electrical engineering", "mechanical engineering", "civil engineering", "chemical engineering", "law", "psychology", "education", "international relations", "architecture"]):
                            should_include = False
                            print(f"SAFETY: Filtering {rec['name']} for business interests")
                    
                    # Arts/Architecture interests - remove non-arts majors
                    elif mentions_arts and not mentions_tech and not mentions_engineering and not mentions_medical and not mentions_business:
                        if any(unrelated in major_name for unrelated in ["medicine", "dentistry", "electrical engineering", "mechanical engineering", "civil engineering", "chemical engineering", "law", "psychology", "education", "international relations", "business administration", "computer science", "data science"]):
                            should_include = False
                            print(f"SAFETY: Filtering {rec['name']} for arts interests")
                    
                    # Law interests - remove non-law majors
                    elif mentions_law and not mentions_tech and not mentions_engineering and not mentions_medical and not mentions_business and not mentions_arts:
                        if any(unrelated in major_name for unrelated in ["medicine", "dentistry", "electrical engineering", "mechanical engineering", "civil engineering", "chemical engineering", "psychology", "education", "international relations", "architecture", "business administration", "computer science", "data science"]):
                            should_include = False
                            print(f"SAFETY: Filtering {rec['name']} for law interests")
                    
                    # Education interests - remove non-education majors
                    elif mentions_education and not mentions_tech and not mentions_engineering and not mentions_medical and not mentions_business and not mentions_arts and not mentions_law:
                        if any(unrelated in major_name for unrelated in ["medicine", "dentistry", "electrical engineering", "mechanical engineering", "civil engineering", "chemical engineering", "law", "psychology", "international relations", "architecture", "business administration", "computer science", "data science"]):
                            should_include = False
                            print(f"SAFETY: Filtering {rec['name']} for education interests")
                    
                    if should_include:
                        filtered_recommendations.append(rec)
                    else:
                        print(f"SAFETY: Excluded {rec['name']} from recommendations")
                
                ml_recommendations = filtered_recommendations
                print(f"DEBUG: After safety filtering: {len(ml_recommendations)} recommendations remain")
                
                # If filtering removed all recommendations, fall back to rule-based
                if not ml_recommendations:
                    print(f"SAFETY: All ML recommendations filtered, falling back to rule-based")
                    return intelligent_major_recommendations(subject_scores, enhanced_interests, enhanced_career_goals, user_preferences, interests)
            except Exception as e:
                print(f"Safety filter error: {e}")
            
            if top_conf >= 0.3 and ml_recommendations:  # Only return if we still have recommendations after filtering
                print(f"Using domain-specific ML prediction ({detected_domain}): {top_class} (confidence: {top_conf:.3f})")
                # FORCE SAFETY FILTERS - Remove unrelated majors immediately
                filtered_final = []
                for rec in ml_recommendations[:5]:
                    major_name = rec["name"].lower()
                    # Only remove engineering majors for NON-engineering tech interests (like programming/software)
                    # Don't remove engineering majors for engineering interests
                    is_engineering_interest = any(eng_term in interests.lower() for eng_term in [
                        "mechanical engineering", "electrical engineering", "civil engineering", "chemical engineering", 
                        "building machine", "building machines", "building circuit", "building circuits", "building electrical",
                        "circuits", "circuit", "electronic", "electronics", "electrical",
                        "infrastructure", "processes", "flight", "space", "aircraft", "rocket", "rockets", 
                        "aerospace", "aviation", "airplane", "helicopter", "satellite", "spacecraft", "engineering challenges"
                    ])
                    if not is_engineering_interest and any(eng in major_name for eng in ["civil engineering", "mechanical engineering", "electrical engineering", "chemical engineering"]):
                        print(f"FORCE FILTER: Removing {rec['name']} for non-engineering tech interests")
                        continue
                    filtered_final.append(rec)
                
                # APPLY SCORE BOOSTS for specific majors
                cs_keywords = ["programming", "coding", "software", "app", "apps", "backend", "frontend", " api ", "database", "developer", "code", "website", "websites"]
                build_keywords = ["built", "build", "building", "developed", "programmed", "created", "creating"]
                architecture_keywords = ["building design", "buildings", "structures", "residential", "commercial building", "floor plan", "blueprint", "architect"]
                
                combined_lower = combined_user_text.lower()
                
                # Check if this is architecture context (buildings, not software)
                is_architecture_context = any(keyword in combined_lower for keyword in architecture_keywords)
                
                for rec in filtered_final:
                    if rec["name"] == "Computer Science":
                        cs_match = any(keyword in combined_lower for keyword in cs_keywords)
                        build_match = any(keyword in combined_lower for keyword in build_keywords)
                        
                        # Don't boost CS if it's architecture context
                        if not is_architecture_context:
                            # EDGE CASE: Database/API boost (highest priority)
                            if ("database" in combined_lower or "databases" in combined_lower) and ("api" in combined_lower or "apis" in combined_lower):
                                rec["score"] = max(rec["score"], 0.70)
                                print(f"DEBUG: CS database/API boost - new score: {rec['score']}")
                            elif cs_match and build_match:
                                # Strong boost when both development keywords and build keywords appear
                                rec["score"] = max(rec["score"], 0.75)
                                print(f"DEBUG: Computer Science STRONG boost applied (build context) - new score: {rec['score']}")
                            elif cs_match:
                                rec["score"] = max(rec["score"], 0.55)
                                print(f"DEBUG: Computer Science boost applied - new score: {rec['score']}")
                        else:
                            print(f"DEBUG: Skipping CS boost - architecture context detected")
                    
                    # Boost Architecture when architecture context is detected
                    elif rec["name"] == "Architecture" and is_architecture_context:
                        rec["score"] = max(rec["score"], 0.65)
                        print(f"DEBUG: Architecture boost applied (architecture context) - new score: {rec['score']}")
                    
                    # UX/UI Design boosts
                    elif rec["name"] == "UX/UI Design":
                        # EDGE CASE: UI design boost (check for singular and plural)
                        if "user interface" in combined_lower or "designing ui" in combined_lower or "design ui" in combined_lower:
                            rec["score"] = max(rec["score"], 0.95)
                            print(f"DEBUG: UX/UI interface boost - new score: {rec['score']}")
                    
                    # Graphic Design boosts
                    elif rec["name"] == "Graphic Design":
                        # Visual design edge case
                        if "visual design" in combined_lower or ("photoshop" in combined_lower and "design" in combined_lower):
                            rec["score"] = max(rec["score"], 0.70)
                            print(f"DEBUG: Graphic visual design boost - new score: {rec['score']}")
                        # Logo/branding edge case
                        elif "logo" in combined_lower or "brand identity" in combined_lower or "branding" in combined_lower:
                            rec["score"] = max(rec["score"], 0.75)
                            print(f"DEBUG: Graphic logo/branding boost - new score: {rec['score']}")
                    
                    # Civil Engineering boosts
                    elif rec["name"] == "Civil Engineering":
                        # EDGE CASE: Bridges/roads boost (check for singular and plural)
                        if (("bridge" in combined_lower or "bridges" in combined_lower) or ("road" in combined_lower or "roads" in combined_lower)) and not is_architecture_context:
                            rec["score"] = max(rec["score"], 0.70)
                            print(f"DEBUG: Civil Engineering bridges/roads boost - new score: {rec['score']}")
                    
                    # Finance boosts
                    elif rec["name"] == "Finance":
                        # Finance/investment edge case
                        if "finance" in combined_lower or "investment" in combined_lower or "financial" in combined_lower:
                            rec["score"] = max(rec["score"], 0.70)
                            print(f"DEBUG: Finance boost - new score: {rec['score']}")
                    
                    # Penalize UX/UI when development/build keywords appear (designers don't BUILD apps, developers do)
                    if rec["name"] == "UX/UI Design":
                        build_match = any(keyword in combined_lower for keyword in build_keywords)
                        
                        # Don't penalize UX/UI if it's architecture context
                        if is_architecture_context:
                            continue
                        
                        if build_match:
                            rec["score"] = rec["score"] * 0.7  # 30% penalty
                            print(f"DEBUG: UX/UI Design penalty applied (build context) - new score: {rec['score']}")
                
                # FORCE ADD Computer Science if tech/build keywords present but CS not in results
                cs_in_results = any(rec["name"] == "Computer Science" for rec in filtered_final)
                cs_match_global = any(keyword in combined_lower for keyword in cs_keywords)
                build_match_global = any(keyword in combined_lower for keyword in build_keywords)
                
                # Only force add if NOT architecture context
                if not cs_in_results and (cs_match_global or build_match_global) and not is_architecture_context:
                    print(f"DEBUG: FORCE ADDING Computer Science (detected app/web/build keywords but CS not in ML predictions)")
                    from ..databases.majors import MAJOR_DATABASE
                    cs_data = MAJOR_DATABASE.get("Computer Science", {})
                    cs_score = 0.75 if (cs_match_global and build_match_global) else 0.55
                    filtered_final.append({
                        "name": "Computer Science",
                        "score": cs_score,
                        "description": cs_data.get("description", ""),
                        "career_paths": cs_data.get("career_paths", []),
                        "source": "ML",
                        "confidence": 0.0
                    })
                
                # FORCE ADD Finance if finance/investment keywords present but Finance not in results
                finance_in_results = any(rec["name"] == "Finance" for rec in filtered_final)
                finance_keywords = ["finance", "investment", "financial", "banking", "portfolio", "stock"]
                finance_match_global = any(keyword in combined_lower for keyword in finance_keywords)
                
                if not finance_in_results and finance_match_global:
                    print(f"DEBUG: FORCE ADDING Finance (detected finance/investment keywords but Finance not in ML predictions)")
                    from ..databases.majors import MAJOR_DATABASE
                    finance_data = MAJOR_DATABASE.get("Finance", {})
                    filtered_final.append({
                        "name": "Finance",
                        "score": 0.70,
                        "description": finance_data.get("description", ""),
                        "career_paths": finance_data.get("career_paths", []),
                        "source": "ML",
                        "confidence": 0.0
                    })
                
                # Re-sort after boosts
                filtered_final.sort(key=lambda x: x["score"], reverse=True)
                return filtered_final
            else:
                print(f"Domain model confidence low ({top_conf:.3f}) or no valid recommendations; trying general model")
        except Exception as e:
            print(f"Domain-specific ML prediction failed: {e}, trying general model")
    
    # Try general ML prediction if domain model failed or not available
    if ml_models and 'major_classifier' in ml_models:
        try:
            # Convert subject_scores to the format expected by prepare_ml_features
            grades = [{"subject": k, "score": v*100} for k, v in subject_scores.items()]
            ml_features = prepare_ml_features(grades, interests, career_goals, 'local')

            clf = ml_models['major_classifier']
            ml_probabilities = clf.predict_proba(ml_features)[0]
            ml_classes = clf.classes_
            top_idx = int(np.argmax(ml_probabilities))
            top_class = ml_classes[top_idx]
            top_conf = float(ml_probabilities[top_idx])

            ml_recommendations = []
            for class_name, prob in zip(ml_classes, ml_probabilities):
                if prob > max(0.05, top_conf * 0.25):
                    from ..databases.majors import MAJOR_DATABASE
                    major_data = MAJOR_DATABASE.get(class_name, {})
                    ml_recommendations.append({
                        "name": class_name,
                        "score": float(prob),
                        "description": major_data.get("description", ""),
                        "career_paths": major_data.get("career_paths", []),
                        "source": "ML",
                        "confidence": round(top_conf, 3)
                    })

            ml_recommendations.sort(key=lambda x: x["score"], reverse=True)
            
            # Always apply safety filters
            print(f"DEBUG: Applying safety filters to {len(ml_recommendations)} ML recommendations")
            
            # Enhanced safety filter: Remove unrelated majors based on detected domain
            try:
                text_lower = combined_user_text.lower()
                
                # Define domain-specific terms
                tech_terms = ["computer science", "programming", "coding", "software", " ai ", "machine learning", "app development", "backend", "frontend", " api ", "database", "cybersecurity", "app", "apps", "website", "websites", "web development", "mobile app"]
                engineering_terms = ["electrical engineering", "circuit", "power systems", "mechanical engineering", "manufacturing", "civil engineering", "infrastructure", "chemical engineering", "aerospace", "aircraft"]
                medical_terms = ["doctor", "medicine", "medical", "hospital", "physician", "surgery", "patient", "healthcare", "dentist", "dental"]
                business_terms = ["business", "management", "finance", "marketing", "entrepreneur", "corporate", "investment", "commerce"]
                arts_terms = ["graphic design", "visual design", "ux design", "ui design", "wireframe", "figma", "architecture", "architect", "building", "painting", "music"]
                law_terms = ["law", "legal", "lawyer", "justice", "court", "attorney"]
                education_terms = ["teaching", "teacher", "education", "classroom", "educator", "professor"]
                
                # Detect what domains the user is interested in
                mentions_tech = any(t in text_lower for t in tech_terms)
                mentions_engineering = any(t in text_lower for t in engineering_terms)
                mentions_medical = any(t in text_lower for t in medical_terms)
                mentions_business = any(t in text_lower for t in business_terms)
                mentions_arts = any(t in text_lower for t in arts_terms)
                mentions_law = any(t in text_lower for t in law_terms)
                mentions_education = any(t in text_lower for t in education_terms)
                
                print(f"DEBUG SAFETY: text='{text_lower}'")
                print(f"DEBUG SAFETY: mentions_tech={mentions_tech}, mentions_engineering={mentions_engineering}")
                
                # Filter out unrelated majors based on detected interests
                filtered_recommendations = []
                for rec in ml_recommendations:
                    major_name = rec["name"].lower()
                    should_include = True
                    
                    # Tech/Data Science interests - remove non-tech majors (but NOT for engineering interests!)
                    if mentions_tech and not mentions_engineering:
                        if any(unrelated in major_name for unrelated in ["medicine", "dentistry", "law", "psychology", "education", "international relations", "architecture", "civil engineering", "mechanical engineering", "electrical engineering", "chemical engineering"]):
                            should_include = False
                            print(f"SAFETY: Filtering {rec['name']} for tech interests")
                    
                    # Engineering interests - remove non-engineering majors
                    if mentions_engineering:
                        if any(unrelated in major_name for unrelated in ["medicine", "dentistry", "law", "psychology", "education", "international relations", "business administration", "data science", "computer science"]):
                            should_include = False
                            print(f"SAFETY: Filtering {rec['name']} for engineering interests")
                    
                    # Medical interests - remove non-medical majors
                    elif mentions_medical and not mentions_tech and not mentions_engineering and not mentions_business:
                        if any(unrelated in major_name for unrelated in ["computer science", "data science", "electrical engineering", "mechanical engineering", "civil engineering", "chemical engineering", "law", "psychology", "education", "international relations", "architecture", "business administration"]):
                            should_include = False
                            print(f"SAFETY: Filtering {rec['name']} for medical interests")
                    
                    # Business interests - remove non-business majors
                    elif mentions_business and not mentions_tech and not mentions_engineering and not mentions_medical and not mentions_arts:
                        if any(unrelated in major_name for unrelated in ["medicine", "dentistry", "electrical engineering", "mechanical engineering", "civil engineering", "chemical engineering", "law", "psychology", "education", "international relations", "architecture"]):
                            should_include = False
                            print(f"SAFETY: Filtering {rec['name']} for business interests")
                    
                    # Arts/Architecture interests - remove non-arts majors
                    elif mentions_arts and not mentions_tech and not mentions_engineering and not mentions_medical and not mentions_business:
                        if any(unrelated in major_name for unrelated in ["medicine", "dentistry", "electrical engineering", "mechanical engineering", "civil engineering", "chemical engineering", "law", "psychology", "education", "international relations", "business administration", "computer science", "data science"]):
                            should_include = False
                            print(f"SAFETY: Filtering {rec['name']} for arts interests")
                    
                    # Law interests - remove non-law majors
                    elif mentions_law and not mentions_tech and not mentions_engineering and not mentions_medical and not mentions_business and not mentions_arts:
                        if any(unrelated in major_name for unrelated in ["medicine", "dentistry", "electrical engineering", "mechanical engineering", "civil engineering", "chemical engineering", "psychology", "education", "international relations", "architecture", "business administration", "computer science", "data science"]):
                            should_include = False
                            print(f"SAFETY: Filtering {rec['name']} for law interests")
                    
                    # Education interests - remove non-education majors
                    elif mentions_education and not mentions_tech and not mentions_engineering and not mentions_medical and not mentions_business and not mentions_arts and not mentions_law:
                        if any(unrelated in major_name for unrelated in ["medicine", "dentistry", "electrical engineering", "mechanical engineering", "civil engineering", "chemical engineering", "law", "psychology", "international relations", "architecture", "business administration", "computer science", "data science"]):
                            should_include = False
                            print(f"SAFETY: Filtering {rec['name']} for law interests")
                    
                    if should_include:
                        filtered_recommendations.append(rec)
                    else:
                        print(f"SAFETY: Excluded {rec['name']} from recommendations")
                
                ml_recommendations = filtered_recommendations
                print(f"DEBUG: After safety filtering: {len(ml_recommendations)} recommendations remain")
                
                # If filtering removed all recommendations, fall back to rule-based
                if not ml_recommendations:
                    print(f"SAFETY: All ML recommendations filtered, falling back to rule-based")
                    return intelligent_major_recommendations(subject_scores, enhanced_interests, enhanced_career_goals, user_preferences, interests)
            except Exception as e:
                print(f"Safety filter error: {e}")
            
            if top_conf >= 0.3 and ml_recommendations:  # Only return if we still have recommendations after filtering
                print(f"Using ML prediction: {top_class} (confidence: {top_conf:.3f})")
                # FORCE SAFETY FILTERS - Remove unrelated majors immediately
                filtered_final = []
                for rec in ml_recommendations[:5]:
                    major_name = rec["name"].lower()
                    # Only remove engineering majors for NON-engineering interests
                    detected_domain = detect_primary_domain(f"{interests} {career_goals}").get("domain", "general")
                    is_engineering_interest = (
                        any(eng in detected_domain for eng in ["mechanical_engineering", "electrical_engineering", "civil_engineering", "chemical_engineering"]) or
                        any(eng_term in interests.lower() for eng_term in [
                            "building circuit", "building circuits", "building electrical", "building machine", "building machines",
                            "circuit", "circuits", "electronic", "electronics", "electrical"
                        ])
                    )
                    
                    if not is_engineering_interest and any(eng in major_name for eng in ["civil engineering", "mechanical engineering", "electrical engineering", "chemical engineering"]):
                        print(f"FORCE FILTER: Removing {rec['name']} for non-engineering interests")
                        continue
                    filtered_final.append(rec)
                
                # APPLY SCORE BOOSTS for specific majors
                cs_keywords = ["programming", "coding", "software", "app", "apps", "backend", "frontend", " api ", "database", "developer", "code", "website", "websites"]
                build_keywords = ["built", "build", "building", "developed", "programmed", "created", "creating"]
                architecture_keywords = ["building design", "buildings", "structures", "residential", "commercial building", "floor plan", "blueprint", "architect"]
                combined_text = f"{interests} {career_goals}".lower()
                
                # Check if this is architecture context (buildings, not software)
                is_architecture_context = any(keyword in combined_text for keyword in architecture_keywords)
                
                for rec in filtered_final:
                    if rec["name"] == "Computer Science":
                        cs_match = any(keyword in combined_text for keyword in cs_keywords)
                        build_match = any(keyword in combined_text for keyword in build_keywords)
                        
                        # Don't boost CS if it's architecture context
                        if not is_architecture_context:
                            # EDGE CASE: Database/API boost (highest priority)
                            if ("database" in combined_text or "databases" in combined_text) and ("api" in combined_text or "apis" in combined_text):
                                rec["score"] = max(rec["score"], 0.70)
                                print(f"DEBUG: CS database/API boost - new score: {rec['score']}")
                            elif cs_match and build_match:
                                # Strong boost when both development keywords and build keywords appear
                                rec["score"] = max(rec["score"], 0.75)
                                print(f"DEBUG: Computer Science STRONG boost applied (build context) - new score: {rec['score']}")
                            elif cs_match:
                                rec["score"] = max(rec["score"], 0.55)
                                print(f"DEBUG: Computer Science boost applied - new score: {rec['score']}")
                        else:
                            print(f"DEBUG: Skipping CS boost - architecture context detected")
                    
                    # Boost Architecture when architecture context is detected
                    elif rec["name"] == "Architecture" and is_architecture_context:
                        rec["score"] = max(rec["score"], 0.65)
                        print(f"DEBUG: Architecture boost applied (architecture context) - new score: {rec['score']}")
                    
                    # UX/UI Design boosts
                    elif rec["name"] == "UX/UI Design":
                        # EDGE CASE: UI design boost (check for singular and plural)
                        if "user interface" in combined_text or "designing ui" in combined_text or "design ui" in combined_text:
                            rec["score"] = max(rec["score"], 0.95)
                            print(f"DEBUG: UX/UI interface boost - new score: {rec['score']}")
                    
                    # Graphic Design boosts
                    elif rec["name"] == "Graphic Design":
                        # Visual design edge case
                        if "visual design" in combined_text or ("photoshop" in combined_text and "design" in combined_text):
                            rec["score"] = max(rec["score"], 0.70)
                            print(f"DEBUG: Graphic visual design boost - new score: {rec['score']}")
                        # Logo/branding edge case
                        elif "logo" in combined_text or "brand identity" in combined_text or "branding" in combined_text:
                            rec["score"] = max(rec["score"], 0.75)
                            print(f"DEBUG: Graphic logo/branding boost - new score: {rec['score']}")
                    
                    # Civil Engineering boosts
                    elif rec["name"] == "Civil Engineering":
                        # EDGE CASE: Bridges/roads boost (check for singular and plural)
                        if (("bridge" in combined_text or "bridges" in combined_text) or ("road" in combined_text or "roads" in combined_text)) and not is_architecture_context:
                            rec["score"] = max(rec["score"], 0.70)
                            print(f"DEBUG: Civil Engineering bridges/roads boost - new score: {rec['score']}")
                    
                    # Finance boosts
                    elif rec["name"] == "Finance":
                        # Finance/investment edge case
                        if "finance" in combined_text or "investment" in combined_text or "financial" in combined_text:
                            rec["score"] = max(rec["score"], 0.70)
                            print(f"DEBUG: Finance boost - new score: {rec['score']}")
                    
                    # Penalize UX/UI when development/build keywords appear (designers don't BUILD apps, developers do)
                    if rec["name"] == "UX/UI Design":
                        build_match = any(keyword in combined_text for keyword in build_keywords)
                        
                        # Don't penalize UX/UI if it's architecture context
                        if is_architecture_context:
                            continue
                        
                        if build_match:
                            rec["score"] = rec["score"] * 0.7  # 30% penalty
                            print(f"DEBUG: UX/UI Design penalty applied (build context) - new score: {rec['score']}")
                
                # FORCE ADD Computer Science if tech/build keywords present but CS not in results
                cs_in_results = any(rec["name"] == "Computer Science" for rec in filtered_final)
                cs_match_global = any(keyword in combined_text for keyword in cs_keywords)
                build_match_global = any(keyword in combined_text for keyword in build_keywords)
                
                # Only force add if NOT architecture context
                if not cs_in_results and (cs_match_global or build_match_global) and not is_architecture_context:
                    print(f"DEBUG: FORCE ADDING Computer Science (detected app/web/build keywords but CS not in ML predictions)")
                    from ..databases.majors import MAJOR_DATABASE
                    cs_data = MAJOR_DATABASE.get("Computer Science", {})
                    cs_score = 0.75 if (cs_match_global and build_match_global) else 0.55
                    filtered_final.append({
                        "name": "Computer Science",
                        "score": cs_score,
                        "description": cs_data.get("description", ""),
                        "career_paths": cs_data.get("career_paths", []),
                        "source": "ML",
                        "confidence": 0.0
                    })
                
                # FORCE ADD Finance if finance/investment keywords present but Finance not in results
                finance_in_results = any(rec["name"] == "Finance" for rec in filtered_final)
                finance_keywords = ["finance", "investment", "financial", "banking", "portfolio", "stock"]
                finance_match_global = any(keyword in combined_text for keyword in finance_keywords)
                
                if not finance_in_results and finance_match_global:
                    print(f"DEBUG: FORCE ADDING Finance (detected finance/investment keywords but Finance not in ML predictions)")
                    from ..databases.majors import MAJOR_DATABASE
                    finance_data = MAJOR_DATABASE.get("Finance", {})
                    filtered_final.append({
                        "name": "Finance",
                        "score": 0.70,
                        "description": finance_data.get("description", ""),
                        "career_paths": finance_data.get("career_paths", []),
                        "source": "ML",
                        "confidence": 0.0
                    })
                
                # Re-sort after boosts
                filtered_final.sort(key=lambda x: x["score"], reverse=True)
                return filtered_final
            else:
                print(f"ML confidence low ({top_conf:.3f}); blending with rule-based")
        except Exception as e:
            print(f"ML prediction failed: {e}, falling back to rule-based")
    
    # Fallback to rule-based recommendations with enhanced text processing
    print("Using rule-based recommendations with enhanced text understanding")
    return intelligent_major_recommendations(subject_scores, enhanced_interests, enhanced_career_goals, user_preferences, interests)

def prepare_ml_features(grades: List[Dict[str, Any]], interests: str, career_goals: str = "", study_preference: str = "local") -> np.ndarray:
    """Prepare features for ML model inference - matches training features exactly"""
    # Convert grades to dict format
    grade_dict = {grade["subject"]: grade["score"] for grade in grades}
    
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
    
    for subject in subjects:
        grade = grade_dict.get(subject, 0)
        max_score = subject_max_scores.get(subject, 100)
        grade_features.append(grade / max_score)  # Normalize to 0-1 using subject-specific max scores
    
    # Text embedding features
    combined_text = f"{interests} {career_goals}"
    # Import sentence_model from text_processing
    from .text_processing import sentence_model
    if sentence_model:
        text_embedding = sentence_model.encode([combined_text])[0]
    else:
        # Fallback to zero vector if sentence model not available
        text_embedding = np.zeros(384)
    
    # Domain detection features
    from .text_processing import detect_primary_domain
    detected_domain = detect_primary_domain(combined_text).get("domain", "general")
    
    # Map current domains to training domains
    domain_mapping = {
        "electrical_engineering": "electrical_engineering",
        "mechanical_engineering": "mechanical_engineering", 
        "civil_engineering": "civil_engineering",
        "chemical_engineering": "chemical_engineering",
        "software_engineering": "technology",
        "data_science": "technology",
        "medicine": "medicine",
        "dentistry": "medicine",  # Map dentistry to medicine for ML
        "business": "business",
        "psychology": "arts",  # Map psychology to arts domain (includes psychology keywords)
        "architecture": "arts",  # Map architecture to arts for ML
        "education": "arts",  # Map education to arts for ML
        "international_relations": "arts",  # Map international relations to arts domain (includes international keywords)
        "general": "general"
    }
    
    mapped_domain = domain_mapping.get(detected_domain, "general")
    domain_features = [1 if domain == mapped_domain else 0 for domain in ['electrical_engineering', 'mechanical_engineering', 'civil_engineering', 'chemical_engineering', 'medicine', 'business', 'technology', 'arts', 'general']]
    
    # Study preference (always local)
    study_features = [1, 0, 0]  # local, abroad, both
    
    # Additional engineered features (must match training)
    grade_values = [grade_dict.get(subject, 0) for subject in subjects]
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
    return feature_vector.reshape(1, -1)
