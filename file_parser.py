# file_parser.py
from io import BytesIO
import config
from logger import logger

try:
    from PyPDF2 import PdfReader
except ImportError:
    PdfReader = None
try:
    from docx import Document
except ImportError:
    Document = None

def parse_txt(file):
    return file.read().decode("utf-8", errors="ignore")

def parse_pdf(file):
    if PdfReader is None:
        raise ImportError("PyPDF2 missing")
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        t = page.extract_text()
        if t:
            text += t
    return text

def parse_docx(file):
    if Document is None:
        raise ImportError("python-docx missing")
    doc = Document(file)
    return "\n".join([p.text for p in doc.paragraphs])

def parse_file(uploaded_file):
    if uploaded_file is None:
        return ""
    ext = uploaded_file.name.split(".")[-1].lower()
    logger.info(f"Parsing {uploaded_file.name}")
    if ext == "txt":
        return parse_txt(uploaded_file)
    elif ext == "pdf":
        return parse_pdf(uploaded_file)
    elif ext == "docx":
        return parse_docx(uploaded_file)
    return ""