"""
Calendar / Schedule MCP Tool
Handles: create, list, delete scheduled events
"""

import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from db.database import create_schedule, list_schedules, delete_schedule


def manage_schedule(action: str, title: str = "", start_time: str = "",
                    end_time: str = "", description: str = "",
                    location: str = "", schedule_id: str = "") -> str:
    """Manage calendar/schedule entries: create, list, or delete.

    Args:
        action: One of 'create', 'list', 'delete'.
        title: Event title (required for create).
        start_time: Start time e.g. '2026-04-10 09:00' (required for create).
        end_time: End time e.g. '2026-04-10 10:00' (optional).
        description: Event description (optional).
        location: Event location (optional).
        schedule_id: Schedule ID (required for delete).

    Returns:
        str: JSON string with the result.
    """
    try:
        if action == "create":
            result = create_schedule(title, start_time, end_time, description, location)
        elif action == "list":
            result = list_schedules()
        elif action == "delete":
            result = delete_schedule(schedule_id)
        else:
            result = {"error": f"Unknown action: {action}. Use create/list/delete."}
        return json.dumps(result, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})
