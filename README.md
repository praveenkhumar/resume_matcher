# AI Resume Skill Extractor & Job Matcher

A Python-based web application that allows users to upload their resume and compare it with a job description to get a match score, extracted skills, and missing skill recommendations.

## Features

- **Resume Upload**: Support for PDF and DOCX formats
- **Text Extraction**: Uses PyMuPDF/pdfplumber for PDFs and python-docx for DOCX files
- **Skill Extraction**: NLP-powered skill identification using spaCy
- **Job Matching**: Compare resume skills with job requirements
- **Match Scoring**: Calculate percentage match between resume and job description
- **Recommendations**: Suggest missing skills to learn
- **Clean UI**: Built with Streamlit for easy web interface

## Project Structure

```
resume_matcher/
│── app.py                    # Main Streamlit application
│── utils/
│   ├── parser.py            # Text extraction from PDFs/DOCX
│   ├── skill_extractor.py   # NLP skill extraction
│   ├── matcher.py           # Skill matching and scoring logic
│── data/
│   ├── skills_list.json     # Predefined skills database
│── requirements.txt         # Python dependencies
│── README.md               # Project documentation
```

## Installation

1. **Clone or download the project**

   ```bash
   cd resume_matcher
   ```

2. **Create virtual environment**

   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows
   # or
   source venv/bin/activate     # On macOS/Linux
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Download spaCy language model**

   ```bash
   python -m spacy download en_core_web_sm
   ```

5. **Download NLTK data** (if not already downloaded)
   ```bash
   python -c "import nltk; nltk.download('stopwords'); nltk.download('wordnet')"
   ```

## Usage

1. **Run the application**

   ```bash
   streamlit run app.py
   ```

2. **Open your browser** to the URL shown (usually http://localhost:8501)

3. **Upload your resume** (PDF or DOCX format)

4. **Paste job description** in the text area

5. **Click "Analyze Match"** to get results

## How It Works

1. **Text Extraction**: Extracts raw text from uploaded resume files
2. **Preprocessing**: Cleans text, removes stopwords, applies lemmatization
3. **Skill Extraction**: Uses keyword matching or NER to identify skills
4. **Matching Logic**: Compares resume skills with job description skills
5. **Scoring**: Calculates match percentage and identifies gaps

## Skill Extraction Methods

- **Keyword Matching**: Matches against a predefined list of skills
- **NER (Named Entity Recognition)**: Uses spaCy to detect potential skills

## Tech Stack

- **Python**: Core programming language
- **Streamlit**: Web application framework
- **spaCy**: Natural Language Processing
- **PyMuPDF/pdfplumber**: PDF text extraction
- **python-docx**: DOCX text extraction
- **NLTK**: Text preprocessing

## Deployment

### Streamlit Cloud (Recommended)

1. **Push to GitHub**

   ```bash
   git add .
   git commit -m "your commit message"
   git push origin main
   ```

2. **Deploy to Streamlit Cloud**
   - Go to [streamlit.io/cloud](https://streamlit.io/cloud)
   - Connect your GitHub repository
   - Select the `main` branch and `app.py` as the main file
   - Click "Deploy"

3. **First Load Setup**
   - On first load, the app will automatically download the spaCy model and NLTK data
   - This may take 1-2 minutes on first deployment
   - Subsequent loads will be fast (models are cached)

4. **Important: Use Pinned Versions**
   - The `requirements.txt` includes specific versions to ensure compatibility
   - Don't remove version pins as they prevent dependency conflicts

### Local Deployment

```bash
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

### Troubleshooting

**"unable to infer type for attribute REGEX" error in production:**

- This error occurs if spaCy model is not properly installed
- The app automatically downloads the model on first load
- Check Streamlit Cloud logs: **Manage app > Logs**
- Solution: The app should auto-download on next load

**Models not downloading in production:**

- Ensure `requirements.txt` has the correct versions
- Our setup runs `setup_models()` on app startup to download missing components
- If still failing, you can pre-run: `python setup_models.py` before deployment

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Future Enhancements

- Add skill importance weighting
- Implement semantic matching with embeddings
- Support for more file formats
- User authentication and resume storage
- Integration with job boards APIs
- Advanced analytics and reporting
