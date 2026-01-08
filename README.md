# 🔍 Internal Expertise Finder

A powerful RAG-based chatbot for discovering internal expertise, skills, and project information within your organization.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/streamlit-1.28%2B-red)

---

## 🎯 Features

- **🔎 Semantic Search**: Find experts by skills, projects, or domains using natural language
- **💬 Conversational Interface**: Chat-based interaction with context memory
- **🎯 Smart Filtering**: Filter by location and team
- **📊 Project Discovery**: Discover who worked on specific projects and their tech stacks
- **🐛 Debug Mode**: Transparent retrieval to see why specific profiles were selected
- **⚡ Fast & Local**: Uses local Ollama LLMs for privacy and speed

---

## 🏗️ Project Structure

```
chatbot/
├── app.py                    # Main application entry point
├── config.py                 # Configuration and constants
├── models.py                 # LLM and embedding model initialization
├── data_processing.py        # Profile data processing
├── indexing.py               # Vector index creation and management
├── filters.py                # UI filters and metadata filtering
├── chat_engine.py            # Chat engine configuration
├── ui.py                     # Streamlit UI components
├── data/
│   └── profiles.json         # Employee profile data
└── docs/
    ├── ARCHITECTURE.md       # System architecture documentation
    ├── FLOW_DIAGRAM.md       # Detailed flow diagrams
    └── USER_GUIDE.md         # User manual
```

---

## 📦 Installation

### Prerequisites
1. **Python 3.9+**
2. **Ollama** ([Installation Guide](https://ollama.ai/))

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd chatbot
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install streamlit llama-index-core llama-index-llms-ollama llama-index-embeddings-ollama
```

### Step 3: Pull Required Ollama Models
```bash
ollama pull llama3.2:3b
ollama pull nomic-embed-text
```

### Step 4: Prepare Data
Ensure `data/profiles.json` exists with your employee data (see [Data Format](#data-format) below).

---

## 🚀 Usage

### Start the Application
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

### Example Queries
- "Find a Python expert"
- "Who worked on the Payment Gateway project?"
- "Find React developers in Bangalore"
- "Who knows Kubernetes and Docker?"

---

## 📊 Data Format

Your `data/profiles.json` should follow this structure:

```json
[
  {
    "name": "Alice Johnson",
    "title": "Senior Backend Engineer",
    "team": "Backend",
    "location": "Bangalore",
    "email": "alice@company.com",
    "experience_years": 5,
    "skills": ["Python", "FastAPI", "PostgreSQL", "Redis"],
    "domains": ["E-commerce", "Payments"],
    "projects": [
      {
        "name": "Payment Gateway v2",
        "desc": "Redesigned payment processing system",
        "stack": ["Python", "FastAPI", "Redis", "PostgreSQL"]
      }
    ]
  }
]
```

**Required Fields**:
- `name`, `title`, `team`, `location`, `email`

**Optional Fields**:
- `experience_years`, `skills`, `domains`, `projects`

---

## 🏛️ Architecture

### Module Overview

| Module | Purpose |
|--------|---------|
| **config.py** | Centralized configuration (model names, paths, prompts) |
| **models.py** | Initialize and cache LLM/embedding models |
| **data_processing.py** | Convert JSON profiles to LlamaIndex documents |
| **indexing.py** | Create and manage vector store index |
| **filters.py** | Handle UI filters and metadata filtering |
| **chat_engine.py** | Configure RAG chat engine |
| **ui.py** | Streamlit UI components |
| **app.py** | Main orchestrator |

### Technology Stack
- **LlamaIndex**: RAG framework and vector indexing
- **Ollama**: Local LLM inference
- **Streamlit**: Web interface
- **Python**: Core language

### Data Flow
```
User Query → Embed Query → Vector Search → Retrieve Documents 
→ Build Context → LLM Generation → Display Response
```

For detailed architecture, see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

---

## 🔧 Configuration

Edit `config.py` to customize:

```python
# Change models
MODEL_NAME = "llama3.2:3b"
EMBED_MODEL_NAME = "nomic-embed-text"

# Adjust retrieval
SIMILARITY_TOP_K = 5  # Number of results to retrieve

# Modify system prompt
SYSTEM_PROMPT = """..."""
```

---

## 📚 Documentation

Comprehensive documentation is available in the `docs/` folder:

1. **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - System design, module structure, and component interactions
2. **[FLOW_DIAGRAM.md](docs/FLOW_DIAGRAM.md)** - Detailed flow diagrams with mermaid charts
3. **[USER_GUIDE.md](docs/USER_GUIDE.md)** - User manual with examples and troubleshooting

---

## 🧪 Development

### Adding New Features

1. **Add Configuration**: Update `config.py`
2. **Create Function**: Add to appropriate module
3. **Update App Flow**: Modify `app.py` if needed
4. **Document**: Update relevant docs

### Code Style
- Use type hints
- Add docstrings to all functions
- Follow PEP 8 conventions

### Testing
```bash
# Test with sample query
streamlit run app.py
# Then query: "Find a Python expert"
```

---

## 🐛 Troubleshooting

### App Won't Start
```bash
# Check Ollama is running
ollama list

# Verify models are pulled
ollama pull llama3.2:3b
ollama pull nomic-embed-text

# Check dependencies
pip install -r requirements.txt
```

### No Results Found
- Remove filters (set to "All")
- Try broader queries
- Check debug output to see retrieved documents
- Verify `profiles.json` has relevant data

### Slow Performance
- First load takes ~10s (model initialization)
- Subsequent queries should be <5s
- Check Ollama is running locally

---

## 📈 Performance

| Metric | Value |
|--------|-------|
| Initial Load | ~10s |
| Query Time | 2-5s |
| Index Size | ~1MB per 100 profiles |
| Memory Usage | ~2GB (models loaded) |
| Concurrent Users | 1 (Streamlit limitation) |

---

## 🛣️ Roadmap

- [ ] Persistent vector store (ChromaDB/Qdrant)
- [ ] Advanced filtering (skills, experience range)
- [ ] Multi-user support
- [ ] Resume/document upload
- [ ] Analytics dashboard
- [ ] Export results
- [ ] API endpoints

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests if applicable
4. Update documentation
5. Submit a pull request

---

## 📄 License

MIT License - see LICENSE file for details

---

## 🙏 Acknowledgments

- **LlamaIndex**: RAG framework
- **Ollama**: Local LLM serving
- **Streamlit**: Web UI framework
- **Nomic AI**: Embedding model

---

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

## 🔗 Useful Links

- [LlamaIndex Documentation](https://docs.llamaindex.ai/)
- [Ollama Documentation](https://ollama.ai/docs)
- [Streamlit Documentation](https://docs.streamlit.io/)

---

**Made with ❤️ for better internal knowledge discovery**
