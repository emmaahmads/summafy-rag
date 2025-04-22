FROM python:3.11-slim

WORKDIR /app

COPY ../requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY retrieve_summarize.py ./

CMD ["tail", "-f", "/dev/null"]
