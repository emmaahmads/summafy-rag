import chromadb
import os

CHROMA_DB_DIR = os.getenv("CHROMA_DB_DIR", "./chroma-data")

client = chromadb.PersistentClient(CHROMA_DB_DIR)
collection = client.get_or_create_collection("pdf_chunks")

# Fetch all documents (chunks) and their IDs, including embeddings
results = collection.get(include=["embeddings", "documents"])

print("IDs:")
print(results["ids"])
print("\nDocuments (chunks):")
for doc in results["documents"]:
    print(doc)

# Embedding structure info
embeddings = results["embeddings"]
print(f"\nNumber of embeddings: {len(embeddings)}")
if len(embeddings) > 0:
    print(f"Length of each embedding: {len(embeddings[0])}")
    print("First 10 values of first embedding:", embeddings[0][:10])
else:
    print("No embeddings found.")

# Uncomment below to also print embeddings (may be large)
# print("\nEmbeddings:")
# print(results["embeddings"])
