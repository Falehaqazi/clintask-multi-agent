# ClinTask — Fair Clinical Triage AI

A multi-agent clinical AI system built with **Google ADK + Gemini 2.5 Flash** that automates emergency department triage while actively detecting and flagging bias in automated medical decisions.

**Built for Google Solution Challenge 2026 — Unbiased AI Decision Track**

## The Problem

AI systems making triage decisions in emergency departments are often opaque, biased, and unaccountable — putting vulnerable patients at risk of unfair or delayed care.

## The Solution

ClinTask orchestrates four specialized AI agents — Intake, Triage Scorer, Bias Auditor, and Discharge Planner — each powered by Gemini 2.5 Flash via Google ADK. It takes raw clinical notes as input and produces evidence-based NEWS2 severity scores, care recommendations, and a real-time bias audit on every decision.

## Architecture

| Agent | Role |
|---|---|
| Coordinator | Routes requests to specialized sub-agents |
| Intake Agent | Extracts vitals, demographics, chief complaint |
| Triage Scorer | Computes NEWS2 score, assigns severity level |
| Bias Auditor | Flags demographic anomalies, outputs FAIR or REVIEW REQUIRED |
| Discharge Planner | Recommends care pathway and logs reasoning chain |

## Key Features

- **NEWS2 Scoring** — clinically validated, bias-resistant severity scoring
- **Bias Auditor Agent** — flags demographic anomalies in every triage decision
- **Full Explainability Trail** — every agent logs its reasoning step-by-step
- **FHIR R4 Compatible** — structured output for hospital EHR integration
- **Clinical Task Management** — task, schedule, and notes agents for clinical workflow
- **Cloud Run Deployed** — scalable, serverless on Google Cloud

## Tech Stack

- Google ADK and Gemini 2.5 Flash
- Google Cloud Run
- FastAPI and SQLite
- Python 3.12

## Live Demo

https://clintask-agent-218190051037.asia-south1.run.app

## Local Setup

Add your Gemini API key to .env then run: adk web

## Author

Faleha Qazi — B.Tech CSE Health Informatics, VIT Bhopal University