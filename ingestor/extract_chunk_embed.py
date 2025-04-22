import os
import sys
import chromadb
from PyPDF2 import PdfReader
import openai

# --- CONFIG ---
CHROMA_DB_DIR = os.getenv("CHROMA_DB_DIR", "./chroma-data")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
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

# --- EMBEDDING (OpenAI) ---
def embed_chunks(chunks, model="text-embedding-ada-002"):
    openai.api_key = OPENAI_API_KEY
    embeddings = []
    for chunk in chunks:
        resp = openai.embeddings.create(input=[chunk], model=model)
        embeddings.append(resp.data[0].embedding)
    return embeddings

# --- STORE IN LOCAL CHROMA DB ---
def store_embeddings(chunks, embeddings, db_dir=CHROMA_DB_DIR):
    # Ensure the DB directory exists
    os.makedirs(db_dir, exist_ok=True)
    client = chromadb.PersistentClient(db_dir)
    collection = client.get_or_create_collection("pdf_chunks")
    for idx, (chunk, emb) in enumerate(zip(chunks, embeddings)):
        collection.add(
            embeddings=[emb],
            documents=[chunk],
            ids=[f"chunk_{idx}"]
        )
    print(f"Stored {len(chunks)} chunks in Chroma DB at {db_dir}")

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
    print(f"Embedding {len(chunks)} chunks ...")
    embeddings = embed_chunks(chunks)
    print(f"Storing in local Chroma DB ...")
    store_embeddings(chunks, embeddings)
    print("Done.")
