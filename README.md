# summafy-doc-ingestor-summarizer

## Running Tests (Unit + Integration)

### 1. Run Tests Without Containers (Unit Tests, Mocks)

These tests use mocks for all external dependencies (OpenAI, ChromaDB, etc). No API keys or running containers are required.

```bash
# Install dependencies
pip install -r requirements.txt pytest reportlab

# Run all tests
pytest tests/
```

### 2. Run End-to-End Tests With Containers

These tests run the actual ingestion and retrieval code inside Docker containers, using real API keys and ChromaDB.

#### Prerequisites
- Docker and docker-compose installed
- A valid OpenAI API key
- (Optional) Ollama API running for summarization

#### Steps
1. **Set your OpenAI API key** (and optionally Ollama variables):
   - Create a `.env` file in the project root with:
     ```
     OPENAI_API_KEY=sk-...your-openai-key...
     # OLLAMA_API_URL and OLLAMA_MODEL if using Ollama
     ```
   - Or export in your shell:
     ```bash
     export OPENAI_API_KEY=sk-...your-openai-key...
     ```
2. **Build and start containers:**
   ```bash
   docker-compose up -d --build
   ```
3. **Copy or move your test PDF into the ingestor directory:**
   ```bash
   cp tests/mock_doc.pdf ingestor/mock_doc.pdf
   ```
4. **Run the ingestor on the PDF:**
   ```bash
   ./scripts/run_ingest.sh mock_doc.pdf
   ```
5. **Run the retriever with a query:**
   ```bash
   ./scripts/run_retrieve.sh "What is this PDF about?"
   ```

#### Troubleshooting
- If you see authentication errors, double-check your API key setup.
- If you get file not found errors, ensure the file path matches the container's view (e.g., `mock_doc.pdf` in `/app`).
- For Docker errors, try `docker-compose down -v` then `docker-compose up -d --build` to reset everything.

---

For more advanced or custom test scenarios, see the test files in `tests/` or ask for help!