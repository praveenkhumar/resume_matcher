#!/usr/bin/env python3
"""
Simple test script to verify the resume matcher functionality
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(__file__))

from utils.skill_extractor import extract_skills, preprocess_text
from utils.matcher import calculate_match_score

def test_preprocessing():
    """Test text preprocessing"""
    text = "I am proficient in Python, SQL, and Machine Learning!"
    processed = preprocess_text(text)
    print(f"Original: {text}")
    print(f"Processed: {processed}")
    return processed

def test_skill_extraction():
    """Test skill extraction"""
    text = "I have experience with Python, JavaScript, React, AWS, and Docker."
    skills = extract_skills(text, method='keyword')
    print(f"Text: {text}")
    print(f"Extracted skills: {skills}")
    return skills

def test_matching():
    """Test skill matching"""
    resume_skills = ["Python", "SQL", "React", "AWS"]
    job_skills = ["Python", "JavaScript", "React", "Docker", "AWS"]

    score, matched, missing = calculate_match_score(resume_skills, job_skills)
    print(f"Resume skills: {resume_skills}")
    print(f"Job skills: {job_skills}")
    print(f"Match score: {score}%")
    print(f"Matched: {matched}")
    print(f"Missing: {missing}")
    return score, matched, missing

if __name__ == "__main__":
    print("Testing Resume Matcher Components...")
    print("=" * 50)

    try:
        print("\n1. Testing text preprocessing:")
        test_preprocessing()

        print("\n2. Testing skill extraction:")
        test_skill_extraction()

        print("\n3. Testing skill matching:")
        test_matching()

        print("\n✅ All tests completed successfully!")

    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()