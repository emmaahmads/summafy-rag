#!/bin/bash

# Function to pull a model
pull_model() {
    local model=$1
    echo "Pulling model: $model"
    ollama pull $model
}

# Pull the specified model or default to llama2
MODEL=${1:-llama2}
pull_model $MODEL

# Keep ollama running
wait # without wait there's no foreground process to keep the container running
