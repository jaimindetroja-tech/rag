"""
Chat engine module.
Handles creation and configuration of the chat engine.
"""

from llama_index.core import VectorStoreIndex
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.vector_stores import MetadataFilters

from config import SYSTEM_PROMPT, CHAT_MEMORY_TOKEN_LIMIT, SIMILARITY_TOP_K


def create_chat_engine(index: VectorStoreIndex, filters: MetadataFilters | None = None):
    """
    Create a chat engine with context mode and memory.
    
    Args:
        index: VectorStoreIndex instance
        filters: Optional metadata filters for search
        
    Returns:
        Chat engine instance configured for context-based chat
    """
    chat_engine = index.as_chat_engine(
        chat_mode="context",
        system_prompt=SYSTEM_PROMPT,
        memory=ChatMemoryBuffer.from_defaults(token_limit=CHAT_MEMORY_TOKEN_LIMIT),
        filters=filters,
        similarity_top_k=SIMILARITY_TOP_K  # Retrieve more results for better coverage
    )
    
    return chat_engine
