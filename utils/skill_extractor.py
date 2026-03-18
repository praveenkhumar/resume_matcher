import logging

import re
import json
import os
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk

logger = logging.getLogger(__name__)

# Download required NLTK data
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

# Load spaCy model
try:
    import spacy
    nlp = spacy.load("en_core_web_sm")
except Exception:
    nlp = None

# Load skills list
SKILLS_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'skills_list.json')
with open(SKILLS_FILE, 'r') as f:
    SKILLS_LIST = json.load(f)

def preprocess_text(text):
    """
    Clean and preprocess text
    """
    if not text:
        return ""

    # Convert to lowercase
    text = text.lower()

    # Remove special characters and extra whitespace
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()

    # Remove stopwords and lemmatize
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()

    words = text.split()
    processed_words = []

    for word in words:
        if word not in stop_words and len(word) > 1:
            lemma = lemmatizer.lemmatize(word)
            processed_words.append(lemma)

    return ' '.join(processed_words)

def extract_skills_keyword_matching(text):
    """
    Extract skills using keyword matching
    """
    if not text:
        return []

    processed_text = preprocess_text(text)
    words = set(processed_text.split())

    matched_skills = []
    for skill in SKILLS_LIST:
        skill_lower = skill.lower()
        # Check if skill is in the text (exact match or partial)
        if skill_lower in processed_text:
            matched_skills.append(skill)
        # Also check individual words for multi-word skills
        elif ' ' in skill_lower:
            skill_words = set(skill_lower.split())
            if skill_words.issubset(words):
                matched_skills.append(skill)

    return list(set(matched_skills))  # Remove duplicates

def extract_skills_ner(text):
    """
    Extract skills using Named Entity Recognition (NER).

    NOTE: spaCy can fail due to compatibility issues (especially with Python 3.14+).
    If NER fails, we fallback to keyword matching to keep the application working.
    """
    if not nlp:
        return extract_skills_keyword_matching(text)

    try:
        doc = nlp(text)

        # This is a simplified NER approach
        # In a real implementation, you might need custom NER training
        skills = []

        # Look for proper nouns that might be skills
        for ent in doc.ents:
            if ent.label_ in ['ORG', 'PRODUCT', 'GPE']:
                skills.append(ent.text.lower())

        # Combine with keyword matching
        keyword_skills = extract_skills_keyword_matching(text)
        skills.extend(keyword_skills)

        return list(set(skills))
    except Exception as e:
        # If NER fails for any reason (e.g., spaCy/pydantic runtime issue), fallback
        # to keyword matching so the app still provides useful output.
        logger.warning("NER skill extraction failed, falling back to keyword matching: %s", e)
        return extract_skills_keyword_matching(text)

def extract_skills(text, method='keyword'):
    """
    Extract skills from text using specified method
    """
    # Check if spaCy is broken (set by setup_models in production)
    try:
        import streamlit as st
        if st.session_state.get('spacy_broken', False):
            return extract_skills_keyword_matching(text)
    except ImportError:
        pass  # Not in Streamlit context

    if method == 'keyword':
        return extract_skills_keyword_matching(text)
    elif method == 'ner':
        return extract_skills_ner(text)
    else:
        raise ValueError("Invalid extraction method. Use 'keyword' or 'ner'")