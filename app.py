"""
Internal Expertise Finder - Main Application
A RAG-based chatbot for finding internal expertise and project information.
"""

from models import setup_global_settings
from indexing import create_vector_index
from filters import create_sidebar_filters, build_metadata_filters
from chat_engine import create_chat_engine
from ui import (
    setup_page_config,
    display_header,
    initialize_chat_session,
    display_chat_history,
    handle_chat_interaction
)


def main():
    """Main application entry point."""
    # Setup page configuration
    setup_page_config()
    
    # Display header
    display_header()
    
    # Initialize models and configure global settings
    llm, embed_model = setup_global_settings()
    
    # Create vector index
    index = create_vector_index()
    
    if not index:
        st.stop()
    
    # Create sidebar filters
    selected_location, selected_team = create_sidebar_filters(index)
    
    # Build metadata filters
    query_filters = build_metadata_filters(selected_location, selected_team)
    
    # Create chat engine with filters
    chat_engine = create_chat_engine(index, filters=query_filters)
    
    # Initialize and display chat
    messages = initialize_chat_session()
    display_chat_history(messages)
    
    # Handle chat interaction
    handle_chat_interaction(chat_engine)


if __name__ == "__main__":
    main()