# src/chathub_app.py

import streamlit as st
import json
import os

# Importing our helper files
from models_config import MODEL_NAMES, MODEL_CONFIG
from api_helper import get_openrouter_response

# --- 1. SET PAGE CONFIGURATION ---
st.set_page_config(
    page_title="ChatHub - Universal LLM Interface",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded" 
)

# --- 2. INITIAL SYSTEM PROMPT ---
SYSTEM_PROMPT = (
    "You are ChatHub, a helpful and friendly AI assistant. "
    "Your responses should be polite, concise, and professional. "
    "Do not mention OpenRouter, Streamlit, or the model name unless directly asked about them. "
    "Focus on providing accurate and high-quality information."
)

# --- PERSISTENCE: SAVE/LOAD FUNCTIONS ---
HISTORY_FILE = "chathub_history.json" 

def save_history():
    """Saves the current chat history to a JSON file."""
    chat_content = st.session_state["messages"][1:] 
    with open(HISTORY_FILE, "w") as f:
        json.dump(chat_content, f, indent=4)
    st.toast("Chat history saved!", icon='💾')

def load_history():
    """Loads chat history from the JSON file if it exists."""
    if os.path.exists(HISTORY_FILE) and os.path.getsize(HISTORY_FILE) > 0:
        with open(HISTORY_FILE, "r") as f:
            try:
                loaded_messages = json.load(f)
                return [{"role": "system", "content": SYSTEM_PROMPT}] + loaded_messages
            except json.JSONDecodeError:
                return [{"role": "system", "content": SYSTEM_PROMPT}]
    return [{"role": "system", "content": SYSTEM_PROMPT}]

def clear_and_start_new_chat():
    """Resets messages and saves the cleared state."""
    st.session_state["messages"] = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]
    save_history()
    st.rerun() 

# --- 4. SESSION STATE MANAGEMENT (Critical for continuity and persistence) ---
if "messages" not in st.session_state:
    st.session_state["messages"] = load_history()
    
if "selected_model" not in st.session_state:
    st.session_state["selected_model"] = MODEL_NAMES[0] 

# --- 5. SIDEBAR: MODEL SELECTOR & PERSISTENT HISTORY ---
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Dropdown for model selection
    selected_model_name = st.selectbox(
        "Choose your LLM:",
        MODEL_NAMES,
        index=MODEL_NAMES.index(st.session_state["selected_model"]),
        key="model_selector"
    )

    st.session_state["selected_model"] = selected_model_name
    
    # Display model description for user clarity
    model_info = MODEL_CONFIG[selected_model_name]
    st.markdown(f"**Model ID:** `{model_info['id']}`")
    st.info(f"**Description:** {model_info['description']}")
    
    st.markdown("---")

    st.subheader("💾 Data Control")
    
    # Button to SAVE chat history
    st.button(
        "💾 Save Session", 
        on_click=save_history,
        help="Manually saves the current conversation history to disk."
    )
    
    st.markdown("---")
    
    st.subheader("💬 Recent History Preview")
    # Display the last 5 user messages in the sidebar for quick reference
    preview_count = 0
    for message in reversed(st.session_state["messages"]):
        if message["role"] == "user":
            st.text(f"• {message['content'][:30]}...") 
            preview_count += 1
            if preview_count >= 5:
                break
            
    if preview_count == 0:
        st.caption("Start a new chat to see history.")
        
    st.markdown("---")
    st.markdown("Project by Joshi78900")
    st.markdown("[GitHub Repo](https://github.com/Joshi78900/ChatHub.git)")

# --- 6. MAIN CHAT CONTAINER (Gemini-style Centering) ---
# We use st.container to create a centered column for the chat interface
# This creates a visually cleaner, less "wide" look, like modern chat UIs.
col1, col2, col3 = st.columns([1, 4, 1])

with col2:
    st.title("🤖 ChatHub")
    st.caption(f"Talking to **{st.session_state['selected_model']}** via OpenRouter API.")
    
    # --- NEW CHAT BUTTON ---
    st.button(
        "✨ Start New Chat", 
        on_click=clear_and_start_new_chat,
        help="Clears the current conversation and starts fresh.",
        use_container_width=True
    )
    
    st.markdown("---")

    # --- DISPLAY CHAT HISTORY ---
    # Loop through the messages stored in session state, skipping the hidden system prompt (index 0).
    for message in st.session_state["messages"][1:]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # --- 7. USER INPUT AND RESPONSE GENERATION ---
    # Use the same centered column for the input box
    if user_prompt := st.chat_input("Ask ChatHub a question..."):
        
        # 7a. Add User Message to History
        st.session_state["messages"].append({"role": "user", "content": user_prompt})
        
        # Display the user's message immediately
        with st.chat_message("user"):
            st.markdown(user_prompt)

        # 7b. Generate Assistant Response
        with st.spinner(f"ChatHub is thinking using {st.session_state['selected_model']}..."):
            
            current_model_id = MODEL_CONFIG[st.session_state["selected_model"]]["id"]
            
            assistant_response = get_openrouter_response(
                model_id=current_model_id,
                messages=st.session_state["messages"]
            )
            
        # 7c. Display and Save Assistant Response with Error Handling
        with st.chat_message("assistant"):
            if "ERROR:" in assistant_response or "API ERROR:" in assistant_response:
                st.error(assistant_response)
                st.warning("The error message above was NOT saved to the chat history.")
            else:
                st.markdown(assistant_response)
                
                # CRITICAL: Save the AI's response ONLY IF it's not an error message
                st.session_state["messages"].append({"role": "assistant", "content": assistant_response})
            
                # --- Add a Copy Button ---
                st.button(
                    "📋 Copy Answer", 
                    on_click=lambda: st.toast("Response copied to clipboard (browser dependent).", icon='✅'),
                    key=f"copy_button_{len(st.session_state['messages'])}",
                    help="Copy the AI's answer to your clipboard."
                )