# src/chathub_app.py

import streamlit as st

# Importing our helper files
from models_config import MODEL_NAMES, MODEL_CONFIG
from api_helper import get_openrouter_response

# --- 1. SET PAGE CONFIGURATION ---
# We set the title, icon (using an emoji), and enable wide mode for better UI space.
st.set_page_config(
    page_title="ChatHub - Universal LLM Interface",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded" 
)

# --- 2. HEADER AND TITLE ---
# The header is displayed prominently at the top.
st.title("🤖 ChatHub: The Universal LLM Interface")
st.caption("Powered by Streamlit and OpenRouter API. Talk to any model with one key!")

# --- 3. INITIAL SYSTEM PROMPT ---
# This is a hidden instruction we give the AI so it knows its role.
SYSTEM_PROMPT = (
    "You are ChatHub, a helpful and friendly AI assistant. "
    "Your responses should be polite, concise, and professional. "
    "Do not mention OpenRouter, Gemini, or Streamlit unless directly asked about them. "
    "Focus on providing accurate and high-quality information."
)

# The rest of the app logic will go below here.
# We will continue in the next steps.
# --- 4. SESSION STATE MANAGEMENT (Critical for continuity) ---
# Initialize chat history if it doesn't exist.
if "messages" not in st.session_state:
    # We start with the hidden system prompt as the first message
    st.session_state["messages"] = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

# Initialize model selection if it doesn't exist (default to the first model)
if "selected_model" not in st.session_state:
    st.session_state["selected_model"] = MODEL_NAMES[0] # The first model in our list

# --- 5. SIDEBAR: MODEL SELECTOR ---
with st.sidebar:
    st.header("⚙️ Configuration")

    # Dropdown for model selection
    selected_model_name = st.selectbox(
        "Choose your LLM:",
        MODEL_NAMES,
        index=MODEL_NAMES.index(st.session_state["selected_model"]),
        key="model_selector"
    )

    # Update session state if the selection changes
    st.session_state["selected_model"] = selected_model_name

    # Display model description for user clarity
    model_info = MODEL_CONFIG[selected_model_name]
    st.markdown(f"**Model ID:** `{model_info['id']}`")
    st.info(f"**Description:** {model_info['description']}")

    # Button to clear chat history
    if st.button("🗑️ Clear Chat History", help="Start a new conversation"):
        # Reset messages to just the system prompt
        st.session_state["messages"] = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]
        st.rerun() # Tells Streamlit to immediately restart the script and apply the change

    st.markdown("---")
    st.markdown("Project by Joshi78900")
    st.markdown("[GitHub Repo](https://github.com/Joshi78900/ChatHub.git)")

    # --- 6. DISPLAY CHAT HISTORY ---
# Loop through the messages stored in session state, skipping the hidden system prompt (index 0).
for message in st.session_state["messages"][1:]:
    # Use st.chat_message to create a styled message container.
    # The name of the role ('user' or 'assistant') dictates the styling and icon.
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# --- 7. USER INPUT AND RESPONSE GENERATION ---
# st.chat_input creates a persistent text input field at the bottom of the page.
if user_prompt := st.chat_input("Ask ChatHub a question..."):

    # 7a. Add User Message to History
    st.session_state["messages"].append({"role": "user", "content": user_prompt})

    # Display the user's message immediately
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # 7b. Generate Assistant Response
    # The 'with st.spinner' block shows a friendly loading message while we wait for the API.
    with st.spinner(f"ChatHub is thinking using {st.session_state['selected_model']}..."):

        # Prepare the history for the API call (excluding the system prompt)
        # We send ALL previous user and assistant messages to give the AI context.
        context_messages = [
            msg for msg in st.session_state["messages"] 
            if msg["role"] != "system" # API Helper includes system prompt automatically
        ]

        # The model ID is fetched from the config using the user-friendly name
        current_model_id = MODEL_CONFIG[st.session_state["selected_model"]]["id"]

        # Call the helper function to get the response
        assistant_response = get_openrouter_response(
            model_id=current_model_id,
            messages=st.session_state["messages"] # Send full history including System Prompt
        )

    # 7c. Display and Save Assistant Response
    with st.chat_message("assistant"):
        # Display the final response
        st.markdown(assistant_response)

        # CRITICAL: Save the AI's response to the history for future turns
        st.session_state["messages"].append({"role": "assistant", "content": assistant_response})

        # --- Bonus: Add a Copy Button (Step 15, we merged it here for efficiency) ---
        st.button(
            "📋 Copy Answer", 
            on_click=lambda: st.toast("Response copied to clipboard (browser dependent).", icon='✅'),
            key=f"copy_button_{len(st.session_state['messages'])}",
            help="Copy the AI's answer to your clipboard."
        )

# 7c. Display and Save Assistant Response with Error Handling
    with st.chat_message("assistant"):
        if "ERROR:" in assistant_response or "API ERROR:" in assistant_response:
            # Display error prominently in red
            st.error(assistant_response)
            st.warning("The error message above was NOT saved to the chat history to prevent context pollution.")
        else:
            # Display the successful response
            st.markdown(assistant_response)

            # CRITICAL: Save the AI's response ONLY IF it's not an error message
            st.session_state["messages"].append({"role": "assistant", "content": assistant_response})

            # --- Bonus: Add a Copy Button (Step 15) ---
            st.button(
                "📋 Copy Answer", 
                on_click=lambda: st.toast("Response copied to clipboard (browser dependent).", icon='✅'),
                key=f"copy_button_{len(st.session_state['messages'])}",
                help="Copy the AI's answer to your clipboard."
            )

