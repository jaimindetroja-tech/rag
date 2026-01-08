# Internal Expertise Finder - Architecture Documentation

## 📋 Table of Contents
1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Module Structure](#module-structure)
4. [Data Flow](#data-flow)
5. [Component Interactions](#component-interactions)

---

## Overview

The Internal Expertise Finder is a **RAG (Retrieval-Augmented Generation)** based chatbot that helps users discover internal expertise, skills, and project information within an organization. It uses **LlamaIndex** for document indexing and retrieval, **Ollama** for local LLM inference, and **Streamlit** for the web interface.

### Key Features
- 🔍 Semantic search across employee profiles
- 📊 Project and skill-based expertise discovery
- 🎯 Location and team-based filtering
- 💬 Context-aware chat interface
- 🐛 Debug mode to inspect retrieved context

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Streamlit Web UI                         │
│                       (ui.py)                                │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ├──► User Input & Chat Interface
                   │
┌──────────────────▼──────────────────────────────────────────┐
│                   Application Core                           │
│                     (app.py)                                 │
│  ┌────────────┐  ┌─────────────┐  ┌──────────────┐         │
│  │  Models    │  │  Indexing   │  │  Chat Engine │         │
│  │ (models.py)│  │(indexing.py)│  │(chat_engine. │         │
│  └────────────┘  └─────────────┘  │    py)       │         │
│                                    └──────────────┘         │
└──────────────────┬──────────────────────────────────────────┘
                   │
    ┌──────────────┼──────────────┐
    │              │              │
    ▼              ▼              ▼
┌────────┐  ┌────────────┐  ┌──────────┐
│ Config │  │    Data    │  │ Filters  │
│(.py)   │  │ Processing │  │(.py)     │
│        │  │   (.py)    │  │          │
└────────┘  └────────────┘  └──────────┘
                   │
                   ▼
         ┌──────────────────┐
         │  Employee Data   │
         │  profiles.json   │
         └──────────────────┘
```

---

## Module Structure

The application is organized into 8 focused modules:

### 1. **config.py** - Configuration Module
**Purpose**: Centralized configuration management

**Contents**:
- Model names (LLM and embedding)
- File paths
- LLM parameters (temperature, timeout)
- Chat engine settings
- System prompt template

**Key Constants**:
```python
MODEL_NAME = "llama3.2:3b"
EMBED_MODEL_NAME = "nomic-embed-text"
DATA_PATH = "data/profiles.json"
SIMILARITY_TOP_K = 5
```

---

### 2. **models.py** - Model Initialization
**Purpose**: Initialize and configure LLM and embedding models

**Key Functions**:
- `initialize_models()`: Creates cached LLM and embedding instances
- `setup_global_settings()`: Configures LlamaIndex global settings

**Caching**: Uses `@st.cache_resource` to prevent model reloading

**Dependencies**: Ollama (local LLM server)

---

### 3. **data_processing.py** - Data Processing
**Purpose**: Transform raw JSON profiles into searchable documents

**Key Functions**:

| Function | Input | Output | Purpose |
|---------|-------|--------|---------|
| `load_profiles_from_json()` | File path | List of profiles | Load JSON data |
| `extract_project_information()` | Project list | Project details, names, stacks | Parse project data |
| `create_document_content()` | Profile dict | Text content + metadata | Format for embedding |
| `convert_profiles_to_documents()` | Profiles list | LlamaIndex Documents | Final document creation |

**Document Structure**:
```
Employee Name: [name]
Role: [title] ([team])
Location: [location]
Email: [email]
Experience: [years] years
Skills: [comma-separated skills]
Domains: [comma-separated domains]
Projects:
  * PROJECT: [name]
    - Description: [desc]
    - Tech Stack: [stack]
--- Search Keywords ---
[Keyword stuffing for better retrieval]
```

---

### 4. **indexing.py** - Vector Indexing
**Purpose**: Create and manage vector store index

**Key Functions**:
- `create_vector_index()`: Builds cached vector index from documents
- `get_unique_metadata_values()`: Extracts unique metadata field values

**Technology**: Uses LlamaIndex's `VectorStoreIndex` for in-memory vector storage

**Caching**: Index is cached to avoid re-indexing on every interaction

---

### 5. **filters.py** - Filtering Logic
**Purpose**: Handle UI filters and metadata-based search filtering

**Key Functions**:
- `create_sidebar_filters()`: Creates Streamlit sidebar filter UI
- `build_metadata_filters()`: Converts UI selections to LlamaIndex filters

**Supported Filters**:
- Location (e.g., "Bangalore", "Remote")
- Team (e.g., "Backend", "Data")

---

### 6. **chat_engine.py** - Chat Engine Configuration
**Purpose**: Configure RAG-based chat engine

**Key Function**:
- `create_chat_engine()`: Initializes chat engine with:
  - Context mode (retrieval + generation)
  - System prompt
  - Chat memory buffer
  - Metadata filters
  - Top-K similarity search

**Chat Mode**: Uses "context" mode for RAG pattern

---

### 7. **ui.py** - User Interface
**Purpose**: Streamlit UI components and chat interaction

**Key Functions**:
- `setup_page_config()`: Configure Streamlit page
- `display_header()`: Show app title and caption
- `initialize_chat_session()`: Setup session state
- `display_chat_history()`: Render message history
- `handle_chat_interaction()`: Process user input and responses
- `display_debug_context()`: Show retrieved source documents

**Session State**: Maintains chat history across interactions

---

### 8. **app.py** - Main Application
**Purpose**: Orchestrate all modules and manage application flow

**Execution Flow**:
```python
1. Setup page config
2. Display header
3. Initialize models
4. Create vector index
5. Create sidebar filters
6. Build metadata filters
7. Create chat engine
8. Initialize chat session
9. Display chat history
10. Handle user interactions
```

---

## Data Flow

### 1. **Initialization Phase**
```
User starts app
    ↓
Load Config
    ↓
Initialize Models (LLM + Embeddings)
    ↓
Load profiles.json
    ↓
Convert to Documents (text + metadata)
    ↓
Create Vector Index (embeddings stored)
    ↓
Index cached in memory
```

### 2. **Query Phase**
```
User enters query
    ↓
Apply filters (location, team)
    ↓
Embed query using embedding model
    ↓
Retrieve top-K similar documents from index
    ↓
Construct context from retrieved documents
    ↓
Generate response using LLM + context
    ↓
Display response + debug info
```

---

## Component Interactions

### RAG Pipeline
```
┌─────────────┐
│ User Query  │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│ Embed Query     │  ← Embedding Model
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ Vector Search   │  ← Vector Index
│ (Top-K)         │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ Retrieved Docs  │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ Build Context   │  ← System Prompt + Retrieved Text
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ LLM Generation  │  ← LLM Model
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ Final Response  │
└─────────────────┘
```

### Caching Strategy
- **Models**: Cached via `@st.cache_resource` (persists across runs)
- **Index**: Cached via `@st.cache_resource` (rebuilt only on data change)
- **Chat History**: Stored in `st.session_state` (per session)

---

## Key Design Decisions

### 1. **Modular Architecture**
- **Why**: Easier testing, maintenance, and extensibility
- **Benefit**: Each module has a single responsibility

### 2. **Keyword Stuffing in Documents**
- **Why**: Improves vector retrieval accuracy
- **How**: Append all searchable keywords at document end

### 3. **Project-Focused Formatting**
- **Why**: Users often search by project name or tech stack
- **How**: Clear "PROJECT:" markers in document text

### 4. **Top-K = 5**
- **Why**: Balance between context quality and token limits
- **Benefit**: Catches more relevant profiles for complex queries

### 5. **Debug Mode**
- **Why**: Transparency in retrieval results
- **Benefit**: Users can verify why specific profiles were selected

---

## Performance Considerations

| Aspect | Strategy | Impact |
|--------|----------|--------|
| Model Loading | Cache with `@st.cache_resource` | Instant subsequent loads |
| Index Creation | Cache vector index | Sub-second query times |
| Embedding | Local Ollama server | No API latency |
| Memory | In-memory vector store | Fast retrieval, limited scalability |

---

## Future Enhancements

1. **Persistent Vector Store**: Use ChromaDB or Qdrant for larger datasets
2. **Advanced Filters**: Skills-based, experience range filters
3. **Multi-modal Search**: Add resume/document upload
4. **Analytics**: Track popular queries and missing expertise
5. **Feedback Loop**: Allow users to rate response relevance

---

## Dependencies

```
streamlit >= 1.28.0
llama-index-core >= 0.10.0
llama-index-llms-ollama >= 0.1.0
llama-index-embeddings-ollama >= 0.1.0
```

External:
- **Ollama** running locally with models:
  - `llama3.2:3b`
  - `nomic-embed-text`
