"""
Model initialization module.
Handles initialization of LLM and embedding models.
"""

import streamlit as st
from llama_index.core import Settings

try:
    from llama_index.llms.ollama import Ollama
    from llama_index.embeddings.ollama import OllamaEmbedding
except ImportError:
    st.error("Missing libraries. Run: pip install llama-index-llms-ollama llama-index-embeddings-ollama")
    st.stop()

from config import MODEL_NAME, EMBED_MODEL_NAME, LLM_TEMPERATURE, LLM_REQUEST_TIMEOUT


@st.cache_resource
def initialize_models():
    """
    Initialize and cache LLM and embedding models.
    
    Returns:
        tuple: (llm, embed_model) - Initialized Ollama LLM and embedding model
    """
    # Initialize LLM with configuration
    # json_mode=False is safer for reasoning; request_timeout prevents hanging
    llm = Ollama(
        model=MODEL_NAME, 
        request_timeout=LLM_REQUEST_TIMEOUT, 
        temperature=LLM_TEMPERATURE
    )
    
    # Initialize embedding model
    embed_model = OllamaEmbedding(model_name=EMBED_MODEL_NAME)
    
    return llm, embed_model


def setup_global_settings():
    """
    Configure global LlamaIndex settings with initialized models.
    
    Returns:
        tuple: (llm, embed_model) - The initialized models
    """
    llm, embed_model = initialize_models()
    Settings.llm = llm
    Settings.embed_model = embed_model
    return llm, embed_model
