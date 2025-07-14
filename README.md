# ReplyGenius
Automatic customer inquiry responding through email.

# Email Integration Setup Guide

This guide will help you set up email integration for your ReplyMind application, allowing it to automatically respond to incoming emails using the same RAG (Retrieval-Augmented Generation) system used for SMS.

## Overview

The email integration works similarly to the SMS workflow:
1. Monitors Gmail for unread messages
2. Processes incoming emails using your business context
3. Generates AI responses using Anthropic Claude
4. Sends automated replies
5. Stores conversation history

## Prerequisites

1. **Google Cloud Project**: You need a Google Cloud project with the Gmail API enabled
2. **OAuth 2.0 Credentials**: Gmail API credentials file (`credentials.json`)
3. **Business Registration**: Your business must be registered in the system first

## Step 1: Set Up Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Gmail API:
   - Go to "APIs & Services" > "Library"
   - Search for "Gmail API"
   - Click "Enable"

## Step 2: Create OAuth 2.0 Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth 2.0 Client IDs"
3. Choose "Desktop application" as the application type
4. Give it a name (e.g., "ReplyMind Email Integration")
5. Download the credentials file and save it as `credentials.json`

## Step 3: Install Dependencies

Install the new dependencies:

```bash
pip install -r requirements.txt
```

## Step 4: Register Your Business Email

Use the setup script to register your business email:

```bash
python setup_gmail.py --business-id 1 --email your-business@example.com --credentials credentials.json
```

This will:
- Test Gmail authentication
- Create a token file for future use
- Register the email address in the database

## Step 5: Start the Application

The email monitoring starts automatically when you run the main application:

```bash
python app.py
```

## API Endpoints

### Register Email Address
```http
POST /api/register-email
Content-Type: application/json

{
    "business_id": 1,
    "email_address": "your-business@example.com",
    "credentials_file": "path/to/credentials.json",
    "token_file": "path/to/token.json"  // optional
}
```

### Email Webhook
```http
POST /email/webhook
Content-Type: application/json

{
    "email_address": "your-business@example.com"
}
```

## How It Works

### Email Processing Flow

1. **Monitoring**: The system continuously monitors Gmail for unread messages
2. **Subject Filtering**: Only processes emails with "TESTING" in the subject line (for safety during testing)
3. **Extraction**: When a new email arrives, it extracts:
   - Sender email address
   - Subject line
   - Email body (plain text)
   - Thread ID (for conversation continuity)
4. **Customer Management**: Creates or finds the customer record
5. **Context Retrieval**: Uses semantic search to find relevant business context
6. **AI Response**: Generates a response using Anthropic Claude with:
   - Email content
   - Conversation history
   - Relevant business context
7. **Reply**: Sends the response and marks the original email as read
8. **Storage**: Stores both incoming and outgoing emails in the database

### Testing Safety

The system includes a safety filter that only processes emails with "TESTING" in the subject line. This prevents accidental automated responses to important emails during testing. To process all emails, you can modify the `TESTING_SUBJECT_FILTER` constant in `routes/email.py`.

### Database Schema

New tables have been added to support email functionality:

- **`email_addresses`**: Stores business email addresses and authentication info
- **`emails`**: Stores all email conversations (similar to `messages` table)
- **`customers`**: Extended to include email addresses

## Configuration

### Environment Variables

No additional environment variables are required beyond your existing setup.

### File Structure

```
ReplyGenius/
├── credentials.json          # Your Gmail API credentials
├── tokens/                   # Directory for OAuth tokens
│   ├── 1_business_at_example_com.json
│   └── ...
├── routes/
│   └── email.py             # Email processing logic
└── setup_gmail.py           # Setup helper script
```

## Testing

### Test Email Processing

```bash
python setup_gmail.py --test 1
```

This will test the email processing for business ID 1.

### List Registered Emails

```bash
python setup_gmail.py --list
```

## Troubleshooting

### Common Issues

1. **Authentication Errors**:
   - Ensure your `credentials.json` file is valid
   - Check that the Gmail API is enabled in your Google Cloud project
   - Verify the OAuth consent screen is configured

2. **Permission Errors**:
   - Make sure the Gmail account has the necessary permissions
   - Check that the OAuth scopes include read, send, and modify permissions

3. **No Emails Processed**:
   - Verify the email address is registered and active
   - Check the logs for any errors
   - Ensure there are unread emails in the Gmail account

### Logs

Check the application logs (`app.log`) for detailed error messages and processing information.

## Security Considerations

1. **Credentials Storage**: Store `credentials.json` securely and don't commit it to version control
2. **Token Files**: Token files contain sensitive authentication data and should be protected
3. **Email Access**: The system will have full access to read and send emails from the configured account
4. **Data Privacy**: Ensure compliance with relevant data protection regulations

## Monitoring

The system logs all email processing activities. Key metrics to monitor:

- Number of emails processed
- Response generation success rate
- Authentication token refresh events
- Error rates and types

## Integration with Existing Features

The email integration uses the same:
- Business context system
- Anthropic Claude integration
- Customer management
- Conversation history tracking

This ensures consistent responses across SMS and email channels. 
