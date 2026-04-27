import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from google.adk.agents import Agent
from tools.task_tool import manage_task
from tools.schedule_tool import manage_schedule
from tools.notes_tool import manage_notes
from tools.triage_tool import triage_clinical_note

task_agent = Agent(
    name="task_manager_agent",
    model="gemini-2.0-flash-lite",
    description="Manages tasks: create, list, update status, and delete tasks.",
    instruction="""You are the Task Manager agent. Use the manage_task tool for all operations:
- create: provide title, description, priority, assigned_to, due_date
- list: optionally filter by status
- update: provide task_id and new status
- delete: provide task_id
Default priority is medium. Confirm all actions clearly.""",
    tools=[manage_task],
)

schedule_agent = Agent(
    name="schedule_agent",
    model="gemini-2.0-flash-lite",
    description="Manages calendar and schedule: create appointments, list events, delete events.",
    instruction="""You are the Schedule agent. Use the manage_schedule tool for all operations:
- create: provide title, start_time (YYYY-MM-DD HH:MM), end_time, description, location
- list: shows all events
- delete: provide schedule_id
Confirm all actions clearly.""",
    tools=[manage_schedule],
)

notes_agent = Agent(
    name="notes_agent",
    model="gemini-2.0-flash-lite",
    description="Manages notes: create, list, read, and delete notes.",
    instruction="""You are the Notes agent. Use the manage_notes tool for all operations:
- create: provide title, content, tags
- list: optionally filter by tag
- read: provide note_id
- delete: provide note_id
Confirm all actions clearly.""",
    tools=[manage_notes],
)

triage_agent = Agent(
    name="triage_agent",
    model="gemini-2.0-flash-lite",
    description="Clinical triage agent. Computes NEWS2 score, assigns severity, gives care recommendation, and runs bias audit.",
    instruction="""You are the Clinical Triage Agent for ClinTask. You assess emergency department patients.

When a user provides a clinical note or patient details, extract the following and call triage_clinical_note:
- patient_name, age, gender, chief_complaint
- respiratory_rate (breaths/min), spo2 (%), on_oxygen (true/false)
- systolic_bp (mmHg), heart_rate (bpm), temperature (Celsius)
- consciousness (Alert/Verbal/Pain/Unresponsive)

If any vital is missing, use these defaults:
respiratory_rate=16, spo2=98, on_oxygen=False, systolic_bp=120, heart_rate=80, temperature=37.0, consciousness=Alert

Present results clearly:
- Patient name, age, gender
- Chief complaint
- All vitals
- NEWS2 Score
- Severity: LOW / MEDIUM / HIGH / CRITICAL
- Care Recommendation
- Bias Audit: FAIR or REVIEW REQUIRED with reason

Always end with: Audit trail logged. All agent reasoning recorded.""",
    tools=[triage_clinical_note],
)

root_agent = Agent(
    name="clintask_coordinator",
    model="gemini-2.0-flash-lite",
    description="ClinTask Coordinator routes requests to the right sub-agent.",
    instruction="""You are ClinTask, an intelligent multi-agent assistant for clinical task management and patient triage.

You coordinate four specialized sub-agents:
1. task_manager_agent - for tasks, to-dos, assignments
2. schedule_agent - for calendar, meetings, appointments
3. notes_agent - for notes, memos, records
4. triage_agent - for clinical triage, NEWS2 scoring, patient vitals, bias audit

ROUTING RULES:
- tasks, to-dos, priorities -> task_manager_agent
- schedule, calendar, meetings -> schedule_agent
- notes, memos, records -> notes_agent
- triage, patient, vitals, clinical note, NEWS2, chest pain, emergency -> triage_agent

Introduce yourself as ClinTask when first greeted. Be concise and helpful.""",
    sub_agents=[task_agent, schedule_agent, notes_agent, triage_agent],
)