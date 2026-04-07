"""
Task Manager MCP Tool
Handles: create, list, update, delete tasks
"""

import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from db.database import create_task, list_tasks, update_task_status, delete_task


def manage_task(action: str, title: str = "", description: str = "",
                priority: str = "medium", assigned_to: str = "",
                due_date: str = "", task_id: str = "", status: str = "") -> str:
    """Manage tasks: create, list, update status, or delete.

    Args:
        action: One of 'create', 'list', 'update', 'delete'.
        title: Task title (required for create).
        description: Task description (optional).
        priority: 'low', 'medium', or 'high' (default: medium).
        assigned_to: Person assigned to the task (optional).
        due_date: Due date as string e.g. '2026-04-15' (optional).
        task_id: Task ID (required for update/delete).
        status: New status for update: 'pending', 'in_progress', 'completed', 'cancelled'.

    Returns:
        str: JSON string with the result.
    """
    try:
        if action == "create":
            result = create_task(title, description, priority, assigned_to, due_date)
        elif action == "list":
            result = list_tasks(status)
        elif action == "update":
            result = update_task_status(task_id, status)
        elif action == "delete":
            result = delete_task(task_id)
        else:
            result = {"error": f"Unknown action: {action}. Use create/list/update/delete."}
        return json.dumps(result, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})
