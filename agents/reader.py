import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    """Reads text from a PDF file using PyMuPDF."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text.encode("utf-8", errors="ignore").decode()

def split_into_chunks(text):
    """Split text into readable paragraph chunks."""
    chunks = text.split("\n\n")
    chunks = [c.strip() for c in chunks if len(c) > 50]
    return chunks
