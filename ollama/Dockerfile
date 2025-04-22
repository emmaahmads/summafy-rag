FROM ollama/ollama:latest

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy the model pulling script
COPY pull-models.sh /usr/local/bin/pull-models.sh
RUN chmod +x /usr/local/bin/pull-models.sh

# Set default model (can be overridden via environment variable)
ENV DEFAULT_MODEL=llama2

# Healthcheck to ensure Ollama is responding
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:11434/api/tags || exit 1

# Start Ollama API server and pull models
CMD ["/bin/sh", "-c", "/usr/local/bin/ollama serve & sleep 5 && /usr/local/bin/pull-models.sh ${DEFAULT_MODEL}"]
