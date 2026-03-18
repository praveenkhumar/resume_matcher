# AI Resume Skill Extractor & Job Matcher

A Python Streamlit app that extracts skills from resumes and compares them to a job description, producing a match score, extracted skills, and missing-skill recommendations.

## Features

- **Resume Upload**: PDF and DOCX support
- **Text Extraction**: Uses PyMuPDF/pdfplumber and python-docx
- **Skill Extraction**: Keyword matching and optional NER via spaCy
- **Job Matching**: Compares resume skills to job requirements
- **Match Scoring**: Percentage match and missing skill suggestions
- **Clean UI**: Built with Streamlit for quick usage

## Project Structure

```
resume_matcher/
├── app.py                    # Main Streamlit application
├── utils/
│   ├── parser.py            # Text extraction from PDFs/DOCX
│   ├── skill_extractor.py   # Skill extraction (keyword + optional NER)
│   └── matcher.py           # Matching and scoring logic
├── data/
│   └── skills_list.json     # Predefined skills database
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

## Installation (Local)

1. Clone the repository and change into the folder:

```bash
git clone <repo-url>
cd resume_matcher
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
# Windows (PowerShell)
venv\Scripts\Activate.ps1
# Windows (cmd)
venv\Scripts\activate.bat
# macOS / Linux
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Download NLTK data (if not already installed):

```bash
python -c "import nltk; nltk.download('stopwords'); nltk.download('wordnet')"
```

## Optional: Enable spaCy Model Auto-Download

To avoid large automatic downloads on low-disk systems, the app does not download the `en_core_web_sm` model by default.
If you want the app to attempt to download the model at startup, set the environment variable `ALLOW_MODEL_DOWNLOAD=1` before running Streamlit.

Examples:

```bash
# Linux / macOS
export ALLOW_MODEL_DOWNLOAD=1
streamlit run app.py

# Windows (PowerShell)
$env:ALLOW_MODEL_DOWNLOAD = "1"
streamlit run app.py
```

If `ALLOW_MODEL_DOWNLOAD` is not set, the app will run using keyword-only extraction and will not attempt to download the spaCy language model.

## Usage

Run the app locally:

```bash
streamlit run app.py
```

Open the URL shown by Streamlit (usually http://localhost:8501), upload a resume (PDF or DOCX), paste or enter a job description, and click "Analyze Match".

## Behavior & Notes

- The app first attempts to import `spaCy` and load the `en_core_web_sm` model if it is already installed.
- If `spaCy` or the model is not available (or import fails), the app falls back to fast keyword-based matching so the UI and matching still work.
- The fallback ensures the app remains usable on systems with limited disk space or when model installation fails.
- If `ALLOW_MODEL_DOWNLOAD=1` is set, the app will try to download the model at startup (this requires available disk space and network access).

## Troubleshooting

- "No module named 'spacy'" or "spaCy model not found":
  - Install spaCy and the model manually when you have disk space:

    ```bash
    pip install spacy
    python -m spacy download en_core_web_sm
    ```

- Disk space issues during installation:
  - Clean temporary files, remove large unused files, or run the app without enabling model downloads (default behavior).

- Streamlit Cloud / Python compatibility:
  - In some cloud environments using Python 3.14+, spaCy may encounter compatibility issues tied to Pydantic V1. If spaCy import fails in the cloud, the app will fall back to keyword matching automatically.

## Deployment (Streamlit Cloud)

1. Push your repo to GitHub.
2. Create a new app on Streamlit Cloud and point it to the `main` branch and `app.py`.
3. If you want Streamlit Cloud to download the spaCy model at first run, set the environment variable `ALLOW_MODEL_DOWNLOAD=1` in the app settings. Otherwise, leave it unset and the app will use keyword matching.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes and test locally
4. Submit a pull request

## License

MIT

## Future Enhancements

- Add an in-app toggle to enable/disable NER per session
- Add semantic matching with embeddings for better relevance
- Provide prepackaged Docker images with models included for easy deployment
