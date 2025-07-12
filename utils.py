from pathlib import Path
from docx import Document
import PyPDF2
import pdfplumber


def load_job_description():
    """Load job description from txt file"""
    job_file_path = Path("./job_description.txt")
    default_description = "No specific job description provided. Evaluate based on general professional standards."

    if not job_file_path.exists():
        print("Warning: job_description.txt not found. Using generic evaluation.")
        return default_description

    with open(job_file_path, "r", encoding="utf-8") as file:
        job_description = file.read().strip()
        if not job_description:
            print("Warning: job_description.txt is empty. Using generic evaluation.")
            return default_description

        return job_description


def extract_text_from_pdf(file_path):
    """Extract text from PDF file"""
    text = ""
    try:
        # Try with pdfplumber first (better for complex layouts)
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception:
        # Fallback to PyPDF2
        try:
            with open(file_path, "rb") as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            print(f"Error reading PDF {file_path}: {e}")
            return None

    return text.strip() if text.strip() else None


def extract_text_from_docx(file_path):
    """Extract text from DOCX file"""
    try:
        doc = Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text.strip() if text.strip() else None
    except Exception as e:
        print(f"Error reading DOCX {file_path}: {e}")
        return None


def extract_text_from_doc(file_path):
    """Extract text from DOC file (basic support)"""
    print(
        f"Warning: DOC files require additional setup. Consider converting {file_path} to PDF or DOCX"
    )
    return None
