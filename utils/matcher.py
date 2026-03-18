def calculate_match_score(resume_skills, job_skills):
    """
    Calculate match score between resume and job description skills

    Match Score (%) = (Matched Skills / Total JD Skills) * 100
    """
    if not job_skills:
        return 0.0, [], []

    # Convert to sets for comparison (case insensitive)
    resume_skills_set = set(skill.lower() for skill in resume_skills)
    job_skills_set = set(skill.lower() for skill in job_skills)

    # Find matching skills
    matched_skills = resume_skills_set.intersection(job_skills_set)

    # Find missing skills
    missing_skills = job_skills_set - resume_skills_set

    # Calculate match score
    if len(job_skills_set) > 0:
        match_score = (len(matched_skills) / len(job_skills_set)) * 100
    else:
        match_score = 0.0

    # Convert back to original case for display
    matched_skills_display = [skill for skill in resume_skills if skill.lower() in matched_skills]
    missing_skills_display = [skill for skill in job_skills if skill.lower() in missing_skills]

    return round(match_score, 2), matched_skills_display, missing_skills_display

def get_skill_recommendations(missing_skills, importance_weights=None):
    """
    Generate skill recommendations based on missing skills
    """
    if not missing_skills:
        return []

    recommendations = []

    # Simple recommendations - just list the missing skills
    for skill in missing_skills:
        recommendations.append(f"You should learn: {skill}")

    # If importance weights are provided, prioritize
    if importance_weights:
        weighted_recommendations = []
        for skill in missing_skills:
            weight = importance_weights.get(skill.lower(), 1)
            weighted_recommendations.append((skill, weight))

        # Sort by weight (descending)
        weighted_recommendations.sort(key=lambda x: x[1], reverse=True)

        recommendations = [f"You should learn: {skill} (Priority: {weight})"
                          for skill, weight in weighted_recommendations]

    return recommendations

def analyze_resume_job_match(resume_text, job_text, extraction_method='keyword', importance_weights=None):
    """
    Complete analysis pipeline
    """
    from .skill_extractor import extract_skills

    # Extract skills from resume and job description
    resume_skills = extract_skills(resume_text, method=extraction_method)
    job_skills = extract_skills(job_text, method=extraction_method)

    # Calculate match score
    match_score, matched_skills, missing_skills = calculate_match_score(resume_skills, job_skills)

    # Generate recommendations
    recommendations = get_skill_recommendations(missing_skills, importance_weights)

    return {
        'match_score': match_score,
        'resume_skills': resume_skills,
        'job_skills': job_skills,
        'matched_skills': matched_skills,
        'missing_skills': missing_skills,
        'recommendations': recommendations
    }