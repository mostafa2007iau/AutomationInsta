import asyncio
import os
import json
from instagrapi import Client
from instagrapi.exceptions import LoginRequired, ChallengeRequired, PrivateAccount

class InstagramClient:
    """
    Manages all interactions with the Instagram API for a single account.
    This client is stateless regarding application logic; it only holds the connection state.
    """
    def __init__(self, username, password=None, session_json=None, settings=None, tasks=None):
        self.username = username
        self.password = password
        self.session_json = session_json
        self.settings = settings or {}
        self.tasks = tasks or []

        self.cl = Client()
        self.status = "logged_out"

        # Apply proxy if specified
        proxy = self.settings.get("proxy")
        if proxy:
            self.cl.set_proxy(proxy)

    async def login(self):
        """
        Logs the client in using either session JSON or credentials.
        Manages session file persistence.
        """
        session_dir = "sessions"
        os.makedirs(session_dir, exist_ok=True)
        session_file = os.path.join(session_dir, f"{self.username}_session.json")

        try:
            if self.session_json:
                await asyncio.to_thread(self.cl.load_settings_from_dict, json.loads(self.session_json))
            elif os.path.exists(session_file):
                await asyncio.to_thread(self.cl.load_settings, session_file)
            elif self.password:
                await asyncio.to_thread(self.cl.login, self.username, self.password)
            else:
                await self._update_status_and_log("error_credentials_required", "Password or session is required.")
                return False, "Password or session is required to log in."

            self.cl.user_id = await asyncio.to_thread(self.cl.user_id_from_username, self.username)
            await self._update_status_and_log("logged_in", "Login successful.")

            await asyncio.to_thread(self.cl.dump_settings, session_file)

            return True, f"Successfully logged in as {self.username}"

        except (LoginRequired, PrivateAccount) as e:
            message = f"Login failed: The session or credentials may be invalid. {e}"
            await self._update_status_and_log("error_login_failed", message)
            return False, message
        except ChallengeRequired as e:
            message = f"Challenge required for {self.username}. Please resolve it manually. {e}"
            await self._update_status_and_log("error_challenge_required", message)
            return False, message
        except Exception as e:
            message = f"An unexpected error occurred during login: {e}"
            await self._update_status_and_log("error_unexpected", message)
            return False, message

    async def _update_status_and_log(self, status: str, message: str):
        """Helper to update status in AccountManager and log the event."""
        from account_manager import account_manager
        from logger import log_activity

        self.status = status
        # This will fail if account_manager is not ready, but should be fine in normal operation
        await account_manager.update_account_status(self.username, status)

        event_type = "error" if "error" in status else "status_change"
        await log_activity(self.username, event_type, {"message": message, "source": "login"})


    async def logout(self):
        """Logs the client out and clears the state."""
        await asyncio.to_thread(self.cl.logout)
        self.status = "logged_out"
        return True, f"Successfully logged out from {self.username}."

    # --- Wrapper methods for instagrapi functionalities ---

    async def get_media_comments(self, media_pk: str, amount: int = 20):
        """Fetches comments for a given media post."""
        try:
            comments = await asyncio.to_thread(self.cl.media_comments, media_pk, amount)
            return comments
        except Exception as e:
            print(f"[{self.username}] Error fetching comments: {e}")
            if isinstance(e, LoginRequired):
                self.status = "error_login_required"
            return []

    async def reply_to_comment(self, comment_pk: str, text: str):
        """Replies to a specific comment."""
        try:
            await asyncio.to_thread(self.cl.comment_reply, comment_pk, text)
            return True
        except Exception as e:
            print(f"[{self.username}] Error replying to comment {comment_pk}: {e}")
            return False

    async def send_dm(self, user_id: str, text: str):
        """Sends a direct message to a user."""
        try:
            await asyncio.to_thread(self.cl.direct_send, text, user_ids=[user_id])
            return True
        except Exception as e:
            print(f"[{self.username}] Error sending DM to {user_id}: {e}")
            return False

    async def get_post_pk_from_url(self, url: str):
        """Extracts the post PK from a URL."""
        try:
            return await asyncio.to_thread(self.cl.media_pk_from_url, url)
        except Exception:
            return None
