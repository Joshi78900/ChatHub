# src/models_config.py

# This dictionary maps a user-friendly name (what the user sees)
# to the OpenRouter internal model ID (what the API needs).

MODEL_CONFIG = {
    "🧠 GPT-4o (OpenAI)": {
        "id": "openai/gpt-4o",
        "description": "The latest flagship model, best for complex reasoning and general tasks."
    },
    "Anthropic Claude 3.5 Sonnet": {
        "id": "anthropic/claude-3.5-sonnet",
        "description": "Anthropic's balanced model, excels at code, math, and writing."
    },
    "Google Gemini Pro 1.5": {
        "id": "google/gemini-2.5-pro",
        "description": "Google's powerful model with a massive context window for long documents."
    },
    "Meta Llama 3.1 8B (Recommended)": {
        "id": "meta-llama/llama-3.1-8b-instruct",
        "description": "Fastest and highest-rated open model for general chat and quick responses."
    },
    "Mistral Large": {
        "id": "mistralai/mistral-large",
        "description": "Mistral's top-tier model, strong in multilingual tasks and technical fields."
    },
}

# A list of the user-friendly names, used for the dropdown selector in Streamlit.
MODEL_NAMES = list(MODEL_CONFIG.keys())