# app.py - Main Flask application for ReplyMind SMS AI Response Platform

from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import os
from dotenv import load_dotenv
import logging
from datetime import datetime
import json
from anthropic_client import AnthropicClient

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Twilio configuration
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')

# Initialize Twilio client
try:
    twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    logger.info("Twilio client initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Twilio client: {e}")
    twilio_client = None

# Initialize Anthropic client
try:
    anthropic_client = AnthropicClient()
    logger.info("Anthropic client initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Anthropic client: {e}")
    anthropic_client = None

# Simple in-memory message store (replace with PostgreSQL in step 3)
message_history = {}

@app.route('/')
def home():
    """Homepage route - useful for checking if the app is running"""
    return "ReplyMind SMS AI Platform is running!"

@app.route('/sms/webhook', methods=['POST'])
def sms_webhook():
    """Webhook endpoint for receiving SMS messages from Twilio"""
    # Extract message data
    incoming_message = request.form.get('Body', '')
    sender_phone = request.form.get('From', '')
    recipient_phone = request.form.get('To', '')
    message_sid = request.form.get('MessageSid', '')
    
    logger.info(f"Received message from {sender_phone} to {recipient_phone}: {incoming_message}")
    
    # Store message in history (temporary in-memory storage)
    if sender_phone not in message_history:
        message_history[sender_phone] = []
    
    message_history[sender_phone].append({
        'direction': 'inbound',
        'content': incoming_message,
        'timestamp': datetime.now().isoformat(),
        'message_sid': message_sid
    })
    
    # Generate AI response using Anthropic Claude
    if anthropic_client:
        # Get conversation history for context
        history = message_history[sender_phone][:-1]  # Exclude the current message
        response_text = anthropic_client.generate_response(incoming_message, history)
    else:
        response_text = "I apologize, but I'm having trouble generating a response at the moment. Please try again later."
    
    # Create Twilio response
    resp = MessagingResponse()
    resp.message(response_text)
    
    # Store our response in history too
    message_history[sender_phone].append({
        'direction': 'outbound',
        'content': response_text,
        'timestamp': datetime.now().isoformat()
    })
    
    logger.info(f"Sent response to {sender_phone}: {response_text}")
    
    return str(resp)

@app.route('/api/provision-number', methods=['POST'])
def provision_number():
    """API endpoint to provision a new Twilio phone number for a business"""
    if not twilio_client:
        return jsonify({"error": "Twilio client not initialized"}), 500
    
    data = request.json
    business_id = data.get('business_id')
    area_code = data.get('area_code')
    
    if not business_id:
        return jsonify({"error": "business_id is required"}), 400
    
    try:
        # Search for available phone numbers
        available_numbers = twilio_client.available_phone_numbers('US').local.list(
            area_code=area_code,
            limit=1
        )
        
        if not available_numbers:
            return jsonify({"error": "No available phone numbers found in specified area code"}), 404
        
        # Purchase the first available number
        new_number = twilio_client.incoming_phone_numbers.create(
            phone_number=available_numbers[0].phone_number,
            friendly_name=f"Business {business_id}"
        )
        
        # Configure the webhook URL for this number
        webhook_url = f"{request.host_url.rstrip('/')}/sms/webhook"
        new_number.update(
            sms_url=webhook_url
        )
        
        # In step 3, we'll save this to the database
        # For now, just log it
        logger.info(f"Provisioned number {new_number.phone_number} for business {business_id}")
        
        return jsonify({
            "success": True,
            "phone_number": new_number.phone_number,
            "business_id": business_id
        })
        
    except Exception as e:
        logger.error(f"Error provisioning number: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/message-history/<phone_number>', methods=['GET'])
def get_message_history(phone_number):
    """API endpoint to retrieve message history for a phone number"""
    # Normalize phone number format
    if not phone_number.startswith('+'):
        phone_number = '+' + phone_number
    
    if phone_number in message_history:
        return jsonify(message_history[phone_number])
    else:
        return jsonify([])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)