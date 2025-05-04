from flask import request, jsonify
import logging
from database import get_session
from models import Business, ContextItem
import os
from werkzeug.utils import secure_filename
import tiktoken
from typing import List
import numpy as np
from anthropic_client import AnthropicClient
import PyPDF2

logger = logging.getLogger(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx'}
MAX_CHUNK_SIZE = 1000  # Maximum number of tokens per chunk
CHUNK_OVERLAP = 100    # Number of tokens to overlap between chunks

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def read_file_content(filepath: str) -> str:
    """Read content from different file types"""
    file_ext = filepath.rsplit('.', 1)[1].lower()
    
    if file_ext == 'pdf':
        with open(filepath, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            text = ""
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:  # Only add if text was extracted
                    text += page_text + "\n"
            logger.info(f"Extracted {len(text)} characters from PDF")
            return text
    else:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()

def chunk_text(text: str) -> List[str]:
    """Split text into overlapping chunks of approximately MAX_CHUNK_SIZE tokens"""
    encoding = tiktoken.get_encoding("cl100k_base")  # OpenAI's encoding
    tokens = encoding.encode(text)
    chunks = []
    
    logger.info(f"Total tokens in text: {len(tokens)}")
    
    for i in range(0, len(tokens), MAX_CHUNK_SIZE - CHUNK_OVERLAP):
        chunk_tokens = tokens[i:i + MAX_CHUNK_SIZE]
        chunk_text = encoding.decode(chunk_tokens)
        chunks.append(chunk_text)
        logger.info(f"Created chunk {len(chunks)} with {len(chunk_tokens)} tokens")
    
    return chunks

def handle_upload_context():
    """API endpoint to upload and process business context files"""
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    business_id = request.form.get('business_id')
    
    if not business_id:
        return jsonify({"error": "business_id is required"}), 400
    
    if not file or not allowed_file(file.filename):
        return jsonify({"error": f"Invalid file type. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"}), 400
    
    session = get_session()
    try:
        # Verify business exists
        business = session.query(Business).filter_by(id=business_id).first()
        if not business:
            return jsonify({"error": "Business not found"}), 404
        
        # Save file
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Read file content based on file type
        content = read_file_content(filepath)
        
        # Chunk the content
        chunks = chunk_text(content)
        
        # Initialize Anthropic client for embeddings
        anthropic_client = AnthropicClient()
        
        # Process each chunk
        context_items = []
        for i, chunk in enumerate(chunks):
            # Generate embedding
            embedding = anthropic_client.get_embedding(chunk)
            
            # Create context item
            context_item = ContextItem(
                business_id=business_id,
                context_type='file',
                title=f"{filename} - Chunk {i+1}",
                content=chunk,
                is_active=True,
                embedding=embedding
            )
            session.add(context_item)
            context_items.append(context_item)
        
        session.commit()
        
        # Clean up file
        os.remove(filepath)
        
        return jsonify({
            "success": True,
            "message": f"Processed {len(chunks)} chunks from {filename}",
            "context_items": [{
                "id": item.id,
                "title": item.title,
                "content_length": len(item.content)
            } for item in context_items]
        })
        
    except Exception as e:
        logger.error(f"Error processing file: {e}")
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close() 