# ClinTask — Fair Clinical Triage AI

A multi-agent clinical AI system built with **Google ADK + Gemini 2.5 Flash** that automates emergency department triage while actively detecting and flagging bias in automated medical decisions.

**Built for Google Solution Challenge 2026 — Unbiased AI Decision Track**

## The Problem
AI systems making triage decisions in emergency departments are often opaque, biased, and unaccountable — putting vulnerable patients at risk of unfair or delayed care.

## The Solution
ClinTask orchestrates four specialized AI agents — Intake, Triage Scorer, Bias Auditor, and Discharge Planner — each powered by Gemini 2.5 Flash via Google ADK. It takes raw clinical notes as input and produces evidence-based NEWS2 severity scores, care recommendations, and a real-time bias audit on every decision.

## Architecture

┌─────────────────────────────────────────┐
│       ClinTask Coordinator Agent        │
│         (Google ADK + Gemini 2.5)       │
└───┬─────────────┬───────────────┬───────┘
│             │               │
▼             ▼               ▼
┌────────┐  ┌──────────┐  ┌─────────────┐
│ Intake │  │  Triage  │  │    Bias     │
│ Agent  │→ │  Scorer  │→ │  Auditor   │
│        │  │  NEWS2   │  │   Agent    │
└────────┘  └──────────┘  └─────────────┘
│
▼
┌───────────────────┐
│ Discharge Planner │
│     Agent         │
└───────────────────┘

## Key Features
- **NEWS2 Scoring** — clinically validated, bias-resistant severity scoring
- **Bias Auditor Agent** — flags demographic anomalies in every triage decision
- **Full Explainability Trail** — every agent logs its reasoning step-by-step
- **FHIR R4 Compatible** — structured output for hospital EHR integration
- **Clinical Task Management** — task, schedule, and notes agents for clinical workflow
- **Cloud Run Deployed** — scalable, serverless on Google Cloud

## Tech Stack
- **Google ADK** — multi-agent orchestration
- **Gemini 2.5 Flash** — LLM inference for all agents
- **Google Cloud Run** — serverless deployment
- **FastAPI** — REST API backend
- **SQLite** — structured data persistence
- **Python 3.12**

## Local Setup
```bash
pip install -r requirements.txt
# Add your Gemini API key to .env
set GOOGLE_API_KEY=YOUR_KEY
adk web
# Open http://localhost:8000 → select clintask_agents
```

## Deploy to Cloud Run
```bash
gcloud auth login
gcloud config set project clintask-agent-2026
gcloud run deploy clintask-agent \
  --source . \
  --region asia-south1 \
  --allow-unauthenticated \
  --set-env-vars "GOOGLE_API_KEY=YOUR_KEY"
```

## Author
Faleha Qazi — B.Tech CSE (Health Informatics), VIT Bhopal University