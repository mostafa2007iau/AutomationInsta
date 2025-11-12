from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any

from account_manager import account_manager
from instagram_client import InstagramClient
from task_manager import TaskManager
from logger import log_activity
import json
from contextlib import asynccontextmanager

# This dictionary will hold the running TaskManager instances
task_managers: Dict[str, TaskManager] = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # On startup
    print("Application starting up...")
    # You could auto-login accounts or start tasks here.
    # For now, we will require manual initiation via API.
    yield
    # On shutdown
    print("Application shutting down...")
    for manager in task_managers.values():
        manager.stop()
    account_manager.save_accounts_to_file()
    print("All tasks stopped and account data saved.")

# --- FastAPI App Initialization ---
app = FastAPI(
    title="Instagram Multi-Account Automation API",
    description="API for managing multiple Instagram automation accounts.",
    version="2.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to the frontend's origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter(prefix="/api")

# --- Pydantic Models ---
class AccountCredentials(BaseModel):
    username: str
    password: str

class AccountSettings(BaseModel):
    proxy: str = None
    min_delay_s: int = 30
    max_delay_s: int = 90
    max_per_hour: int = 20
    max_per_day: int = 100

class Task(BaseModel):
    post_url: str
    keywords: List[str]
    comment_replies: List[str]
    dm_replies: List[str]

class TasksUpdate(BaseModel):
    tasks: List[Task]

# --- API Endpoints ---

@router.get("/accounts", tags=["Accounts"])
async def get_all_accounts():
    """Returns a list of all accounts and their current status."""
    return [
        {
            "username": client.username,
            "status": client.status,
            "settings": client.settings
        }
        for client in account_manager.get_all_accounts()
    ]

@router.post("/accounts", tags=["Accounts"])
async def add_account(creds: AccountCredentials):
    """Adds a new Instagram account to the manager."""
    if account_manager.get_account(creds.username):
        raise HTTPException(status_code=409, detail="Account already exists.")

    # This is a simplified add. In a real app, you'd encrypt the password.
    new_client = InstagramClient(username=creds.username, password=creds.password)
    account_manager.accounts[creds.username] = new_client
    account_manager.save_accounts_to_file()

    await log_activity(creds.username, "status_change", {"new_status": "added", "message": "Account added to system."})
    return {"message": "Account added successfully. Please log in to verify."}

@router.post("/accounts/{username}/login", tags=["Accounts"])
async def login_account(username: str):
    """Initiates a login attempt for a specific account."""
    client = account_manager.get_account(username)
    if not client:
        raise HTTPException(status_code=404, detail="Account not found.")

    success, message = await client.login()
    if success:
        return {"message": message}
    else:
        # The error status is already set and saved by the login method
        raise HTTPException(status_code=401, detail=message)

@router.put("/accounts/{username}/settings", tags=["Settings"])
async def update_account_settings(username: str, settings: AccountSettings):
    """Updates the settings for a specific account."""
    client = account_manager.get_account(username)
    if not client:
        raise HTTPException(status_code=404, detail="Account not found.")

    client.settings.update(settings.dict())
    account_manager.save_accounts_to_file()

    await log_activity(username, "status_change", {"message": "Settings updated."})
    return {"message": "Settings updated successfully."}

@router.put("/accounts/{username}/tasks", tags=["Tasks"])
async def update_account_tasks(username: str, tasks_update: TasksUpdate):
    """Updates the automation tasks for a specific account."""
    client = account_manager.get_account(username)
    if not client:
        raise HTTPException(status_code=404, detail="Account not found.")

    # Pydantic models need to be converted to dicts for JSON serialization
    client.tasks = [task.dict() for task in tasks_update.tasks]
    account_manager.save_accounts_to_file()

    await log_activity(username, "status_change", {"message": "Automation tasks updated."})
    return {"message": "Tasks updated successfully."}

@router.get("/logs", tags=["Logging"])
async def get_activity_logs():
    """Retrieves the full activity log."""
    try:
        with open("backend/data/activity_log.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

@router.post("/accounts/{username}/tasks/start", tags=["Tasks"])
async def start_tasks(username: str):
    """Starts the TaskManager for a specific account."""
    if username in task_managers and task_managers[username].is_running:
        raise HTTPException(status_code=400, detail="Tasks are already running.")

    client = account_manager.get_account(username)
    if not client:
        raise HTTPException(status_code=404, detail="Account not found.")
    if client.status != "logged_in":
        raise HTTPException(status_code=403, detail="Account must be logged in to start tasks.")
    if not client.tasks:
        raise HTTPException(status_code=400, detail="No tasks configured for this account.")

    # Update status before starting
    await account_manager.update_account_status(username, "running_tasks")

    manager = TaskManager(client)
    manager.load_tasks(client.tasks) # Load real tasks
    await manager.start()
    task_managers[username] = manager

    return {"message": f"Automation started for {username}."}

@router.post("/accounts/{username}/tasks/stop", tags=["Tasks"])
async def stop_tasks(username: str):
    """Stops the TaskManager for a specific account."""
    manager = task_managers.get(username)
    if not manager or not manager.is_running:
        raise HTTPException(status_code=400, detail="Tasks are not running.")

    manager.stop()
    del task_managers[username]

    # Revert status to logged_in
    await account_manager.update_account_status(username, "logged_in")

    return {"message": f"Automation stopped for {username}."}

# Include the router in the main app
app.include_router(router)
