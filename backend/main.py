from fastapi import FastAPI, BackgroundTasks
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables from .env file
load_dotenv()

app = FastAPI(
    title="Instagram Automation API",
    description="An unofficial API for automating Instagram tasks like replying to comments and DMs.",
    version="0.1.0"
)

# --- CORS Middleware ---
# This allows the frontend (running on a different port/domain) to communicate with the backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, you should restrict this to your frontend's domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Instagram Automation API!"}

from .instagram_client import InstagramClient
from pydantic import BaseModel
from fastapi.responses import JSONResponse

# --- Pydantic Models for API requests ---
class UserCredentials(BaseModel):
    username: str
    password: str

class SessionData(BaseModel):
    session_data: dict

# --- Global Instagram Client Instance ---
# This single instance will manage the Instagram session for the application.
# (Note: For a multi-user application, a more complex session management system would be needed)
client = InstagramClient()

# --- API Endpoints ---
@app.post("/login/credentials", tags=["Authentication"])
async def login_via_credentials(credentials: UserCredentials):
    """
    Login to Instagram using username and password.
    """
    success, message = await client.login_with_credentials(credentials.username, credentials.password)
    if success:
        return {"message": message}
    return JSONResponse(status_code=401, content={"message": message})

@app.post("/login/session", tags=["Authentication"])
async def login_via_session(session: SessionData):
    """
    Login to Instagram using session data (as a JSON object).
    """
    success, message = client.login_with_session(session.session_data)
    if success:
        return {"message": message}
    return JSONResponse(status_code=401, content={"message": message})

@app.post("/logout", tags=["Authentication"])
async def logout():
    """
    Logout from the current Instagram session.
    """
    success, message = client.logout()
    if success:
        return {"message": message}
    return JSONResponse(status_code=400, content={"message": message})

from fastapi import BackgroundTasks

class AutomationRequest(BaseModel):
    post_url: str
    keywords: list[str]
    comment_replies: list[str]
    dm_replies: list[str]
    followers_only: bool = False
    follow_message: str = "Please follow our page to get a response."

@app.post("/automations", tags=["Automation"])
async def create_automation(request: AutomationRequest, background_tasks: BackgroundTasks):
    """
    Create and start a new automation task.
    """
    if not client.is_logged_in:
        return JSONResponse(status_code=403, content={"message": "You must be logged in."})

    task_id, message = client.start_automation(
        background_tasks=background_tasks,
        post_url=request.post_url,
        keywords=request.keywords,
        comment_replies=request.comment_replies,
        dm_replies=request.dm_replies,
        followers_only=request.followers_only,
        follow_message=request.follow_message
    )
    if task_id:
        return {"task_id": task_id, "message": message}
    return JSONResponse(status_code=500, content={"message": message})

@app.get("/automations", tags=["Automation"])
async def get_active_automations():
    """
    Get a list of all active automation tasks.
    """
    if not client.is_logged_in:
        return JSONResponse(status_code=403, content={"message": "You must be logged in."})

    active_tasks_info = {
        task_id: {
            "post_url": task.post_url,
            "keywords": task.keywords,
            "is_running": task.is_running
        }
        for task_id, task in client.active_tasks.items()
    }
    return active_tasks_info

@app.delete("/automations/{task_id}", tags=["Automation"])
async def stop_automation(task_id: str):
    """
    Stop a running automation task by its ID.
    """
    if not client.is_logged_in:
        return JSONResponse(status_code=403, content={"message": "You must be logged in."})

    success, message = client.stop_automation(task_id)
    if success:
        return {"message": message}
    return JSONResponse(status_code=404, content={"message": message})

# --- n8n Integration Endpoint ---
class N8NRequest(BaseModel):
    action: str # e.g., "send_dm", "get_comments"
    payload: dict

@app.post("/api/n8n/action", tags=["n8n Integration"])
async def handle_n8n_action(request: N8NRequest):
    """
    A generic endpoint to handle actions from n8n workflows.
    """
    if not client.is_logged_in:
        return JSONResponse(status_code=403, content={"message": "Authentication required."})

    action = request.action
    payload = request.payload

    try:
        if action == "send_dm":
            user_id = payload.get("user_id")
            text = payload.get("text")
            if not user_id or not text:
                return JSONResponse(status_code=400, content={"message": "user_id and text are required for send_dm."})
            client.cl.direct_send(text, user_ids=[str(user_id)])
            return {"status": "success", "message": f"DM sent to user {user_id}."}

        elif action == "post_comment":
            media_id = payload.get("media_id")
            text = payload.get("text")
            if not media_id or not text:
                return JSONResponse(status_code=400, content={"message": "media_id and text are required for post_comment."})
            client.cl.media_comment(media_id, text)
            return {"status": "success", "message": f"Comment posted on media {media_id}."}

        elif action == "get_media_comments":
            media_id = payload.get("media_id")
            amount = payload.get("amount", 20)
            if not media_id:
                return JSONResponse(status_code=400, content={"message": "media_id is required for get_media_comments."})
            comments = client.cl.media_comments(media_id, amount=int(amount))
            comments_data = [c.dict() for c in comments]
            return {"status": "success", "data": comments_data}

        elif action == "get_user_posts":
            user_id = payload.get("user_id", client.cl.user_id) # Defaults to self if no user_id is provided
            amount = payload.get("amount", 10)
            if not user_id:
                return JSONResponse(status_code=400, content={"message": "user_id is required."})
            posts = client.cl.user_medias(user_id, amount=int(amount))
            posts_data = [p.dict() for p in posts]
            return {"status": "success", "data": posts_data}

        elif action == "check_follower_status":
            target_user_id = payload.get("target_user_id")
            if not target_user_id:
                return JSONResponse(status_code=400, content={"message": "target_user_id is required."})

            followers = await client.get_followers()
            is_follower = str(target_user_id) in followers
            return {"status": "success", "is_follower": is_follower}

        else:
            return JSONResponse(status_code=400, content={"message": f"Unknown action: {action}"})

    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

@app.get("/status", tags=["General"])
async def get_status():
    """
    Check the current login status.
    """
    if client.is_logged_in:
        return {"status": "logged_in", "username": client.username}
    return {"status": "logged_out"}
