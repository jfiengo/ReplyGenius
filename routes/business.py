from flask import request, jsonify
from twilio.rest import Client
import os
import logging
from database import get_session
from models import Business, PhoneNumber
from datetime import datetime

logger = logging.getLogger(__name__)

# Twilio configuration
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')

# Initialize Twilio client
try:
    twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    logger.info("Twilio client initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Twilio client: {e}")
    twilio_client = None

def handle_register_business():
    """API endpoint to register a new business"""
    data = request.json
    
    # Validate required fields
    required_fields = ['name', 'business_type']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    session = get_session()
    try:
        # Create new business
        business = Business(
            name=data['name'],
            business_type=data['business_type'],
            services=data.get('services'),
            hours=data.get('hours')
        )
        
        session.add(business)
        session.commit()
        
        # If phone number is provided, register it
        phone_number = data.get('phone_number')
        if phone_number:
            # Validate phone number format
            if not phone_number.startswith('+'):
                phone_number = '+' + phone_number
            
            # Check if phone number is already registered
            existing_number = session.query(PhoneNumber).filter_by(phone_number=phone_number).first()
            if existing_number:
                session.rollback()
                return jsonify({
                    "error": "Phone number already registered",
                    "business_id": existing_number.business_id
                }), 400
            
            # Create phone number record
            phone_record = PhoneNumber(
                business_id=business.id,
                phone_number=phone_number,
                is_active=True,
                provider=data.get('provider', 'manual')  # Default to 'manual' if not specified
            )
            session.add(phone_record)
            session.commit()
        
        logger.info(f"Registered new business: {business.name} (ID: {business.id})")
        
        # Prepare response
        response = {
            "success": True,
            "business": {
                "id": business.id,
                "name": business.name,
                "business_type": business.business_type,
                "services": business.services,
                "hours": business.hours,
                "created_at": business.created_at.isoformat()
            }
        }
        
        # Add phone number info if registered
        if phone_number:
            response["phone_number"] = {
                "number": phone_record.phone_number,
                "is_active": phone_record.is_active,
                "provider": phone_record.provider
            }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error registering business: {e}")
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

def handle_provision_number():
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
        
        # Save to database
        session = get_session()
        try:
            phone_number = PhoneNumber(
                business_id=business_id,
                phone_number=new_number.phone_number,
                is_active=True,
                provider='twilio',
                provider_id=new_number.sid
            )
            session.add(phone_number)
            session.commit()
            
            logger.info(f"Provisioned number {new_number.phone_number} for business {business_id}")
            
            return jsonify({
                "success": True,
                "phone_number": new_number.phone_number,
                "business_id": business_id
            })
        finally:
            session.close()
        
    except Exception as e:
        logger.error(f"Error provisioning number: {e}")
        return jsonify({"error": str(e)}), 500 