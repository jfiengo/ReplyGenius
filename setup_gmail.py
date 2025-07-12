#!/usr/bin/env python3
"""
Gmail Setup Script for ReplyMind

This script helps you set up Gmail authentication for your business email addresses.
You'll need to:

1. Go to Google Cloud Console (https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Gmail API
4. Create OAuth 2.0 credentials
5. Download the credentials.json file
6. Run this script to authenticate

Usage:
    python setup_gmail.py --business-id 1 --email your-business@example.com --credentials credentials.json
"""

import argparse
import os
import json
import requests
from database import get_session
from models import Business, EmailAddress
from routes.email import authenticate_gmail

def setup_gmail_for_business(business_id, email_address, credentials_file):
    """Set up Gmail authentication for a business email address"""
    
    # Verify credentials file exists
    if not os.path.exists(credentials_file):
        print(f"Error: Credentials file {credentials_file} not found")
        return False
    
    # Verify business exists
    session = get_session()
    try:
        business = session.query(Business).filter_by(id=business_id).first()
        if not business:
            print(f"Error: Business with ID {business_id} not found")
            return False
        
        print(f"Setting up Gmail for business: {business.name}")
        print(f"Email address: {email_address}")
        
        # Check if email already exists
        existing_email = session.query(EmailAddress).filter_by(email_address=email_address).first()
        if existing_email:
            print(f"Email address {email_address} is already registered")
            return True
        
        # Create token file path
        token_file = f"tokens/{business_id}_{email_address.replace('@', '_at_')}.json"
        os.makedirs(os.path.dirname(token_file), exist_ok=True)
        
        # Test authentication
        print("Testing Gmail authentication...")
        try:
            service = authenticate_gmail(credentials_file, token_file)
            print("✅ Gmail authentication successful!")
        except Exception as e:
            print(f"❌ Gmail authentication failed: {e}")
            return False
        
        # Create email address record
        email_record = EmailAddress(
            business_id=business_id,
            email_address=email_address,
            credentials_file=credentials_file,
            token_file=token_file
        )
        session.add(email_record)
        session.commit()
        
        print(f"✅ Email address {email_address} successfully registered for business {business.name}")
        return True
        
    except Exception as e:
        print(f"Error setting up Gmail: {e}")
        session.rollback()
        return False
    finally:
        session.close()

def list_business_emails():
    """List all registered business email addresses"""
    session = get_session()
    try:
        email_addresses = session.query(EmailAddress).join(Business).all()
        
        if not email_addresses:
            print("No email addresses registered")
            return
        
        print("Registered Email Addresses:")
        print("-" * 50)
        for email_addr in email_addresses:
            print(f"Business: {email_addr.business.name}")
            print(f"Email: {email_addr.email_address}")
            print(f"Status: {'Active' if email_addr.is_active else 'Inactive'}")
            print(f"Credentials: {email_addr.credentials_file}")
            print("-" * 50)
            
    except Exception as e:
        print(f"Error listing emails: {e}")
    finally:
        session.close()

def test_email_processing(business_id):
    """Test email processing for a business"""
    session = get_session()
    try:
        business = session.query(Business).filter_by(id=business_id).first()
        if not business:
            print(f"Business with ID {business_id} not found")
            return
        
        email_addresses = session.query(EmailAddress).filter_by(business_id=business_id, is_active=True).all()
        
        if not email_addresses:
            print(f"No active email addresses found for business {business.name}")
            return
        
        print(f"Testing email processing for business: {business.name}")
        
        for email_addr in email_addresses:
            print(f"Testing email: {email_addr.email_address}")
            try:
                service = authenticate_gmail(email_addr.credentials_file, email_addr.token_file)
                
                # Get recent messages (not just unread)
                results = service.users().messages().list(
                    userId='me', maxResults=5
                ).execute()
                
                messages = results.get('messages', [])
                print(f"Found {len(messages)} recent messages")
                
                if messages:
                    # Get first message details
                    message = service.users().messages().get(
                        userId='me', id=messages[0]['id']
                    ).execute()
                    
                    headers = message['payload']['headers']
                    sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
                    subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
                    
                    print(f"Sample message - From: {sender}, Subject: {subject}")
                
            except Exception as e:
                print(f"Error testing {email_addr.email_address}: {e}")
        
    except Exception as e:
        print(f"Error testing email processing: {e}")
    finally:
        session.close()

def main():
    parser = argparse.ArgumentParser(description='Setup Gmail for ReplyMind')
    parser.add_argument('--business-id', type=int, help='Business ID')
    parser.add_argument('--email', type=str, help='Email address to register')
    parser.add_argument('--credentials', type=str, help='Path to credentials.json file')
    parser.add_argument('--list', action='store_true', help='List all registered email addresses')
    parser.add_argument('--test', type=int, help='Test email processing for business ID')
    
    args = parser.parse_args()
    
    if args.list:
        list_business_emails()
    elif args.test:
        test_email_processing(args.test)
    elif args.business_id and args.email and args.credentials:
        setup_gmail_for_business(args.business_id, args.email, args.credentials)
    else:
        parser.print_help()

if __name__ == '__main__':
    main() 