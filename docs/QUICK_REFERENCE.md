# Quick Reference Guide

## 📁 File Organization

```
chatbot/
├── 🎯 Core Application Files
│   ├── app.py                    # Main entry point - run this!
│   ├── config.py                 # All configuration settings
│   ├── models.py                 # LLM & embedding initialization
│   ├── data_processing.py        # JSON → Documents conversion
│   ├── indexing.py               # Vector index management
│   ├── filters.py                # Search filtering logic
│   ├── chat_engine.py            # RAG engine setup
│   └── ui.py                     # Streamlit UI components
│
├── 📊 Data
│   └── data/
│       └── profiles.json         # Employee profiles
│
├── 📚 Documentation
│   └── docs/
│       ├── ARCHITECTURE.md       # System design & architecture
│       ├── FLOW_DIAGRAM.md       # Detailed flow diagrams
│       ├── USER_GUIDE.md         # How to use the app
│       └── REFACTORING_SUMMARY.md # What changed and why
│
└── 📦 Configuration
    ├── requirements.txt          # Python dependencies
    └── README.md                 # Project overview
```

---

## 🚀 Quick Commands

### Start the Application
```bash
streamlit run app.py
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Pull Ollama Models
```bash
ollama pull llama3.2:3b
ollama pull nomic-embed-text
```

---

## 🔍 Where to Look?

### "I want to change the LLM model"
👉 Edit `config.py` → Change `MODEL_NAME`

### "I want to modify the system prompt"
👉 Edit `config.py` → Change `SYSTEM_PROMPT`

### "I want to change how profiles are processed"
👉 Edit `data_processing.py` → Modify `create_document_content()`

### "I want to add a new filter"
👉 Edit `filters.py` → Add filter to `create_sidebar_filters()`

### "I want to change the UI"
👉 Edit `ui.py` → Modify UI functions

### "I want to understand the architecture"
👉 Read `docs/ARCHITECTURE.md`

### "I want to see the data flow"
👉 Read `docs/FLOW_DIAGRAM.md`

### "I need user instructions"
👉 Read `docs/USER_GUIDE.md`

---

## 📊 Module Responsibilities

| Module | "This module handles..." |
|--------|-------------------------|
| **app.py** | "...orchestrating everything and running the app" |
| **config.py** | "...all configuration constants and settings" |
| **models.py** | "...loading and caching the LLM models" |
| **data_processing.py** | "...converting JSON profiles into searchable documents" |
| **indexing.py** | "...creating the vector index for semantic search" |
| **filters.py** | "...sidebar filters and metadata filtering" |
| **chat_engine.py** | "...setting up the RAG chat engine" |
| **ui.py** | "...all Streamlit UI components and interactions" |

---

## 🔄 Data Flow Summary

```
profiles.json 
    ↓ [data_processing.py]
Documents 
    ↓ [indexing.py]
Vector Index 
    ↓ [User Query + filters.py]
Filtered Search 
    ↓ [chat_engine.py]
LLM Response 
    ↓ [ui.py]
Display to User
```

---

## 🎯 Key Functions Reference

### Data Processing
- `load_profiles_from_json()` - Load JSON file
- `convert_profiles_to_documents()` - JSON → Documents
- `create_document_content()` - Format profile text

### Indexing
- `create_vector_index()` - Build cached index
- `get_unique_metadata_values()` - Extract filter options

### Filters
- `create_sidebar_filters()` - Build UI filters
- `build_metadata_filters()` - Convert to filter objects

### Models
- `initialize_models()` - Load LLM & embeddings
- `setup_global_settings()` - Configure LlamaIndex

### Chat Engine
- `create_chat_engine()` - Initialize RAG engine

### UI
- `handle_chat_interaction()` - Process user queries
- `display_debug_context()` - Show retrieved documents

---

## 🐛 Debugging Checklist

### App won't start?
1. ✅ Ollama running? → `ollama list`
2. ✅ Models pulled? → `ollama pull llama3.2:3b`
3. ✅ Dependencies installed? → `pip install -r requirements.txt`
4. ✅ profiles.json exists? → Check `data/profiles.json`

### No results?
1. ✅ Remove filters (set to "All")
2. ✅ Check debug output
3. ✅ Try broader query
4. ✅ Verify data in profiles.json

### Slow performance?
1. ✅ First load is slow (~10s) - normal
2. ✅ Check Ollama is local
3. ✅ Reduce SIMILARITY_TOP_K in config.py

---

## 📈 Performance Expectations

| Operation | Time |
|-----------|------|
| First Load | ~10s |
| Subsequent Queries | 2-5s |
| Filter Change | Instant |
| Model Reload | Never (cached) |
| Index Rebuild | Only on data change |

---

## 🎓 For New Developers

### Day 1: Understanding
1. Read `README.md` (overview)
2. Read `docs/ARCHITECTURE.md` (system design)
3. Skim code in this order: `config.py` → `app.py` → other modules

### Day 2: Running
1. Install dependencies
2. Pull Ollama models
3. Run the app
4. Test with queries from `USER_GUIDE.md`

### Day 3: Modifying
1. Pick a small change (e.g., change a filter label)
2. Find the relevant module
3. Make the change
4. Test it works

---

## 💡 Tips for Extending

### Adding a New Feature
1. Decide which module it belongs to
2. Add function to that module
3. Call from `app.py` if needed
4. Update documentation

### Modifying Existing Behavior
1. Find the relevant function (use Quick Reference above)
2. Read its docstring
3. Make changes
4. Test thoroughly

### Adding a New Data Source
1. Add loader function in `data_processing.py`
2. Convert to Document format
3. Update `create_vector_index()` in `indexing.py`

---

## 📚 Documentation Map

```
README.md
├── What: Project overview
├── Why: Features and benefits
└── How: Quick start

docs/ARCHITECTURE.md
├── System Design
├── Module Structure
├── Data Flow
└── Design Decisions

docs/FLOW_DIAGRAM.md
├── 12 Detailed Diagrams
├── Process Flows
└── End-to-End Examples

docs/USER_GUIDE.md
├── Installation
├── Usage Examples
├── Troubleshooting
└── FAQ

docs/REFACTORING_SUMMARY.md
├── Before/After Comparison
├── What Changed
└── Migration Guide
```

---

## 🔗 Quick Links

- **Start Here**: `README.md`
- **Architecture**: `docs/ARCHITECTURE.md`
- **Flows**: `docs/FLOW_DIAGRAM.md`
- **User Manual**: `docs/USER_GUIDE.md`
- **What Changed**: `docs/REFACTORING_SUMMARY.md`

---

## ✅ Quick Health Check

Run these to verify everything works:

```bash
# Syntax check
python3 -m py_compile *.py

# Start app
streamlit run app.py

# Test query (in browser)
"Find a Python expert"

# Check debug output
Click "Debug: See Retrieved Context" expander
```

If all above work → ✅ You're good to go!

---

**Last Updated**: 2026-01-08  
**Version**: 2.0 (Refactored)
