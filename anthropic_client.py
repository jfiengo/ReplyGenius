import os
from dotenv import load_dotenv
import logging
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_anthropic import ChatAnthropic
from typing import List, Dict, Any

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

class AnthropicClient:
    def __init__(self):
        """Initialize the Anthropic client with API key from environment variables"""
        self.api_key = os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is not set")
        
        # Initialize Langchain's Anthropic client
        self.client = ChatAnthropic(
            anthropic_api_key=self.api_key,
            model="claude-3-haiku-20240307"  # Using Haiku for cost-effective testing
        )
        
        # Initialize the chat prompt template
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are a helpful AI assistant. Your task is to respond to messages in a friendly, professional, and concise manner.
            You are communicating via SMS, so keep your responses brief and to the point while maintaining a helpful and friendly tone."""),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}")
        ])

    def _format_message_history(self, message_history: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """
        Convert message history from the database format to Langchain message format
        
        Args:
            message_history (List[Dict[str, Any]]): Message history in the format from get_message_history
            
        Returns:
            List[Dict[str, str]]: Messages in Langchain format
        """
        formatted_messages = []
        for msg in message_history:
            role = "human" if msg['direction'] == 'inbound' else "ai"
            formatted_messages.append({
                "role": role,
                "content": msg['content']
            })
        return formatted_messages

    def generate_response(self, message: str, message_history: List[Dict[str, Any]] = None) -> str:
        """
        Generate a response using Claude API
        
        Args:
            message (str): The incoming message to respond to
            message_history (List[Dict[str, Any]], optional): Message history in the format from get_message_history
            
        Returns:
            str: The generated response
        """
        try:
            # Format the message history if provided
            chat_history = []
            if message_history:
                chat_history = self._format_message_history(message_history)
            
            # Format the prompt using the template
            formatted_prompt = self.prompt_template.format_messages(
                chat_history=chat_history,
                input=message
            )
            
            # Get response from Langchain's Anthropic client
            response = self.client.invoke(formatted_prompt)
            
            # Return the response content
            return response.content
            
        except Exception as e:
            logger.error(f"Error generating response from Claude: {e}")
            return "I apologize, but I'm having trouble generating a response at the moment. Please try again later." 