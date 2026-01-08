# Internal Expertise Finder - Flow Diagrams

## 📊 Complete Application Flow

This document provides detailed flow diagrams for understanding the application logic.

---

## 1. Application Startup Flow

```mermaid
graph TD
    A[User Starts App] --> B[app.py: main()]
    B --> C[ui.setup_page_config]
    C --> D[ui.display_header]
    D --> E[models.setup_global_settings]
    E --> F{Models Cached?}
    F -->|No| G[Initialize LLM & Embeddings]
    F -->|Yes| H[Load from Cache]
    G --> I[Set Global Settings]
    H --> I
    I --> J[indexing.create_vector_index]
    J --> K{Index Cached?}
    K -->|No| L[Load Profiles from JSON]
    K -->|Yes| M[Load from Cache]
    L --> N[Convert to Documents]
    N --> O[Create Vector Index]
    O --> P[Cache Index]
    M --> P
    P --> Q[filters.create_sidebar_filters]
    Q --> R[User Selects Filters]
    R --> S[filters.build_metadata_filters]
    S --> T[chat_engine.create_chat_engine]
    T --> U[ui.initialize_chat_session]
    U --> V[ui.display_chat_history]
    V --> W[Ready for User Input]
```

---

## 2. Data Processing Pipeline

```mermaid
graph LR
    A[profiles.json] --> B[load_profiles_from_json]
    B --> C[List of Profile Dicts]
    C --> D[convert_profiles_to_documents]
    D --> E[For Each Profile]
    E --> F[create_document_content]
    F --> G[Extract Basic Fields]
    G --> H[extract_project_information]
    H --> I[Format Document Text]
    I --> J[Build Metadata Dict]
    J --> K[Create LlamaIndex Document]
    K --> L[Append to Documents List]
    L --> M{More Profiles?}
    M -->|Yes| E
    M -->|No| N[Return Documents List]
    N --> O[VectorStoreIndex.from_documents]
```

---

## 3. Query Processing Flow

```mermaid
graph TD
    A[User Enters Query] --> B[ui.handle_chat_interaction]
    B --> C[Add to Session History]
    C --> D[Display User Message]
    D --> E[chat_engine.chat Query]
    E --> F[Apply Metadata Filters]
    F --> G[Embed Query Text]
    G --> H[Vector Similarity Search]
    H --> I[Retrieve Top-K Documents]
    I --> J[Build Context String]
    J --> K[Construct LLM Prompt]
    K --> L[System Prompt + Context + Query]
    L --> M[LLM Generates Response]
    M --> N[Return Response Object]
    N --> O[Display Response]
    O --> P[display_debug_context]
    P --> Q[Show Retrieved Profiles]
    Q --> R[Add to Session History]
```

---

## 4. Document Creation Logic

```mermaid
graph TD
    A[Single Profile Dict] --> B[Extract: name, title, team, etc.]
    B --> C[Extract: skills, domains]
    C --> D[Extract: projects array]
    D --> E{Has Projects?}
    E -->|Yes| F[For Each Project]
    E -->|No| G[projects_text = 'No projects']
    F --> H[Extract: name, desc, stack]
    H --> I[Format Project Block]
    I --> J[Collect Project Names]
    J --> K[Collect Tech Stacks]
    K --> L{More Projects?}
    L -->|Yes| F
    L -->|No| M[Join All Project Blocks]
    M --> N[Build Keyword String]
    G --> N
    N --> O[Create Final Text Content]
    O --> P[Create Metadata Dict]
    P --> Q[Return text, metadata]
```

**Final Document Format**:
```
Employee Name: Alice Johnson
Role: Senior Backend Engineer (Backend Team)
Location: Bangalore
Email: alice@company.com
Experience: 5 years
Skills: Python, Node.js, PostgreSQL
Domains: E-commerce, Payments
Projects:
  * PROJECT: Payment Gateway v2
    - Description: Redesigned payment processing
    - Tech Stack: Python, FastAPI, Redis
  * PROJECT: Order Management System
    - Description: Built scalable order processing
    - Tech Stack: Node.js, MongoDB, Kafka
--- Search Keywords ---
Alice Johnson, Backend Team, Python, Node.js, E-commerce, Payment Gateway v2, Order Management System, FastAPI, Redis, MongoDB
```

---

## 5. Vector Search Process

```mermaid
graph LR
    A[User Query] --> B[Embedding Model]
    B --> C[Query Vector 768d]
    C --> D[Vector Index]
    D --> E{For Each Document}
    E --> F[Calculate Cosine Similarity]
    F --> G[Score Document]
    G --> H{More Docs?}
    H -->|Yes| E
    H -->|No| I[Sort by Score DESC]
    I --> J[Select Top 5 Documents]
    J --> K[Apply Metadata Filters]
    K --> L{Filter Match?}
    L -->|Yes| M[Include Document]
    L -->|No| N[Exclude Document]
    M --> O[Return Filtered Results]
    N --> O
```

---

## 6. Filter Application Logic

```mermaid
graph TD
    A[User Selects Filters] --> B{Location != 'All'?}
    B -->|Yes| C[Add Location Filter]
    B -->|No| D{Team != 'All'?}
    C --> D
    D -->|Yes| E[Add Team Filter]
    D -->|No| F{Any Filters?}
    E --> F
    F -->|Yes| G[Create MetadataFilters Object]
    F -->|No| H[filters = None]
    G --> I[Pass to Chat Engine]
    H --> I
    I --> J[Vector Search]
    J --> K{For Each Retrieved Doc}
    K --> L{Filters Applied?}
    L -->|No| M[Include All Results]
    L -->|Yes| N{Doc Matches Filters?}
    N -->|Yes| O[Include Document]
    N -->|No| P[Exclude Document]
    M --> Q[Final Result Set]
    O --> Q
    P --> K
```

---

## 7. Chat Memory Management

```mermaid
graph LR
    A[User Query 1] --> B[Chat Engine]
    B --> C[Response 1]
    C --> D[Store in Memory Buffer]
    D --> E[User Query 2]
    E --> F[Retrieve Recent Context]
    F --> G[Previous Q&A + New Query]
    G --> H[Vector Search]
    H --> I[LLM Generation with History]
    I --> J[Response 2]
    J --> K{Token Limit Exceeded?}
    K -->|Yes| L[Truncate Oldest Messages]
    K -->|No| M[Append to Memory]
    L --> M
```

**Memory Configuration**:
- Token Limit: 4000 tokens
- Type: ChatMemoryBuffer
- Truncation: FIFO (oldest messages dropped first)

---

## 8. Error Handling Flow

```mermaid
graph TD
    A[Application Start] --> B{profiles.json Exists?}
    B -->|No| C[Display Error: File Not Found]
    B -->|Yes| D{Valid JSON?}
    C --> E[st.stop]
    D -->|No| F[Display Error: Invalid JSON]
    D -->|Yes| G{Ollama Libraries Installed?}
    F --> E
    G -->|No| H[Display Error: Missing Libraries]
    G -->|Yes| I{Ollama Models Available?}
    H --> E
    I -->|No| J[Display Warning: Pull Models]
    I -->|Yes| K[Continue Normal Flow]
    J --> K
    K --> L{Index Creation Success?}
    L -->|No| M[Display Error: Index Failed]
    L -->|Yes| N[App Ready]
    M --> E
```

---

## 9. Module Dependency Graph

```mermaid
graph TD
    A[app.py] --> B[config.py]
    A --> C[models.py]
    A --> D[indexing.py]
    A --> E[filters.py]
    A --> F[chat_engine.py]
    A --> G[ui.py]
    
    C --> B
    
    D --> H[data_processing.py]
    H --> B
    
    E --> D
    
    F --> B
    
    G --> B
    
    style A fill:#ff9999
    style B fill:#99ccff
    style C fill:#99ff99
    style D fill:#99ff99
    style E fill:#99ff99
    style F fill:#99ff99
    style G fill:#99ff99
    style H fill:#99ff99
```

**Legend**:
- 🔴 Main Entry Point (app.py)
- 🔵 Configuration (config.py)
- 🟢 Functional Modules

---

## 10. Session State Management

```mermaid
graph LR
    A[First Page Load] --> B{st.session_state.messages exists?}
    B -->|No| C[Initialize with Welcome Message]
    B -->|Yes| D[Load Existing Messages]
    C --> E[Display Messages]
    D --> E
    E --> F[User Inputs Query]
    F --> G[Append User Message]
    G --> H[Generate Response]
    H --> I[Append Assistant Message]
    I --> J[Re-render Chat History]
    J --> K[Wait for Next Input]
    K --> F
```

**Session State Structure**:
```python
st.session_state.messages = [
    {"role": "assistant", "content": "Welcome message"},
    {"role": "user", "content": "User query 1"},
    {"role": "assistant", "content": "Response 1"},
    # ... more messages
]
```

---

## 11. Caching Strategy

```mermaid
graph TD
    A[Function Called] --> B{@st.cache_resource?}
    B -->|Yes| C{Cached Result Exists?}
    B -->|No| D[Execute Function]
    C -->|Yes| E[Return Cached Result]
    C -->|No| F[Execute Function]
    F --> G[Store in Cache]
    G --> H[Return Result]
    E --> I[Fast Response]
    D --> J[Normal Execution]
    H --> I
```

**Cached Functions**:
1. `models.initialize_models()` - LLM & embedding models
2. `indexing.create_vector_index()` - Vector index

**Cache Invalidation**:
- Models: Never (unless Streamlit cache cleared)
- Index: When `profiles.json` file changes

---

## 12. End-to-End Example: Finding a Python Expert

```mermaid
sequenceDiagram
    participant U as User
    participant UI as ui.py
    participant CE as chat_engine.py
    participant IDX as indexing.py
    participant LLM as Ollama LLM
    
    U->>UI: Types "Find a Python expert"
    UI->>CE: chat_engine.chat(query)
    CE->>IDX: Embed & search index
    IDX-->>CE: Top 5 matching profiles
    Note over CE: Profiles with "Python" in skills
    CE->>LLM: System prompt + context + query
    LLM-->>CE: Generated response
    CE-->>UI: Response + source nodes
    UI->>U: Display response
    UI->>U: Show debug: Retrieved profiles
```

**Retrieved Context Example**:
```
Employee Name: Alice Johnson
Skills: Python, Django, FastAPI
Projects: Payment Gateway (Python, FastAPI)

Employee Name: Bob Smith
Skills: Python, Data Science, TensorFlow
Projects: ML Model Pipeline (Python, TensorFlow)
```

**LLM Response**:
```
Found 2 Python experts:

1. **Alice Johnson** (Senior Backend Engineer)
   - **Expertise**: Python, Django, FastAPI
   - **Relevant Project**: Payment Gateway using FastAPI
   - **Experience**: 5 years

2. **Bob Smith** (Data Scientist)
   - **Expertise**: Python, Data Science, TensorFlow
   - **Relevant Project**: ML Model Pipeline
   - **Experience**: 4 years
```

---

## Summary of Key Flows

| Flow | Trigger | Duration | Cached? |
|------|---------|----------|---------|
| App Startup | User opens app | ~5-10s first time | Yes (after first run) |
| Data Loading | Startup | ~1-2s | Yes |
| Index Creation | Startup | ~2-3s | Yes |
| Query Processing | User input | ~2-5s | No |
| Filter Change | User selection | Instant | No |
| Model Loading | Startup | ~3-5s | Yes |

---

## Performance Optimization Points

1. **Model Caching**: Prevents re-loading 1GB+ models
2. **Index Caching**: Avoids re-embedding all documents
3. **Top-K Limitation**: Limits LLM context size
4. **Metadata Filtering**: Reduces search space
5. **Local LLM**: No API latency
