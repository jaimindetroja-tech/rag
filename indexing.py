"""
Indexing module.
Handles creation and caching of vector store index.
"""

import streamlit as st
from llama_index.core import VectorStoreIndex

from data_processing import load_profiles_from_json, convert_profiles_to_documents


@st.cache_resource
def create_vector_index():
    """
    Load data and create a cached vector store index.
    
    Returns:
        VectorStoreIndex: Indexed vector store, or None if data loading fails
    """
    try:
        # Load profiles from JSON
        profiles = load_profiles_from_json()
        
        # Convert to documents
        documents = convert_profiles_to_documents(profiles)
        
        # Create and return vector index
        return VectorStoreIndex.from_documents(documents)
        
    except FileNotFoundError as e:
        st.error(str(e))
        return None
    except Exception as e:
        st.error(f"Error creating index: {str(e)}")
        return None


def get_unique_metadata_values(index: VectorStoreIndex, metadata_key: str) -> list[str]:
    """
    Extract unique values for a metadata field across all documents.
    
    Args:
        index: VectorStoreIndex instance
        metadata_key: Metadata field name to extract
        
    Returns:
        Sorted list of unique values
    """
    all_docs = index.docstore.docs.values()
    values = set(d.metadata.get(metadata_key, "Unknown") for d in all_docs)
    return sorted(list(values))
