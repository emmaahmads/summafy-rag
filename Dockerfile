FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all scripts and code
COPY . .

# Default: keep container running for manual exec (override in docker-compose or with CMD)
CMD ["tail", "-f", "/dev/null"]
