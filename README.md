# 🌍 Agentic Travel Planning Assistant

An agentic AI travel planner built with LangChain, LangGraph, and MCP (Model Context Protocol).

## 📋 Description

This project implements an agentic travel planning assistant capable of reasoning about a user request and invoking external tools via MCP servers. It was built as part of the **Agentic AI Lab** using LangChain and MCP.

## 🏗️ Architecture

```
Streamlit GUI → LangGraph Agent ↔ Groq LLM → MCP Tool Servers
```

## 🛠️ Tools (via MCP)

| Tool | Purpose | Port |
|------|---------|------|
| Destination Search | Retrieves tourist attractions and activities | 3336 |
| Budget Calculator | Estimates total travel cost in USD | 3333 |
| Weather Tool | Provides weather conditions for travel dates | 3334 |
| Currency Converter | Converts budget to preferred currency | 3335 |
| Calculator | Performs arithmetic operations | 3337 |

## ⚙️ Tech Stack

- Python 3.10+
- LangChain / LangGraph
- MCP SDK v1.27.0
- Groq API (`llama-3.3-70b-versatile`)
- Streamlit
- Pydantic

## 🚀 Installation

### 1. Clone the repository
```bash
git clone https://github.com/TON_USERNAME/travel-agent.git
cd travel-agent
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install langchain langchain-community streamlit mcp fastapi uvicorn langchain-groq langgraph langchain-core pydantic python-dotenv
```

### 4. Configure API Key
Create a `.env` file in the root directory:
```
GROQ_API_KEY=your_groq_api_key_here
```
Get your free API key at: https://console.groq.com

## ▶️ Usage

Open **6 terminals**, activate venv in each, then run:

| Terminal | Command |
|----------|---------|
| 1 | `python budget_mcp_server.py` |
| 2 | `python weather_mcp_server.py` |
| 3 | `python currency_mcp_server.py` |
| 4 | `python search_mcp_server.py` |
| 5 | `python calculator_mcp_server.py` |
| 6 | `streamlit run app.py` |

Then open **http://localhost:8501** in your browser.

## 💡 Example Query

> "Plan a 5-day trip to Barcelona with an estimated budget and suggested activities"

## 📝 Exercises Implemented

- ✅ **Exercise 1** — Display each tool call in the GUI
- ✅ **Exercise 2** — Critic agent to validate itineraries
- ✅ **Exercise 3** — Budget constraint with automatic re-planning
