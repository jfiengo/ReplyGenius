from flask import request, jsonify
import logging
import base64
import email
import os
import json
import time
import threading
from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from database import get_session
from models import Customer, Email, Business, EmailAddress
from anthropic_client import AnthropicClient
from utils.context_utils import get_relevant_context

logger = logging.getLogger(__name__)

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.send',
          'https://www.googleapis.com/auth/gmail.modify']

# Configuration
TESTING_SUBJECT_FILTER = "TESTING"  # Only process emails with this subject

# Global variable to track when monitoring started
monitoring_start_time = None

# Set to prevent tokenizer parallelism issues
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Track processed message IDs to prevent duplicates
processed_message_ids = set()
processed_message_ids_lock = threading.Lock()
MAX_PROCESSED_MESSAGES = 1000  # Keep only last 1000 processed message IDs

def authenticate_gmail(credentials_file, token_file):
    """Authenticate with Gmail API"""
    creds = None
    
    # Token file stores the user's access and refresh tokens
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    
    # If there are no valid credentials, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save credentials for next run
        with open(token_file, 'w') as token:
            token.write(creds.to_json())
    
    return build('gmail', 'v1', credentials=creds)

def extract_body(message):
    """Extract plain text body from Gmail message"""
    try:
        if 'parts' in message['payload']:
            for part in message['payload']['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body']['data']
                    return base64.urlsafe_b64decode(data).decode('utf-8')
        else:
            if message['payload']['mimeType'] == 'text/plain':
                data = message['payload']['body']['data']
                return base64.urlsafe_b64decode(data).decode('utf-8')
        return ""
    except Exception as e:
        logger.error(f"Error extracting email body: {e}")
        return ""



def send_reply(service, to_email, original_subject, response_text, thread_id=None):
    """Send reply email"""
    try:
        # Create proper email headers for a reply
        from_email = "me"  # Gmail will use the authenticated user's email
        
        # Build the email message with proper headers
        message_lines = [
            f"From: {from_email}",
            f"To: {to_email}",
            f"Subject: Re: {original_subject}",
            "MIME-Version: 1.0",
            "Content-Type: text/plain; charset=UTF-8",
            "Content-Transfer-Encoding: 7bit",
            "",  # Empty line to separate headers from body
            response_text
        ]
        
        message = "\n".join(message_lines)
        
        # Encode the message
        encoded_message = base64.urlsafe_b64encode(message.encode('utf-8')).decode('utf-8')
        
        # Prepare the request body
        body = {'raw': encoded_message}
        
        # Add thread ID if available to create a proper reply
        if thread_id:
            body['threadId'] = thread_id
            logger.info(f"Sending reply in thread {thread_id}")
        else:
            logger.info("No thread ID available, sending as new email")
        
        # Send the message
        send_message = service.users().messages().send(
            userId='me',
            body=body
        ).execute()
        
        logger.info(f"Reply sent to {to_email}")
        return send_message
    except Exception as e:
        logger.error(f"Error sending reply: {e}")
        return None

def process_email_for_business(email_address: str, session):
    """Process incoming emails for a specific business email address"""
    global processed_message_ids
    
    try:
        # Find business by email address
        business_email = session.query(EmailAddress).filter(
            EmailAddress.email_address == email_address,
            EmailAddress.is_active == True
        ).first()
        
        if not business_email:
            logger.error(f"No active business found for email address: {email_address}")
            return
        
        business = business_email.business
        logger.info(f"Processing emails for business: {business.name} (ID: {business.id})")
        
        # Authenticate with Gmail
        service = authenticate_gmail(business_email.credentials_file, business_email.token_file)
        
        # Get unread messages
        results = service.users().messages().list(
            userId='me', q='is:unread'
        ).execute()
        
        messages = results.get('messages', [])
        
        # Filter messages to only process those received after monitoring started
        if monitoring_start_time:
            filtered_messages = []
            for msg in messages:
                try:
                    # Get message details to check timestamp
                    message = service.users().messages().get(
                        userId='me', id=msg['id']
                    ).execute()
                    
                    # Get message timestamp (in milliseconds)
                    message_timestamp = int(message['internalDate'])
                    message_datetime = datetime.fromtimestamp(message_timestamp / 1000)
                    
                    # Only process messages received after monitoring started
                    if message_datetime > monitoring_start_time:
                        filtered_messages.append(msg)
                    else:
                        # Mark old messages as read without processing
                        service.users().messages().modify(
                            userId='me', id=msg['id'],
                            body={'removeLabelIds': ['UNREAD']}
                        ).execute()
                        logger.debug(f"Marked old message {msg['id']} as read (received before monitoring started)")
                        
                except Exception as e:
                    logger.error(f"Error checking message timestamp {msg['id']}: {e}")
                    continue
            
            messages = filtered_messages
            if messages:
                logger.info(f"Found {len(messages)} new messages to process (received after monitoring started)")
        else:
            # If monitoring_start_time is None, this is the first run - mark all existing as read
            logger.info("First monitoring run - marking all existing unread messages as read")
            for msg in messages:
                try:
                    service.users().messages().modify(
                        userId='me', id=msg['id'],
                        body={'removeLabelIds': ['UNREAD']}
                    ).execute()
                except Exception as e:
                    logger.error(f"Error marking message {msg['id']} as read: {e}")
            messages = []  # Don't process any existing messages
        
        for msg in messages:
            try:
                # Check if we've already processed this message
                with processed_message_ids_lock:
                    if msg['id'] in processed_message_ids:
                        logger.debug(f"Skipping already processed message {msg['id']}")
                        continue
                
                # Get full message
                message = service.users().messages().get(
                    userId='me', id=msg['id']
                ).execute()
                
                # Extract email details
                headers = message['payload']['headers']
                sender = next((h['value'] for h in headers if h['name'] == 'From'), '')
                subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '')
                thread_id = message.get('threadId', '')
                
                # Check if subject contains the testing filter
                if TESTING_SUBJECT_FILTER not in subject.upper():
                    logger.info(f"Skipping email with subject '{subject}' - does not contain '{TESTING_SUBJECT_FILTER}'")
                    # Mark as read even if we're not processing it
                    service.users().messages().modify(
                        userId='me', id=msg['id'],
                        body={'removeLabelIds': ['UNREAD']}
                    ).execute()
                    continue
                
                # Extract sender email
                sender_email = sender.split('<')[1].split('>')[0] if '<' in sender else sender
                
                # Get email body
                body = extract_body(message)
                
                if not body:
                    logger.warning(f"No body found for message {msg['id']}")
                    continue
                
                # Find or create customer
                customer = session.query(Customer).filter_by(email_address=sender_email).first()
                if not customer:
                    customer = Customer(email_address=sender_email)
                    session.add(customer)
                    session.commit()
                    logger.info(f"Created new customer with email: {sender_email}")
                
                # Store incoming email
                incoming_email = Email(
                    customer_id=customer.id,
                    business_id=business.id,
                    direction='inbound',
                    subject=subject,
                    content=body,
                    message_id=msg['id'],
                    thread_id=thread_id,
                    status='received'
                )
                session.add(incoming_email)
                session.commit()
                logger.info(f"Stored incoming email from {sender_email}")
                
                # Get conversation history for context
                history = session.query(Email).filter(
                    Email.customer_id == customer.id,
                    Email.business_id == business.id
                ).order_by(Email.sent_at.desc()).limit(10).all()
                
                # Generate AI response using Anthropic Claude
                anthropic_client = AnthropicClient()
                if anthropic_client:
                    # Convert history to format expected by anthropic_client
                    history_formatted = [{
                        'direction': email.direction,
                        'content': f"Subject: {email.subject}\n\n{email.content}",
                        'timestamp': email.sent_at.isoformat()
                    } for email in reversed(history)]
                    
                    # Get relevant business context
                    business_context = get_relevant_context(body, business.id, session)
                    logger.info(f"Found relevant business context: {business_context[:100]}...")
                    
                    # Generate response with context
                    response_text = anthropic_client.generate_response(
                        message=body,
                        message_history=history_formatted,
                        business_context=business_context
                    )
                else:
                    response_text = "I apologize, but I'm having trouble generating a response at the moment. Please try again later."
                
                # Send reply
                reply_message = send_reply(service, sender_email, subject, response_text, thread_id)
                
                # Store outgoing email
                outgoing_email = Email(
                    customer_id=customer.id,
                    business_id=business.id,
                    direction='outbound',
                    subject=f"Re: {subject}",
                    content=response_text,
                    thread_id=thread_id,
                    status='sent'
                )
                session.add(outgoing_email)
                session.commit()
                logger.info(f"Stored outgoing email to {sender_email}")
                
                # Mark as read
                service.users().messages().modify(
                    userId='me', id=msg['id'],
                    body={'removeLabelIds': ['UNREAD']}
                ).execute()
                
                # Add to processed set to prevent duplicate processing
                with processed_message_ids_lock:
                    processed_message_ids.add(msg['id'])
                    
                    # Clean up old message IDs to prevent memory growth
                    if len(processed_message_ids) > MAX_PROCESSED_MESSAGES:
                        # Remove oldest entries (convert to list, slice, convert back to set)
                        processed_message_ids = set(list(processed_message_ids)[-MAX_PROCESSED_MESSAGES:])
                
            except Exception as e:
                logger.error(f"Error processing individual message {msg['id']}: {e}")
                continue
                
    except Exception as e:
        logger.error(f"Error processing emails for {email_address}: {e}")

def handle_email_webhook():
    """Webhook endpoint for processing emails"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Extract email data from webhook
        email_address = data.get('email_address')
        
        if not email_address:
            return jsonify({"error": "email_address is required"}), 400
        
        # Process emails in a background thread
        def process_emails():
            session = get_session()
            try:
                process_email_for_business(email_address, session)
            except Exception as e:
                logger.error(f"Error in background email processing: {e}")
            finally:
                session.close()
        
        thread = threading.Thread(target=process_emails)
        thread.start()
        
        return jsonify({"success": True, "message": "Email processing started"})
        
    except Exception as e:
        logger.error(f"Error handling email webhook: {e}")
        return jsonify({"error": str(e)}), 500

def handle_register_email():
    """API endpoint to register a business email address"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        business_id = data.get('business_id')
        email_address = data.get('email_address')
        credentials_file = data.get('credentials_file')
        token_file = data.get('token_file')
        
        if not all([business_id, email_address, credentials_file]):
            return jsonify({"error": "business_id, email_address, and credentials_file are required"}), 400
        
        session = get_session()
        try:
            # Verify business exists
            business = session.query(Business).filter_by(id=business_id).first()
            if not business:
                return jsonify({"error": "Business not found"}), 404
            
            # Check if email address already exists
            existing_email = session.query(EmailAddress).filter_by(email_address=email_address).first()
            if existing_email:
                return jsonify({"error": "Email address already registered"}), 400
            
            # Create email address record
            email_record = EmailAddress(
                business_id=business_id,
                email_address=email_address,
                credentials_file=credentials_file,
                token_file=token_file or f"tokens/{business_id}_{email_address}.json"
            )
            session.add(email_record)
            session.commit()
            
            return jsonify({
                "success": True,
                "message": f"Email address {email_address} registered for business {business.name}",
                "email_id": email_record.id
            })
            
        except Exception as e:
            logger.error(f"Error registering email: {e}")
            session.rollback()
            return jsonify({"error": str(e)}), 500
        finally:
            session.close()
            
    except Exception as e:
        logger.error(f"Error in register email endpoint: {e}")
        return jsonify({"error": str(e)}), 500

def monitor_emails_for_business(business_id: int):
    """Monitor emails for a specific business"""
    session = get_session()
    try:
        # Get all active email addresses for the business
        email_addresses = session.query(EmailAddress).filter(
            EmailAddress.business_id == business_id,
            EmailAddress.is_active == True
        ).all()
        
        for email_address in email_addresses:
            process_email_for_business(email_address.email_address, session)
            
    except Exception as e:
        logger.error(f"Error monitoring emails for business {business_id}: {e}")
    finally:
        session.close()

def start_email_monitoring():
    """Start background email monitoring for all businesses"""
    global monitoring_start_time
    
    # Set the monitoring start time
    monitoring_start_time = datetime.now()
    logger.info(f"Email monitoring started at {monitoring_start_time}")
    
    def monitor_loop():
        while True:
            try:
                session = get_session()
                businesses = session.query(Business).all()
                
                for business in businesses:
                    monitor_emails_for_business(business.id)
                
                session.close()
                time.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                logger.error(f"Error in email monitoring loop: {e}")
                time.sleep(60)
    
    thread = threading.Thread(target=monitor_loop, daemon=True)
    thread.start()
    logger.info("Email monitoring thread started") 