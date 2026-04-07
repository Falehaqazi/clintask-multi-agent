# ClinTask — Multi-Agent Task Management System

A multi-agent AI system built with **Google ADK + Gemini 2.0 Flash** that helps users manage tasks, schedules, and information through coordinated AI agents.

Built for **Google Gen AI Academy APAC Edition — Track 1**

## Architecture

```
┌─────────────────────────────────────┐
│     ClinTask Coordinator Agent      │
│        (Primary / Router)           │
└──────┬──────────┬──────────┬────────┘
       │          │          │
       ▼          ▼          ▼
┌──────────┐ ┌──────────┐ ┌──────────┐
│  Task    │ │ Schedule │ │  Notes   │
│ Manager  │ │  Agent   │ │  Agent   │
│  Agent   │ │          │ │          │
└────┬─────┘ └────┬─────┘ └────┬─────┘
     │            │            │
     ▼            ▼            ▼
┌─────────────────────────────────────┐
│     SQLite Database (MCP Tools)     │
│   tasks | schedules | notes tables  │
└─────────────────────────────────────┘
```

## Core Requirements Met

| Requirement | Implementation |
|---|---|
| Primary agent coordinating sub-agents | Coordinator routes to 3 sub-agents |
| Structured data storage & retrieval | SQLite with tasks, schedules, notes tables |
| Multiple tools via MCP | Task tool, Schedule tool, Notes tool |
| Multi-step workflows | Cross-agent coordination (e.g., "plan my day") |
| API-based deployment | Cloud Run with HTTP endpoint |

## Project Structure

```
clintask/
├── clintask_agents/
│   ├── __init__.py
│   └── agent.py              # Coordinator + 3 sub-agents
├── tools/
│   ├── __init__.py
│   ├── task_tool.py           # Task manager MCP tool
│   ├── schedule_tool.py       # Calendar MCP tool
│   └── notes_tool.py          # Notes MCP tool
├── db/
│   ├── __init__.py
│   └── database.py            # SQLite operations
├── Dockerfile
├── requirements.txt
├── .env
└── README.md
```

## Example Interactions

**Single-agent task:**
> "Create a high-priority task: Review patient lab results by Friday"

**Multi-step workflow:**
> "Plan my day — show my pending tasks and upcoming schedule"

**Cross-agent coordination:**
> "Schedule a meeting with Dr. Kumar tomorrow at 2pm and create a task to prepare the agenda"

## Local Setup

```bash
pip install -r requirements.txt
# Edit .env with your Gemini API key
adk web
# Open http://localhost:8000 → select clintask_agents
```

## Deploy to Cloud Run

```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

gcloud services enable run.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com

gcloud run deploy clintask-agent \
  --source . \
  --region asia-south1 \
  --allow-unauthenticated \
  --set-env-vars "GOOGLE_API_KEY=YOUR_KEY"
```

## Tech Stack

- **Google ADK** — Agent orchestration framework
- **Gemini 2.0 Flash** — LLM inference
- **SQLite** — Structured data persistence
- **Cloud Run** — Serverless deployment
- **Python 3.12**

## Author

Faleha Qazi — B.Tech CSE (Health Informatics), VIT Bhopal University
