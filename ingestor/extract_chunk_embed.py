import sys
from PyPDF2 import PdfReader

# --- CONFIG ---
CHUNK_SIZE = 300  # characters per chunk

# --- PDF TEXT EXTRACTION ---
def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

# --- CHUNKING ---
def chunk_text(text, chunk_size=CHUNK_SIZE):
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i+chunk_size])
    return chunks

# --- MAIN ---
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_chunk_embed.py <PDF_PATH>")
        sys.exit(1)
    pdf_path = sys.argv[1]
    print(f"Extracting text from {pdf_path} ...")
    text = extract_text_from_pdf(pdf_path)
    print(f"Splitting into chunks ...")
    chunks = chunk_text(text)
    print(f"Extracted {len(chunks)} chunks.")
    print("Done.")
