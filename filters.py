"""
Filters module.
Handles UI filters and metadata filtering for search queries.
"""

import streamlit as st
from llama_index.core.vector_stores import MetadataFilter, MetadataFilters
from llama_index.core import VectorStoreIndex

from indexing import get_unique_metadata_values


def create_sidebar_filters(index: VectorStoreIndex) -> tuple[str, str]:
    """
    Create sidebar filter UI elements.
    
    Args:
        index: VectorStoreIndex instance
        
    Returns:
        tuple: (selected_location, selected_team)
    """
    st.sidebar.header("Filter Results")
    
    # Extract unique values for filters
    locations = get_unique_metadata_values(index, "location")
    teams = get_unique_metadata_values(index, "team")
    
    # Create selectboxes
    selected_location = st.sidebar.selectbox("Location", ["All"] + locations)
    selected_team = st.sidebar.selectbox("Team", ["All"] + teams)
    
    return selected_location, selected_team


def build_metadata_filters(selected_location: str, selected_team: str) -> MetadataFilters | None:
    """
    Build MetadataFilters object based on user selections.
    
    Args:
        selected_location: Selected location from filter
        selected_team: Selected team from filter
        
    Returns:
        MetadataFilters object if filters applied, None otherwise
    """
    filters = []
    
    if selected_location != "All":
        filters.append(MetadataFilter(key="location", value=selected_location))
    
    if selected_team != "All":
        filters.append(MetadataFilter(key="team", value=selected_team))
    
    return MetadataFilters(filters=filters) if filters else None
