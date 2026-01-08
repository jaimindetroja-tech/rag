# Internal Expertise Finder - User Guide

## 🚀 Quick Start

### Prerequisites
1. **Ollama** installed and running
2. Required models pulled:
   ```bash
   ollama pull llama3.2:3b
   ollama pull nomic-embed-text
   ```
3. Python 3.9+ installed
4. Dependencies installed:
   ```bash
   pip install streamlit llama-index-core llama-index-llms-ollama llama-index-embeddings-ollama
   ```

### Running the Application
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 📖 How to Use

### Basic Search
Simply type your query in the chat input:

**Example Queries**:
- "Find a Python expert"
- "Who knows React?"
- "Who worked on the Payment Gateway project?"
- "Find someone with experience in machine learning"
- "Who is in the Backend team?"

### Using Filters

**Location Filter**:
- Select a specific location to narrow results
- Example: Select "Bangalore" to find local experts

**Team Filter**:
- Select a specific team
- Example: Select "Backend" to find backend engineers

**Combining Filters**:
- Apply both location and team filters together
- Example: "Bangalore + Backend" only shows backend engineers in Bangalore

### Understanding Responses

**Response Format**:
```
Found X relevant people:

1. **Name** (Role, Team)
   - **Expertise**: Skills
   - **Relevant Project**: Project name and tech stack
   - **Experience**: Years
   - **Contact**: Email

2. **Name** (Role, Team)
   ...
```

### Debug Mode

Click the **"🔍 Debug: See Retrieved Context"** expander to view:
- Which profiles were retrieved
- The actual document content used by the LLM
- Why specific people were selected

---

## 💡 Tips for Better Results

### 1. Be Specific
- ❌ "Find someone"
- ✅ "Find a Python expert with FastAPI experience"

### 2. Use Project Names
- ❌ "Who built payment systems?"
- ✅ "Who worked on the Payment Gateway project?"

### 3. Combine Skills
- "Find someone who knows both Python and React"
- "Who has experience with machine learning and cloud deployment?"

### 4. Ask About Tech Stacks
- "Who has used Kafka?"
- "Find someone with Kubernetes experience"

### 5. Use Context from Previous Messages
The chat remembers your conversation:
```
You: "Find Python experts"
Bot: [Lists 3 people]
You: "Tell me more about their projects"
Bot: [Provides project details for the 3 people]
```

---

## 🎯 Common Use Cases

### 1. Finding Experts for a New Project
**Scenario**: Need someone who knows GraphQL and PostgreSQL

**Query**: "Find someone with GraphQL and PostgreSQL experience"

**Expected Result**: List of people with both skills, showing relevant projects

---

### 2. Discovering Project Contributors
**Scenario**: Want to know who worked on a specific project

**Query**: "Who worked on the Order Management System?"

**Expected Result**: Team members with their roles and contributions

---

### 3. Building a Team
**Scenario**: Need to form a frontend team in Mumbai

**Steps**:
1. Select "Mumbai" in Location filter
2. Query: "Find React and TypeScript experts"
3. Review results

---

### 4. Knowledge Transfer
**Scenario**: Need to learn about a specific tech stack

**Query**: "Who has experience with Kafka and microservices?"

**Follow-up**: "Tell me about their Kafka projects"

---

## 🔧 Troubleshooting

### Issue: No Results Found
**Possible Causes**:
1. Filters too restrictive
   - **Solution**: Set filters to "All"
2. Query too specific
   - **Solution**: Use broader terms (e.g., "backend" instead of "FastAPI expert")
3. No matching profiles
   - **Solution**: Try related skills (e.g., "JavaScript" instead of "React")

---

### Issue: Slow Response
**Possible Causes**:
1. First time running (loading models)
   - **Solution**: Wait ~10 seconds, subsequent queries will be faster
2. Ollama not running
   - **Solution**: Start Ollama service
3. Large context
   - **Solution**: Apply filters to reduce search space

---

### Issue: Irrelevant Results
**Possible Causes**:
1. Query too vague
   - **Solution**: Add specific skills or project names
2. Generic keywords
   - **Solution**: Use technical terms (e.g., "FastAPI" instead of "web framework")

---

### Issue: App Won't Start
**Errors**:

**"Missing libraries"**
```bash
pip install llama-index-llms-ollama llama-index-embeddings-ollama
```

**"File not found: data/profiles.json"**
- Ensure `data/profiles.json` exists in the project directory

**"Model not found"**
```bash
ollama pull llama3.2:3b
ollama pull nomic-embed-text
```

---

## 📊 Understanding Debug Output

When you expand "Debug: See Retrieved Context", you'll see:

```
--- From Profile: Alice Johnson ---
Employee Name: Alice Johnson
Role: Senior Backend Engineer (Backend Team)
Location: Bangalore
Skills: Python, FastAPI, PostgreSQL
Projects:
  * PROJECT: Payment Gateway v2
    - Description: Redesigned payment...
    - Tech Stack: Python, FastAPI, Redis
...
```

**What This Means**:
- The LLM retrieved Alice's profile
- It found relevant keywords (Python, FastAPI)
- This document was used to generate the response

**Why It's Useful**:
- Verify the search is working correctly
- Understand why someone was included/excluded
- See the actual data the LLM is reading

---

## 🎨 UI Overview

### Main Interface
```
┌─────────────────────────────────────────────────┐
│  🔍 Internal Expertise Finder                   │
│  Powered by llama3.2:3b & nomic-embed-text      │
├─────────────────────────────────────────────────┤
│                                                 │
│  💬 Chat History:                               │
│  ┌──────────────────────────────────────────┐  │
│  │ Bot: Ready to search profiles...         │  │
│  │ You: Find a Python expert                │  │
│  │ Bot: Found 3 Python experts:             │  │
│  │      1. Alice Johnson (Backend)...       │  │
│  └──────────────────────────────────────────┘  │
│                                                 │
│  [Query employee database...] 🔍               │
└─────────────────────────────────────────────────┘
```

### Sidebar
```
┌──────────────────┐
│ Filter Results   │
├──────────────────┤
│ Location:        │
│ [All         ▼]  │
│                  │
│ Team:            │
│ [All         ▼]  │
└──────────────────┘
```

---

## 📈 Advanced Features

### 1. Contextual Follow-ups
The chat remembers context:
```
Query 1: "Find React experts"
Response: [Lists 3 people]

Query 2: "What projects did they work on?"
Response: [Details about the 3 people's React projects]
```

### 2. Multi-Criteria Search
Combine multiple requirements:
```
"Find someone with:
- Python and Go experience
- Worked on microservices
- In the Backend team"
```

### 3. Comparative Queries
```
"Compare the Python experience of Alice and Bob"
```

---

## 🔄 Session Management

### Chat History
- Persists during your browser session
- Cleared when you refresh the page
- Contains user queries and bot responses

### Starting Fresh
- Refresh the page to clear history
- Filters are also reset

---

## 📝 Best Practices

1. **Start Broad, Then Narrow**
   - First: "Find backend engineers"
   - Then: "Who among them knows Kubernetes?"

2. **Use Filters Strategically**
   - Apply filters before complex queries
   - Removes irrelevant results upfront

3. **Verify with Debug Mode**
   - Check if the right profiles were retrieved
   - Understand the AI's reasoning

4. **Ask Follow-up Questions**
   - Use the chat memory advantageously
   - Build on previous responses

5. **Be Patient on First Load**
   - Initial model loading takes ~10s
   - Subsequent queries are much faster

---

## 🆘 Getting Help

If you encounter issues:

1. **Check Debug Output**: See what documents were retrieved
2. **Review Filters**: Ensure they're not too restrictive
3. **Try Simpler Queries**: Start broad, then refine
4. **Verify Data**: Ensure `profiles.json` has the expected data
5. **Check Ollama**: Ensure Ollama service is running

---

## 🔮 Coming Soon

Planned features:
- [ ] Skills-based filtering
- [ ] Experience range filters
- [ ] Export results as CSV
- [ ] Bookmark favorite profiles
- [ ] Multi-language support
- [ ] Resume upload and search

---

## 📧 Example Conversation

```
User: "Hi, I need to find React experts for a new project"

Bot: "Found 3 React experts:

1. **Sarah Williams** (Frontend Engineer, Frontend Team)
   - **Expertise**: React, TypeScript, Next.js
   - **Relevant Project**: E-commerce Dashboard (React, TypeScript)
   - **Experience**: 6 years
   - **Contact**: sarah@company.com

2. **Mike Chen** (Full Stack Developer, Product Team)
   - **Expertise**: React, Node.js, GraphQL
   - **Relevant Project**: Customer Portal (React, GraphQL)
   - **Experience**: 4 years
   - **Contact**: mike@company.com

3. **Emily Davis** (Senior Frontend Engineer, Design Team)
   - **Expertise**: React, Vue.js, CSS-in-JS
   - **Relevant Project**: Design System (React, Storybook)
   - **Experience**: 7 years
   - **Contact**: emily@company.com"

User: "Tell me more about Sarah's e-commerce project"

Bot: "Sarah Williams worked on the **E-commerce Dashboard** project:

**Description**: Built a comprehensive admin dashboard for managing e-commerce operations, including inventory, orders, and analytics.

**Tech Stack**: React, TypeScript, Next.js, Tailwind CSS

**Her Role**: Led the frontend development, implemented real-time updates using WebSockets, and designed the component architecture.

Would you like to know more about any specific aspect of this project?"

User: "Is she in Bangalore?"

Bot: "No, Sarah Williams is located in **Mumbai** according to the profile data."

User: "Find React experts in Bangalore then"

Bot: [Applies location filter and searches again...]
```

---

This guide should help you get the most out of the Internal Expertise Finder! 🎉
