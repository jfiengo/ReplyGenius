from flask import jsonify
import logging
from database import get_session
from models import Message, Customer

logger = logging.getLogger(__name__)

def handle_get_message_history(phone_number):
    """API endpoint to retrieve message history for a phone number"""
    # Normalize phone number format
    if not phone_number.startswith('+'):
        phone_number = '+' + phone_number
    
    session = get_session()
    try:
        # Find customer by phone number
        customer = session.query(Customer).filter_by(phone_number=phone_number).first()
        if not customer:
            return jsonify([])
        
        # Get message history
        messages = session.query(Message).filter(
            Message.customer_id == customer.id
        ).order_by(Message.sent_at.desc()).all()
        
        # Format response
        message_history = [{
            'direction': msg.direction,
            'content': msg.content,
            'timestamp': msg.sent_at.isoformat(),
            'status': msg.status
        } for msg in messages]
        
        return jsonify(message_history)
    finally:
        session.close() 