"""
ClinTask — Multi-Agent Clinical Task Management System
Built with Google ADK + Gemini

Architecture:
  Coordinator Agent (primary)
    ├── Task Manager Agent (sub-agent) — manages tasks via DB
    ├── Schedule Agent (sub-agent) — manages calendar/schedules via DB
    └── Notes Agent (sub-agent) — manages notes via DB

Each sub-agent has MCP-style tools that read/write to SQLite.
The coordinator routes user requests to the appropriate sub-agent.
"""

import sys
import os

# Ensure project root is in path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from google.adk.agents import Agent
from tools.task_tool import manage_task
from tools.schedule_tool import manage_schedule
from tools.notes_tool import manage_notes


# ──────────────────────────────────────────────
# Sub-Agent 1: Task Manager
# ──────────────────────────────────────────────
task_agent = Agent(
    name="task_manager_agent",
    model="gemini-2.0-flash",
    description="Manages tasks: create, list, update status, and delete tasks. Handles to-do items, assignments, and task tracking.",
    instruction="""You are the Task Manager agent. You handle all task-related requests.

Use the `manage_task` tool for all operations:
- To create a task: action='create', provide title, description, priority, assigned_to, due_date
- To list tasks: action='list', optionally filter by status ('pending','in_progress','completed','cancelled')
- To update a task: action='update', provide task_id and new status
- To delete a task: action='delete', provide task_id

Always confirm actions with clear responses. Show task details after creation.
If listing returns empty, say "No tasks found."
For priority, default to 'medium' unless the user specifies otherwise.
""",
    tools=[manage_task],
)


# ──────────────────────────────────────────────
# Sub-Agent 2: Schedule Manager
# ──────────────────────────────────────────────
schedule_agent = Agent(
    name="schedule_agent",
    model="gemini-2.0-flash",
    description="Manages calendar and schedule: create appointments, list upcoming events, delete events. Handles meetings, deadlines, and time-based entries.",
    instruction="""You are the Schedule agent. You handle all calendar and scheduling requests.

Use the `manage_schedule` tool for all operations:
- To create an event: action='create', provide title, start_time (format: 'YYYY-MM-DD HH:MM'), end_time, description, location
- To list events: action='list'
- To delete an event: action='delete', provide schedule_id

Always format times clearly. When creating events, confirm the details back to the user.
If no events exist, say "No scheduled events found."
""",
    tools=[manage_schedule],
)


# ──────────────────────────────────────────────
# Sub-Agent 3: Notes Manager
# ──────────────────────────────────────────────
notes_agent = Agent(
    name="notes_agent",
    model="gemini-2.0-flash",
    description="Manages notes: create, list, read, and delete notes. Handles meeting notes, clinical notes, memos, and information storage/retrieval.",
    instruction="""You are the Notes agent. You handle all note-related requests.

Use the `manage_notes` tool for all operations:
- To create a note: action='create', provide title, content, tags (comma-separated)
- To list notes: action='list', optionally filter by tag
- To read a specific note: action='read', provide note_id
- To delete a note: action='delete', provide note_id

When creating notes, confirm with the title and ID. When reading, display the full content.
If no notes found, say "No notes found."
""",
    tools=[manage_notes],
)


# ──────────────────────────────────────────────
# Primary Coordinator Agent
# ──────────────────────────────────────────────
root_agent = Agent(
    name="clintask_coordinator",
    model="gemini-2.0-flash",
    description="ClinTask Coordinator — routes user requests to the appropriate sub-agent for task management, scheduling, or notes.",
    instruction="""You are ClinTask, an intelligent multi-agent assistant that helps users manage tasks, schedules, and notes.

You coordinate three specialized sub-agents:
1. **task_manager_agent** — for creating, listing, updating, and deleting tasks/to-dos
2. **schedule_agent** — for managing calendar events, appointments, and meetings
3. **notes_agent** — for creating, reading, and organizing notes and information

ROUTING RULES:
- If the user mentions tasks, to-dos, assignments, priorities → delegate to task_manager_agent
- If the user mentions schedule, calendar, meetings, appointments, time slots → delegate to schedule_agent
- If the user mentions notes, memos, records, information storage → delegate to notes_agent
- If the request involves MULTIPLE agents (e.g., "create a task and schedule a meeting"), handle them sequentially by delegating to each relevant agent

MULTI-STEP WORKFLOWS:
- For complex requests like "Plan my day", coordinate across agents: check schedules, list pending tasks, and retrieve relevant notes
- For "Create a follow-up", create both a task AND a schedule entry
- Always summarize the combined results back to the user

Be helpful, concise, and proactive. If the user's intent is unclear, ask a brief clarifying question.
Start by introducing yourself as ClinTask when first greeted.
""",
    sub_agents=[task_agent, schedule_agent, notes_agent],
)
