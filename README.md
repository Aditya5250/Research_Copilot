# AI Research Copilot

A production-grade, stateful Multi-Agent AI Research Platform built with **LangGraph**, **pgvector**, **FastAPI**, and **Streamlit**.

## Features
- **Multi-Agent Orchestration**: Planner, Researcher, Writer, and Critic collaborating via a stateful, cyclical graph.
- **Hybrid RAG**: Integrated web search (Tavily) + semantic vector search over uploaded documents (pgvector).
- **Human-in-the-Loop (HITL)**: Graph interrupts before research execution for human inspection, plan editing, and approval.
- **Live Streaming**: Server-Sent Events (SSE) stream agent thoughts, node transitions, and token generation in real time.
- **Production Observability**: Full execution tracing, cost tracking, and token usage via Langfuse.
- **Rigorous Evaluation**: Automated benchmark test suite using RAGAS for faithfulness and relevance scoring.

## Quickstart (Development)

### 1. Start Postgres with pgvector
```bash
docker compose up -d postgres
```

### 2. Configure Environment
```bash
cp .env.example .env
# Fill in ANTHROPIC_API_KEY, TAVILY_API_KEY, etc.
```

### 3. Run FastAPI Backend
```bash
uv run uvicorn copilot.main:app --reload --port 8000
```
Visit API docs at `http://localhost:8000/docs`.

### 4. Run Streamlit UI
```bash
uv run streamlit run frontend/app.py
```
