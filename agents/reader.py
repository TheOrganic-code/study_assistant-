import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF using PyMuPDF.
    Works best for digital (text-based) PDFs.
    """
    text = ""
    try:
        with fitz.open(pdf_path) as doc:
            for page_num, page in enumerate(doc, start=1):
                page_text = page.get_text("text")
                text += f"\n\n--- Page {page_num} ---\n{page_text}"
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text.encode("utf-8", errors="ignore").decode()


def split_into_chunks(text, chunk_size=700):
    """
    Split extracted text into smaller chunks for model processing.
    Each chunk ≈ 700 words (ideal for Gemini and faster processing).
    """
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size]).strip()
        if len(chunk) > 50:
            chunks.append(chunk)
    return chunks
