FROM python:3.11-slim

WORKDIR /app

COPY ../requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY extract_chunk_embed.py ./
COPY inspect_chroma.py ./

CMD ["tail", "-f", "/dev/null"]
