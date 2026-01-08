"""
UI module.
Handles Streamlit UI components and chat interface.
"""

import streamlit as st

from config import MODEL_NAME, EMBED_MODEL_NAME


def setup_page_config():
    """Configure Streamlit page settings."""
    st.set_page_config(page_title="Internal Expertise Finder", layout="wide")


def display_header():
    """Display application header and title."""
    st.title("🔍 Internal Expertise Finder")
    st.caption(f"Powered by {MODEL_NAME} & {EMBED_MODEL_NAME}")


def initialize_chat_session():
    """
    Initialize chat session state with welcome message.
    
    Returns:
        List of message dictionaries
    """
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant", 
                "content": "Ready to search profiles. Try 'Who worked on Expertise Finder?' or 'Find a Node.js expert'."
            }
        ]
    
    return st.session_state.messages


def display_chat_history(messages: list):
    """
    Display chat message history.
    
    Args:
        messages: List of message dictionaries with 'role' and 'content' keys
    """
    for msg in messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])


def display_debug_context(response):
    """
    Display debug information showing retrieved context.
    
    Args:
        response: Chat engine response object
    """
    with st.expander("🔍 Debug: See Retrieved Context"):
        for node in response.source_nodes:
            st.text(f"--- From Profile: {node.metadata.get('name')} ---")
            # Show first 300 chars to verify project presence
            st.text(node.node.get_content()[:300] + "...")


def handle_chat_interaction(chat_engine):
    """
    Handle user chat input and display response.
    
    Args:
        chat_engine: Configured chat engine instance
    """
    if prompt := st.chat_input("Query employee database..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate and display response
        with st.chat_message("assistant"):
            with st.spinner("Searching..."):
                response = chat_engine.chat(prompt)
                st.markdown(response.response)
                
                # Show debug information
                display_debug_context(response)
        
        # Add assistant message to history
        st.session_state.messages.append({"role": "assistant", "content": response.response})
