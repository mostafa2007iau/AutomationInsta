import json
import asyncio
from datetime import datetime
from typing import Literal

LOG_FILE = "backend/data/activity_log.json"
# Use a lock to prevent race conditions when writing to the log file
_log_lock = asyncio.Lock()

async def log_activity(
    username: str,
    event: Literal["action", "status_change", "error"],
    details: dict
):
    """
    Asynchronously logs an event to the central activity log.

    Args:
        username: The username of the account related to the event.
        event: The type of event (e.g., 'action', 'status_change', 'error').
        details: A dictionary containing event-specific information.
    """
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "username": username,
        "event": event,
        "details": details
    }

    async with _log_lock:
        try:
            # Read the existing logs
            try:
                with open(LOG_FILE, "r") as f:
                    logs = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                logs = []

            # Append the new log and write back
            logs.append(log_entry)

            with open(LOG_FILE, "w") as f:
                json.dump(logs, f, indent=4)

        except Exception as e:
            print(f"CRITICAL: Failed to write to log file: {e}")

# --- Example Usage ---
# async def main():
#     await log_activity(
#         "test_user",
#         "action",
#         {"type": "comment_reply", "post_url": "...", "target_user": "...", "text": "..."}
#     )
#     await log_activity(
#         "test_user",
#         "error",
#         {"source": "login", "message": "Challenge required"}
#     )
#
# if __name__ == "__main__":
#     asyncio.run(main())
