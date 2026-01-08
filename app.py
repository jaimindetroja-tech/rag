import streamlit as st
import json
import os
from llama_index.core import Document, VectorStoreIndex, Settings
from llama_index.core.memory import ChatMemoryBuffer

# --- LIBRARY CHECKS ---
try:
    from llama_index.llms.ollama import Ollama
    from llama_index.embeddings.ollama import OllamaEmbedding
except ImportError:
    st.error("Missing libraries. Run: pip install llama-index-llms-ollama llama-index-embeddings-ollama")
    st.stop()

# --- CONFIGURATION ---
MODEL_NAME = "llama3.2:3b"      # Ensure this model is pulled in Ollama
EMBED_MODEL_NAME = "nomic-embed-text" # Ensure this is pulled: `ollama pull nomic-embed-text`
DATA_PATH = "data/profiles.json"

# --- PAGE CONFIG ---
st.set_page_config(page_title="Internal Expertise Finder", layout="wide")
st.title("🔍 Internal Expertise Finder")
st.caption(f"Powered by {MODEL_NAME} & {EMBED_MODEL_NAME}")

# --- INIT MODELS ---
@st.cache_resource
def get_models():
    # json_mode=False is safer for reasoning; request_timeout prevents hanging
    llm = Ollama(model=MODEL_NAME, request_timeout=300.0, temperature=0.1)
    embed_model = OllamaEmbedding(model_name=EMBED_MODEL_NAME)
    return llm, embed_model

llm, embed_model = get_models()
Settings.llm = llm
Settings.embed_model = embed_model

# --- OPTIMIZED DATA INGESTION ---
@st.cache_resource
def load_and_index_data():
    if not os.path.exists(DATA_PATH):
        st.error(f"File not found: {DATA_PATH}")
        return None

    with open(DATA_PATH, "r") as f:
        profiles = json.load(f)

    documents = []
    for p in profiles:
        # 1. Safe Extraction
        name = p.get("name", "Unknown")
        title = p.get("title", "N/A")
        team = p.get("team", "General")
        location = p.get("location", "Remote")
        email = p.get("email", "N/A")
        exp = p.get("experience_years", 0)
        
        # 2. List Processing
        skills = ", ".join(p.get("skills", []))
        domains = ", ".join(p.get("domains", []))
        
        # 3. Deep Project Parsing (Crucial for your error)
        project_details = []
        project_names = []
        project_stacks = []
        
        raw_projects = p.get("projects", [])
        if raw_projects:
            for proj in raw_projects:
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
        
        projects_text = "\n".join(project_details) if project_details else "No projects listed."
        
        # 4. Keyword Stuffing (Optimisation)
        # We explicitly list keywords at the bottom to boost vector retrieval matching
        all_keywords = f"{name}, {team}, {skills}, {domains}, {', '.join(project_names)}, {', '.join(project_stacks)}"

        # 5. Final Text Blob
        text_content = (
            f"Employee Name: {name}\n"
            f"Role: {title} ({team})\n"
            f"Location: {location}\n"
            f"Email: {email}\n"
            f"Experience: {exp} years\n"
            f"Skills: {skills}\n"
            f"Domains: {domains}\n"
            f"Projects:\n{projects_text}\n"
            f"--- Search Keywords ---\n{all_keywords}"
        )

        # 6. Metadata (Helps debugging and potential filtering)
        doc = Document(
            text=text_content,
            metadata={
                "name": name,
                "team": team,
                "location": location,
                "project_names": ", ".join(project_names) # Store project names in metadata
            }
        )
        documents.append(doc)
    
    return VectorStoreIndex.from_documents(documents)

index = load_and_index_data()

if not index:
    st.stop()

# --- SIDEBAR FILTERS ---
st.sidebar.header("Filter Results")
all_docs = index.docstore.docs.values()

# Robust set generation
locations = sorted(list(set(d.metadata.get("location", "Unknown") for d in all_docs)))
teams = sorted(list(set(d.metadata.get("team", "Unknown") for d in all_docs)))

sel_loc = st.sidebar.selectbox("Location", ["All"] + locations)
sel_team = st.sidebar.selectbox("Team", ["All"] + teams)

# Apply filters
filters = []
if sel_loc != "All":
    from llama_index.core.vector_stores import MetadataFilter
    filters.append(MetadataFilter(key="location", value=sel_loc))
if sel_team != "All":
    from llama_index.core.vector_stores import MetadataFilter
    filters.append(MetadataFilter(key="team", value=sel_team))

from llama_index.core.vector_stores import MetadataFilters
query_filters = MetadataFilters(filters=filters) if filters else None

# --- CHAT ENGINE ---
# Optimized Prompt for "Project Details" requests
SYSTEM_PROMPT = """
You are an expert HR & Tech Assistant. You have access to employee profiles, skills, and project history.

YOUR GOAL:
Answer queries about who knows what, or specific details about projects.

STRICT RULES:
1. **Context First:** Only answer based on the retrieved context below. If the info isn't there, say "I couldn't find that information."
2. **Project Queries:** If the user asks about a specific project (e.g., "Expertise Finder"), look for "PROJECT:" in the text and summarize the Description and Tech Stack.
3. **Format:**
   - **Name** (Role, Team)
   - **Relevance:** Why you selected them.
   - **Evidence:** Direct quote of the Skill or Project Name.

Example Query: "Tell me about Expertise Finder"
Example Answer:
"Found 2 people working on 'Expertise Finder':
1. **Rohan Iyer** (Data Engineer)
   - **Role:** Implemented search using embeddings.
   - **Stack:** RAG, LlamaIndex, Chroma.
2. **Divya Singh** (Backend Engineer)
   - **Role:** Worked on citations and grounded answers.
   - **Stack:** Embeddings, RAG."
"""

chat_engine = index.as_chat_engine(
    chat_mode="context",
    system_prompt=SYSTEM_PROMPT,
    memory=ChatMemoryBuffer.from_defaults(token_limit=4000),
    filters=query_filters,
    similarity_top_k=5  # Increased to 5 to catch more project members
)

# --- UI ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Ready to search profiles. Try 'Who worked on Expertise Finder?' or 'Find a Node.js expert'."}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Query employee database..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching..."):
            response = chat_engine.chat(prompt)
            st.markdown(response.response)
            
            # --- DEBUGGING SECTION ---
            # This helps you see if the retrieval actually found the project
            with st.expander("🔍 Debug: See Retrieved Context"):
                for node in response.source_nodes:
                    st.text(f"--- From Profile: {node.metadata.get('name')} ---")
                    # Show first 300 chars to verify project presence
                    st.text(node.node.get_content()[:300] + "...") 
    
    st.session_state.messages.append({"role": "assistant", "content": response.response})
    