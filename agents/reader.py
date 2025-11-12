import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    """Reads text from a PDF file."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text.encode("utf-8", errors="ignore").decode()

def split_into_chunks(text):
    """Split text into chunks (paragraphs)."""
    chunks = text.split("\n\n")
    chunks = [c.strip() for c in chunks if len(c) > 50]
    return chunks

if __name__ == "__main__":
    text = extract_text_from_pdf("sample.pdf")
    chunks = split_into_chunks(text)
    print(len(chunks), "chunks extracted.")
