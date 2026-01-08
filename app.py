import streamlit as st
import json
import os
from llama_index.core import Document, VectorStoreIndex, Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core.memory import ChatMemoryBuffer

# --- CONFIGURATION (Step 4 Requirements) ---
MODEL_NAME = "llama3.2:3b"  # or "qwen2.5:3b"
EMBED_MODEL_NAME = "nomic-embed-text"
DATA_PATH = "data/profiles.json"

# --- PAGE SETUP ---
st.set_page_config(page_title="Internal Expertise Finder", layout="wide")
st.title("🔍 Internal Expertise Finder (Local RAG)")
st.markdown(f"**Model:** {MODEL_NAME} | **Stack:** LlamaIndex + Chroma + Streamlit")

# --- INITIALIZE MODELS ---
@st.cache_resource
def get_models():
    llm = Ollama(model=MODEL_NAME, request_timeout=300.0)
    embed_model = OllamaEmbedding(model_name=EMBED_MODEL_NAME)
    return llm, embed_model

llm, embed_model = get_models()
Settings.llm = llm
Settings.embed_model = embed_model

# --- DATA INGESTION (Step 5 & 8A1) ---
@st.cache_resource
def load_and_index_data():
    if not os.path.exists(DATA_PATH):
        st.error(f"Data file not found at {DATA_PATH}")
        return None

    with open(DATA_PATH, "r") as f:
        profiles = json.load(f)

    documents = []
    for p in profiles:
        # Robustness: Handle missing fields gracefully
        name = p.get("name", "Unknown")
        title = p.get("title", "N/A")
        team = p.get("team", "General")
        location = p.get("location", "Remote")
        email = p.get("email", "No email")
        
        # Parse Skills
        skills = ", ".join(p.get("skills", []))
        
        # Parse Projects (Robustness for missing projects)
        projects_text = ""
        raw_projects = p.get("projects", [])
        if raw_projects:
            for proj in raw_projects:
                p_name = proj.get("name", "Unnamed Project")
                p_desc = proj.get("desc", "")
                projects_text += f"- Project: {p_name} ({p_desc})\n"
        
        # Parse Bio
        bio = p.get("bio", "") or "No bio provided."

        # Create a text blob for the LLM to read
        text_content = (
            f"Name: {name}\n"
            f"This profile belongs to {name}.\n"  # Explicitly mention the name in the text
            f"Title: {title}\n"
            f"Team: {team}\n"
            f"Location: {location}\n"
            f"Email: {email}\n"
            f"Skills: {skills}\n"
            f"Bio: {bio}\n"
            f"Projects:\n{projects_text}"
        )

        # Create Document with Metadata for filtering
        doc = Document(
            text=text_content,
            metadata={
                "name": name,
                "team": team,
                "location": location,
                "email": email
            }
        )
        documents.append(doc)
    
    # Build Index (In-memory for simplicity, or persist to Chroma if dataset is huge)
    return VectorStoreIndex.from_documents(documents)

index = load_and_index_data()

if not index:
    st.stop()

# --- SIDEBAR FILTERS (Requirement C2) ---
st.sidebar.header("Filters")
# Extract unique locations/teams for the dropdowns
all_docs = index.docstore.docs.values()
locations = sorted(list(set([d.metadata["location"] for d in all_docs])))
teams = sorted(list(set([d.metadata["team"] for d in all_docs])))

selected_location = st.sidebar.selectbox("Location", ["All"] + locations)
selected_team = st.sidebar.selectbox("Team", ["All"] + teams)

# Define filters based on selection
filters = []
if selected_location != "All":
    from llama_index.core.vector_stores import MetadataFilter
    filters.append(MetadataFilter(key="location", value=selected_location))
if selected_team != "All":
    from llama_index.core.vector_stores import MetadataFilter
    filters.append(MetadataFilter(key="team", value=selected_team))

from llama_index.core.vector_stores import MetadataFilters
query_filters = MetadataFilters(filters=filters) if filters else None

# --- CHAT ENGINE SETUP (Requirements 6.1, 6.2, 6.3) ---
# Custom System Prompt to enforce strict output format
SYSTEM_PROMPT = """
You are an Internal Expertise Finder assistant. Your goal is to find the right people for a topic based strictly on the provided context.

RULES:
1. **Grounded Matching:** Only recommend people if the context explicitly supports their expertise. If no strong match is found, state that clearly.
2. **Evidence is Mandatory:** For every recommendation, you MUST provide "Evidence" snippets (direct quotes of skills, projects, or bio) from the context.
3. **Clarification:** If the user query is vague (e.g., "Need help with data"), ask 1-2 clarifying questions.
4. **Format:**
   - **Name** - Title (Team, Location) - Email
   - **Why:** Brief explanation.
   - **Evidence:** [Snippet from context]
   
5. **No Hallucination:** Do not invent skills or people.

Example Output:
**Aditi Shah** — ML Engineer (ML, Bangalore) — aditi.shah@company.com
- **Why:** Strong experience in RAG and vector databases.
- **Evidence:** Project "Expertise Finder" used embeddings + vector database.
- **Evidence:** Skills include "RAG", "Chroma".
"""

# We use the Chat Engine to maintain history
chat_engine = index.as_chat_engine(
    chat_mode="context",
    system_prompt=SYSTEM_PROMPT,
    memory=ChatMemoryBuffer.from_defaults(token_limit=3000),
    filters=query_filters, # Apply the sidebar filters here
    similarity_top_k=3     # Return top 3 matches
)

# --- UI CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi! I can help you find experts within the company. Try asking 'Who knows Redis?' or 'Need an ML expert'."}]

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask about skills, tools, or people..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response
    with st.chat_message("assistant"):
        with st.spinner("Searching employee profiles..."):
            response = chat_engine.chat(prompt)
            st.markdown(response.response)
    
    # Add assistant message to history
    st.session_state.messages.append({"role": "assistant", "content": response.response})

# --- DEBUG / BONUS (Optional) ---
# st.sidebar.markdown("---")
# st.sidebar.subheader("Debug Info")
# if st.sidebar.checkbox("Show Retrieved Nodes"):
#     if 'response' in locals():
#         st.sidebar.json([n.node.get_content() for n in response.source_nodes])