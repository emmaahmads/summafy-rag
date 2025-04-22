import os
import sys
import chromadb
from chromadb.config import Settings
import openai
import requests

# --- CONFIG ---
CHROMA_DB_DIR = os.getenv("CHROMA_DB_DIR", "./chroma_db")
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama2")  # Change to your preferred model
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# --- EMBED QUERY ---
def embed_query(query, model="text-embedding-ada-002"):
    openai.api_key = OPENAI_API_KEY
    resp = openai.embeddings.create(input=[query], model=model)
    return resp.data[0].embedding

# --- RETRIEVE CHUNKS ---
def retrieve_relevant_chunks(query, top_k=5):
    client = chromadb.Client(Settings(persist_directory=CHROMA_DB_DIR))
    collection = client.get_or_create_collection("pdf_chunks")
    query_emb = embed_query(query)
    results = collection.query(
        query_embeddings=[query_emb],
        n_results=top_k
    )
    # results["documents"] is a list of lists (one per query)
    return results["documents"][0] if results["documents"] else []

# --- SUMMARIZE WITH OLLAMA ---
def summarize_with_ollama(chunks, prompt_prefix="Summarize the following text:"):
    text = "\n".join(chunks)
    prompt = f"{prompt_prefix}\n{text}"
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt
    }
    response = requests.post(OLLAMA_API_URL, json=payload)
    response.raise_for_status()
    result = response.json()
    # Ollama API returns streaming chunks, but for basic use we expect 'response' key
    return result.get("response", "No summary returned.")

# --- MAIN ---
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python retrieve_summarize.py <QUERY>")
        sys.exit(1)
    query = sys.argv[1]
    print(f"Searching for relevant chunks for query: {query}")
    chunks = retrieve_relevant_chunks(query)
    print(f"Retrieved {len(chunks)} chunks. Sending to LLM for summarization...")
    summary = summarize_with_ollama(chunks)
    print("\n--- SUMMARY ---\n")
    print(summary)
