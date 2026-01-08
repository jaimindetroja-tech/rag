"""
Data processing module.
Handles loading profiles from JSON and converting them to LlamaIndex documents.
"""

import json
import os
from typing import List, Dict, Any
from llama_index.core import Document

from config import DATA_PATH


def load_profiles_from_json(file_path: str = DATA_PATH) -> List[Dict[str, Any]]:
    """
    Load employee profiles from JSON file.
    
    Args:
        file_path: Path to the profiles JSON file
        
    Returns:
        List of profile dictionaries
        
    Raises:
        FileNotFoundError: If the JSON file doesn't exist
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(file_path, "r") as f:
        profiles = json.load(f)
    
    return profiles


def extract_project_information(projects: List[Dict[str, Any]]) -> tuple[List[str], List[str], List[str]]:
    """
    Extract structured information from project data.
    
    Args:
        projects: List of project dictionaries
        
    Returns:
        tuple: (project_details, project_names, project_stacks)
            - project_details: Formatted project descriptions for LLM
            - project_names: List of project names
            - project_stacks: List of all technologies used across projects
    """
    project_details = []
    project_names = []
    project_stacks = []
    
    if not projects:
        return project_details, project_names, project_stacks
    
    for proj in projects:
        p_name = proj.get("name", "Unnamed Project")
        p_desc = proj.get("desc", "")
        p_stack = ", ".join(proj.get("stack", []))
        
        # Collect for metadata/keywords
        project_names.append(p_name)
        project_stacks.extend(proj.get("stack", []))
        
        # Format for LLM reading
        project_details.append(
            f"  * PROJECT: {p_name}\n"
            f"    - Description: {p_desc}\n"
            f"    - Tech Stack: {p_stack}"
        )
    
    return project_details, project_names, project_stacks


def create_document_content(profile: Dict[str, Any]) -> tuple[str, Dict[str, Any]]:
    """
    Create document content and metadata from a profile.
    
    Args:
        profile: Employee profile dictionary
        
    Returns:
        tuple: (text_content, metadata) - Formatted text and metadata dict
    """
    # 1. Safe Extraction of basic fields
    name = profile.get("name", "Unknown")
    title = profile.get("title", "N/A")
    team = profile.get("team", "General")
    location = profile.get("location", "Remote")
    email = profile.get("email", "N/A")
    exp = profile.get("experience_years", 0)
    
    # 2. List Processing for skills and domains
    skills = ", ".join(profile.get("skills", []))
    domains = ", ".join(profile.get("domains", []))
    
    # 3. Deep Project Parsing
    raw_projects = profile.get("projects", [])
    project_details, project_names, project_stacks = extract_project_information(raw_projects)
    
    projects_text = "\n".join(project_details) if project_details else "No projects listed."
    
    # 4. Keyword Stuffing for better vector retrieval
    # Explicitly list keywords to boost retrieval matching
    all_keywords = f"{name}, {team}, {skills}, {domains}, {', '.join(project_names)}, {', '.join(project_stacks)}"
    
    # 5. Final Text Blob for embedding
    # We use delimiters to help the LLM strictly separate this profile from others in the context window
    text_content = (
        f"<<< PROFILE START >>>\n"
        f"Employee Name: {name}\n"
        f"Role: {title} ({team})\n"
        f"Location: {location}\n"
        f"Email: {email}\n"
        f"Experience: {exp} years\n"
        f"Skills: {skills}\n"
        f"Domains: {domains}\n"
        f"Projects:\n{projects_text}\n"
        f"--- Search Keywords ---\n{all_keywords}\n"
        f"<<< PROFILE END >>>"
    )
    
    # 6. Metadata for filtering and debugging
    metadata = {
        "name": name,
        "team": team,
        "location": location,
        "project_names": ", ".join(project_names)
    }
    
    return text_content, metadata


def convert_profiles_to_documents(profiles: List[Dict[str, Any]]) -> List[Document]:
    """
    Convert employee profiles to LlamaIndex Document objects.
    
    Args:
        profiles: List of employee profile dictionaries
        
    Returns:
        List of LlamaIndex Document objects
    """
    documents = []
    
    for profile in profiles:
        text_content, metadata = create_document_content(profile)
        
        doc = Document(
            text=text_content,
            metadata=metadata
        )
        documents.append(doc)
    
    return documents
