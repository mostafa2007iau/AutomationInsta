from fastapi import FastAPI, APIRouter, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List

from instagram_client import InstagramClient

app = FastAPI(
    title="Instagram Automation API",
    description="An unofficial API for automating Instagram tasks.",
    version="1.0.0"
)

# All API routes will be prefixed with /api
router = APIRouter(prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = InstagramClient()

# --- Pydantic Models ---
class CredentialsLogin(BaseModel):
    username: str
    password: str

class SessionIdLogin(BaseModel):
    session_json: str

class AutomationRequest(BaseModel):
    post_url: str
    keywords: List[str]
    comment_replies: List[str] = []
    dm_replies: List[str] = []
    followers_only: bool = False
    follow_message: str = "Please follow our page to get a response."

class WebhookRequest(BaseModel):
    url: str

class ReplyRequest(BaseModel):
    comment_id: str
    reply_text: str

# --- API Endpoints ---

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Instagram Automation API! API docs are at /docs."}

@router.get("/status", tags=["General"])
async def get_status():
    if client.is_logged_in:
        return {"status": "logged_in", "username": client.username}
    return {"status": "logged_out"}

@router.post("/login/credentials", tags=["Authentication"])
async def login_via_credentials(creds: CredentialsLogin):
    success, message = await client.login_with_credentials(creds.username, creds.password)
    if success:
        return {"message": message}
    return JSONResponse(status_code=401, content={"message": message})

@router.post("/login/session", tags=["Authentication"])
async def login_via_session_id(session: SessionIdLogin):
    success, message = await client.login_with_session_id(session.session_json)
    if success:
        return {"message": message}
    return JSONResponse(status_code=401, content={"message": message})

@router.post("/logout", tags=["Authentication"])
async def logout():
    success, message = client.logout()
    if success:
        return {"message": message}
    return JSONResponse(status_code=400, content={"message": message})

@router.post("/automations", tags=["Automation"])
async def create_automation(request: AutomationRequest):
    if not client.is_logged_in:
        return JSONResponse(status_code=403, content={"message": "You must be logged in."})
    task_id, message = client.start_automation(**request.dict())
    if task_id:
        return {"task_id": task_id, "message": message}
    return JSONResponse(status_code=500, content={"message": message})

@router.get("/automations", tags=["Automation"])
async def get_active_automations():
    if not client.is_logged_in:
        return JSONResponse(status_code=403, content={"message": "You must be logged in."})
    return {
        task_id: {
            "post_url": task_info["task_obj"].post_url,
            "keywords": task_info["task_obj"].keywords,
            "status": task_info["task_obj"].status
        }
        for task_id, task_info in client.active_tasks.items()
    }

@router.delete("/automations/{task_id}", tags=["Automation"])
async def delete_automation(task_id: str):
    success, message = await client.stop_automation(task_id)
    if success:
        return {"message": message}
    return JSONResponse(status_code=404, content={"message": message})

@router.post("/webhooks", tags=["Webhooks"])
async def add_webhook(webhook: WebhookRequest):
    if not client.is_logged_in:
        return JSONResponse(status_code=403, content={"message": "Authentication required."})
    if client.add_webhook(webhook.url):
        return {"message": "Webhook added successfully."}
    return JSONResponse(status_code=400, content={"message": "Webhook URL already exists."})

@router.get("/webhooks", tags=["Webhooks"])
async def get_webhooks():
    if not client.is_logged_in:
        return JSONResponse(status_code=403, content={"message": "Authentication required."})
    return {"webhooks": client.webhooks}

@router.delete("/webhooks", tags=["Webhooks"])
async def remove_webhook(webhook: WebhookRequest):
    if not client.is_logged_in:
        return JSONResponse(status_code=403, content={"message": "Authentication required."})
    if client.remove_webhook(webhook.url):
        return {"message": "Webhook removed successfully."}
    return JSONResponse(status_code=404, content={"message": "Webhook URL not found."})

# --- n8n Optimized Endpoints ---
n8n_router = APIRouter(prefix="/api/n8n", tags=["n8n Integration"])

@n8n_router.post("/automations/reply", tags=["n8n Integration"])
async def n8n_reply_to_comment(request: ReplyRequest):
    if not client.is_logged_in:
        return JSONResponse(status_code=403, content={"message": "Authentication required."})
    try:
        success = await client.reply_to_comment(request.comment_id, request.reply_text)
        if success:
            return {"message": "Reply sent successfully."}
        else:
            return JSONResponse(status_code=500, content={"message": "Failed to send reply."})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

class IsFollowerRequest(BaseModel):
    user_id: str

@n8n_router.post("/user/is-follower", tags=["n8n Integration"])
async def n8n_is_follower(request: IsFollowerRequest):
    if not client.is_logged_in:
        return JSONResponse(status_code=403, content={"message": "Authentication required."})
    try:
        is_follower_status = await client.is_follower(request.user_id)
        return {"is_follower": is_follower_status}
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

class SendDmRequest(BaseModel):
    user_id: str
    text: str

@n8n_router.post("/dm/send", tags=["n8n Integration"])
async def n8n_send_dm(request: SendDmRequest):
    if not client.is_logged_in:
        return JSONResponse(status_code=403, content={"message": "Authentication required."})
    try:
        success = await client.send_dm(request.user_id, request.text)
        if success:
            return {"message": "DM sent successfully."}
        else:
            return JSONResponse(status_code=500, content={"message": "Failed to send DM."})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

# Include the routers in the main app
app.include_router(router)
app.include_router(n8n_router)
