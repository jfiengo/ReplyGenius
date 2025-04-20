# test_webhook.py - Utility to simulate Twilio webhook requests
import requests
import argparse
import sys

def simulate_sms_webhook(server_url, from_number, message_body):
    """Simulate an incoming SMS webhook from Twilio to your local server"""
    
    # Default Twilio test phone number
    to_number = "+15005550006"  # Twilio's magic test number
    
    # Prepare the payload that Twilio would send
    payload = {
        "From": from_number,
        "To": to_number, 
        "Body": message_body,
        "MessageSid": "SM12345678901234567890123456789012"  # Dummy SID
    }
    
    try:
        # Send POST request to your webhook endpoint
        webhook_url = f"{server_url.rstrip('/')}/sms/webhook"
        print(f"Sending test webhook to: {webhook_url}")
        print(f"From: {from_number}")
        print(f"Message: {message_body}")
        
        response = requests.post(webhook_url, data=payload)
        
        # Print the response
        print("\nResponse Status Code:", response.status_code)
        print("Response Body:")
        print(response.text)
        
        return response
        
    except requests.exceptions.RequestException as e:
        print(f"Error sending request: {e}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulate Twilio SMS webhook requests")
    parser.add_argument("--url", "-u", default="http://localhost:5000", 
                        help="URL of your Flask application (default: http://localhost:5000)")
    parser.add_argument("--from", "-f", dest="from_number", default="+12345678901",
                        help="Sender's phone number (default: +12345678901)")
    parser.add_argument("--message", "-m", default="Test message from webhook simulator",
                        help="SMS message body")
    
    # If no arguments provided, show help
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
        
    args = parser.parse_args()
    
    simulate_sms_webhook(args.url, args.from_number, args.message)