"""
Notes MCP Tool
Handles: create, list, read, delete notes
"""

import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from db.database import create_note, list_notes, get_note, delete_note


def manage_notes(action: str, title: str = "", content: str = "",
                 tags: str = "", note_id: str = "", tag: str = "") -> str:
    """Manage notes: create, list, read, or delete.

    Args:
        action: One of 'create', 'list', 'read', 'delete'.
        title: Note title (required for create).
        content: Note content (required for create).
        tags: Comma-separated tags e.g. 'clinical,followup' (optional).
        note_id: Note ID (required for read/delete).
        tag: Filter notes by tag when listing (optional).

    Returns:
        str: JSON string with the result.
    """
    try:
        if action == "create":
            result = create_note(title, content, tags)
        elif action == "list":
            result = list_notes(tag)
        elif action == "read":
            result = get_note(note_id)
        elif action == "delete":
            result = delete_note(note_id)
        else:
            result = {"error": f"Unknown action: {action}. Use create/list/read/delete."}
        return json.dumps(result, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})
