#!/bin/bash
# Build a deployment package for AWS Lambda
# Usage: ./build_lambda_zip.sh

set -e

LAMBDA_DIR="lambda_package"
ZIP_FILE="lambda-ingestor.zip"

# Clean up any previous builds
rm -rf $LAMBDA_DIR $ZIP_FILE
mkdir $LAMBDA_DIR

# Install dependencies to the package directory
pip install --target $LAMBDA_DIR -r requirements.txt

# Copy source files (excluding otel_config.py)
cp extract_chunk_embed.py $LAMBDA_DIR/

# If you have other .py files to include, add them here
# cp another_module.py $LAMBDA_DIR/

# Create the zip file
cd $LAMBDA_DIR
zip -r ../$ZIP_FILE .
cd ..

echo "Lambda deployment package created: $ZIP_FILE"
