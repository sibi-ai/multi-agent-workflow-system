# Multi-Agent Workflow System

A production multi-agent orchestration system built with **LangGraph** and **LangChain**.
Agents coordinate via shared state graphs with tool use, persistent memory, and human-in-the-loop checkpoints.

## Architecture

```
Ingestion Agent  →  Processing Agent  →  Reporting Agent
      ↓                   ↓                    ↓
  [API Tool]         [DB Tool]           [Email Tool]
      ↓                   ↓                    ↓
           Shared Long-Term Memory (Pinecone)
                         ↓
             Human Approval Checkpoint
```

## Features

- Multi-agent orchestration via LangGraph state graphs
- Tool use — agents call REST APIs, SQL databases, file systems
- Agent memory — short-term (in-graph state), long-term (Pinecone), persistent key-value store
- Human-in-the-loop — interrupt nodes before consequential actions
- Structured audit logging of every agent decision and tool call
- Async FastAPI service exposing agent workflows as endpoints

## Stack

| Component | Technology |
|-----------|-----------|
| Orchestration | LangGraph, LangChain |
| LLM | OpenAI GPT-4o |
| Long-term memory | Pinecone |
| Serving | FastAPI (async) |
| Infra | Docker, AWS EC2 |
| Monitoring | structlog (JSON) |

## Project Structure

```
├── src/
│   ├── agents/         # Ingestion, processing, reporting agents
│   ├── graph/          # LangGraph state schema and workflow
│   ├── memory/         # Vector store and key-value clients
│   ├── tools/          # API, DB, and file system tools
│   └── serving/        # FastAPI app
├── configs/
├── tests/
├── .github/workflows/
├── Dockerfile
└── requirements.txt
```

## Quickstart

```bash
git clone https://github.com/sibi-ai/multi-agent-workflow-system
cd multi-agent-workflow-system
pip install -r requirements.txt
# Set OPENAI_API_KEY and PINECONE_API_KEY in .env
uvicorn src.serving.api:app --reload
```

## Key Design Decisions

- Each agent has a defined role and isolated tool set
- Handoff conditions are explicit in the state graph
- Human approval nodes use LangGraph interrupt mechanism
- All tool calls are logged with input, output, agent ID, and timestamp
