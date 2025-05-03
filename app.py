# app.py - Main Flask application for ReplyMind SMS AI Response Platform

from flask import Flask
import logging
from datetime import datetime
import json
from database import init_db, setup_pgvector, get_session
from routes.sms import handle_sms_webhook
from routes.business import handle_provision_number, handle_register_business
from routes.message import handle_get_message_history

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

# Initialize Database
init_db()

# Setup pgvector extension
with get_session() as session:
    setup_pgvector(session)

@app.route('/')
def home():
    """Homepage route - useful for checking if the app is running"""
    return "ReplyMind SMS AI Platform is running!"

@app.route('/sms/webhook', methods=['POST'])
def sms_webhook():
    return handle_sms_webhook()

@app.route('/api/provision-number', methods=['POST'])
def provision_number():
    return handle_provision_number()

@app.route('/api/register-business', methods=['POST'])
def register_business():
    return handle_register_business()

@app.route('/api/message-history/<phone_number>', methods=['GET'])
def get_message_history(phone_number):
    return handle_get_message_history(phone_number)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)