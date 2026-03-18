import spacy
import re
import json
import os
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk

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
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("spaCy model 'en_core_web_sm' not found. Please run: python -m spacy download en_core_web_sm")
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
    Extract skills using Named Entity Recognition (placeholder)
    """
    if not nlp:
        return []

    doc = nlp(text)

    # This is a simplified NER approach
    # In a real implementation, you might need custom NER training
    skills = []

    # Look for proper nouns that might be skills
    for ent in doc.ents:
        if ent.label_ in ['ORG', 'PRODUCT', 'GPE']:  # Organizations, Products, Geo-political entities
            skills.append(ent.text.lower())

    # Combine with keyword matching
    keyword_skills = extract_skills_keyword_matching(text)
    skills.extend(keyword_skills)

    return list(set(skills))

def extract_skills(text, method='keyword'):
    """
    Extract skills from text using specified method
    """
    if method == 'keyword':
        return extract_skills_keyword_matching(text)
    elif method == 'ner':
        return extract_skills_ner(text)
    else:
        raise ValueError("Invalid extraction method. Use 'keyword' or 'ner'")