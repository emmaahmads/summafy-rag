import io
import logging
from PyPDF2 import PdfReader
import boto3

# --- CONFIG ---
CHUNK_SIZE = 300  # characters per chunk

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize AWS clients
s3 = boto3.client('s3')

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

def lambda_handler(event, context):
    try:
        # Validate and extract event data
        if not event or 'Records' not in event or not event['Records']:
            logger.error('Event structure is invalid or missing Records')
            return {
                'statusCode': 400,
                'statusMessage': 'Bad Request',
                'error': 'Invalid event structure.'
            }
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        logger.info(f"Processing file from bucket: {bucket}, key: {key}")
        # Get object content
        response = s3.get_object(Bucket=bucket, Key=key)
        object_content = response['Body'].read()
    except Exception as e:
        logger.exception('Failed to get file from S3')
        return {
            'statusCode': 500,
            'statusMessage': 'Internal Server Error',
            'error': str(e)
        }

    try:
        # Check if file is PDF by looking at magic numbers
        if object_content.startswith(b'%PDF'):
            pdf_file = io.BytesIO(object_content)
            text = extract_text_from_pdf(pdf_file)
            if text == "":
                logger.warning('PDF is not text-based or text extraction failed')
                return {
                    'statusCode': 415,
                    'statusMessage': 'Unsupported Media Type',
                    'error': 'File is not a text-based PDF or contains no extractable text.'
                }
            chunks = chunk_text(text)
            logger.info(f"Extracted {len(chunks)} chunks from PDF.")
            return {
                'statusCode': 200,
                'statusMessage': 'OK',
                'text': text,
                'chunks': chunks,
                'chunk_size': CHUNK_SIZE,
                'chunk_count': len(chunks)
            }
        else:
            logger.warning('File is not a PDF (magic number check failed)')
            return {
                'statusCode': 415,
                'statusMessage': 'Unsupported Media Type',
                'error': 'File is not a PDF.'
            }
    except Exception as e:
        logger.exception('Error processing PDF file')
        return {
            'statusCode': 500,
            'statusMessage': 'Error reading file',
            'error': str(e)
        }