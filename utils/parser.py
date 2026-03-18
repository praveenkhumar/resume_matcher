import fitz  # PyMuPDF
import pdfplumber
from docx import Document
import os

def extract_text_from_pdf(file_path):
    """
    Extract text from PDF using PyMuPDF (fitz)
    """
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        print(f"Error extracting text from PDF with PyMuPDF: {e}")
        # Fallback to pdfplumber
        try:
            with pdfplumber.open(file_path) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() or ""
                return text
        except Exception as e2:
            print(f"Error extracting text from PDF with pdfplumber: {e2}")
            return ""

def extract_text_from_docx(file_path):
    """
    Extract text from DOCX using python-docx
    """
    try:
        doc = Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        print(f"Error extracting text from DOCX: {e}")
        return ""

def extract_text(file_path):
    """
    Extract text from file based on extension
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension == '.pdf':
        return extract_text_from_pdf(file_path)
    elif file_extension == '.docx':
        return extract_text_from_docx(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_extension}. Supported formats: PDF, DOCX")