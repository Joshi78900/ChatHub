# src/api_helper.py

import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# CRITICAL: Fetch the API key securely from the environment
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Base URL for OpenRouter API
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

def get_openrouter_response(model_id: str, messages: list) -> str:
    """
    Sends a request to the OpenRouter API for a chat completion.

    Args:
        model_id (str): The specific OpenRouter model ID to use (e.g., 'openai/gpt-4o').
        messages (list): The chat history in the required OpenRouter format.

    Returns:
        str: The generated response text, or an error message.
    """
    if not OPENROUTER_API_KEY:
        return "ERROR: OpenRouter API key not found. Please check your .env file."

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://chathub-joshi78900.streamlit.app", # Replace with your live URL later!
        "X-Title": "ChatHub by Joshi78900",
    }

    data = {
        "model": model_id,
        "messages": messages,
        "stream": False, # For simplicity, we won't use streaming yet
    }

    try:
        # Making the POST request to the API
        response = requests.post(OPENROUTER_URL, headers=headers, json=data)
        response.raise_for_status() # Raises an HTTPError for bad responses (4xx or 5xx)

        # Parsing the JSON response
        response_json = response.json()

        # Extracting the message content
        return response_json["choices"][0]["message"]["content"]

    except requests.exceptions.RequestException as e:
        # Handle network errors, connection problems, and HTTP errors
        print(f"API Request Failed: {e}")
        return f"API ERROR: Could not connect to OpenRouter or got a bad response. Details: {e}"
    except KeyError:
        # Handle cases where the response JSON structure is unexpected
        print(f"API JSON Parsing Failed. Response: {response_json}")
        return "API ERROR: The response structure from OpenRouter was unexpected."
    except Exception as e:
        # Handle any other unexpected error
        return f"An unexpected error occurred: {e}"