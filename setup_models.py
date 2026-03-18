#!/usr/bin/env python
"""
Setup script for downloading required models and data.
Run this during deployment to pre-cache models.
"""

import subprocess
import sys
import nltk

print("Setting up spaCy language model...")
try:
    subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    print("✓ spaCy model downloaded successfully")
except Exception as e:
    print(f"✗ Failed to download spaCy model: {e}")

print("\nSetting up NLTK data...")
try:
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('omw-1.4')
    print("✓ NLTK data downloaded successfully")
except Exception as e:
    print(f"✗ Failed to download NLTK data: {e}")

print("\n✅ Setup complete!")
