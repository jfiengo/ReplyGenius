from flask import request
from twilio.twiml.messaging_response import MessagingResponse
import logging
from database import get_session
from models import Customer, Message, Business, PhoneNumber
from anthropic_client import AnthropicClient
from utils.context_utils import get_relevant_context

logger = logging.getLogger(__name__)





def handle_sms_webhook():
    """Webhook endpoint for receiving SMS messages from Twilio"""
    # Extract message data
    incoming_message = request.form.get('Body', '')
    sender_phone = request.form.get('From', '')
    recipient_phone = request.form.get('To', '')
    message_sid = request.form.get('MessageSid', '')
    
    # Normalize phone numbers - remove any spaces and ensure '+' prefix
    sender_phone = sender_phone.replace(' ', '')
    recipient_phone = recipient_phone.replace(' ', '')
    
    if not sender_phone.startswith('+'):
        sender_phone = '+' + sender_phone
    if not recipient_phone.startswith('+'):
        recipient_phone = '+' + recipient_phone
    
    logger.info(f"Received message from {sender_phone} to {recipient_phone}: {incoming_message}")
    
    # Get database session
    session = get_session()
    
    try:
        # Find or create customer
        customer = session.query(Customer).filter_by(phone_number=sender_phone).first()
        if not customer:
            customer = Customer(phone_number=sender_phone)
            session.add(customer)
            session.commit()
            logger.info(f"Created new customer with phone number: {sender_phone}")
        
        # Find business by phone number
        business = session.query(Business).join(PhoneNumber).filter(
            PhoneNumber.phone_number == recipient_phone,
            PhoneNumber.is_active == True
        ).first()
        
        if not business:
            logger.error(f"No active business found for phone number: {recipient_phone}")
            # Log all active phone numbers for debugging
            active_numbers = session.query(PhoneNumber).filter_by(is_active=True).all()
            logger.info(f"Active phone numbers in database: {[n.phone_number for n in active_numbers]}")
            # Log the exact query being executed
            query = session.query(Business).join(PhoneNumber).filter(
                PhoneNumber.phone_number == recipient_phone,
                PhoneNumber.is_active == True
            )
            logger.info(f"SQL Query: {str(query)}")
            return str(MessagingResponse().message("Error: Business not found"))
        
        logger.info(f"Found business: {business.name} (ID: {business.id}) for phone number: {recipient_phone}")
        
        # Store incoming message
        incoming_msg = Message(
            customer_id=customer.id,
            business_id=business.id,
            direction='inbound',
            content=incoming_message,
            message_sid=message_sid,
            status='received'
        )
        session.add(incoming_msg)
        session.commit()
        logger.info(f"Stored incoming message from {sender_phone}")
        
        # Get conversation history for context
        history = session.query(Message).filter(
            Message.customer_id == customer.id,
            Message.business_id == business.id
        ).order_by(Message.sent_at.desc()).limit(10).all()
        
        # Generate AI response using Anthropic Claude
        anthropic_client = AnthropicClient()
        if anthropic_client:
            # Convert history to format expected by anthropic_client
            history_formatted = [{
                'direction': msg.direction,
                'content': msg.content,
                'timestamp': msg.sent_at.isoformat()
            } for msg in reversed(history)]
            
            # Get relevant business context
            business_context = get_relevant_context(incoming_message, business.id, session)
            logger.info(f"Found relevant business context: {business_context[:100]}...")
            
            # Generate response with context
            response_text = anthropic_client.generate_response(
                message=incoming_message,
                message_history=history_formatted,
                business_context=business_context
            )
        else:
            response_text = "I apologize, but I'm having trouble generating a response at the moment. Please try again later."
        
        # Store outgoing message
        outgoing_msg = Message(
            customer_id=customer.id,
            business_id=business.id,
            direction='outbound',
            content=response_text,
            status='sent'
        )
        session.add(outgoing_msg)
        session.commit()
        logger.info(f"Stored outgoing message to {sender_phone}")
        
        # Create Twilio response
        resp = MessagingResponse()
        resp.message(response_text)
        
        logger.info(f"Sent response to {sender_phone}: {response_text}")
        
        return str(resp)
        
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        session.rollback()
        return str(MessagingResponse().message("Error processing message"))
    finally:
        session.close() 