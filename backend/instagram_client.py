import asyncio
from instagrapi import Client
from instagrapi.exceptions import LoginRequired
import os
import json
import uuid
import time
import random
from instagrapi.types import Comment
import httpx

WEBHOOK_FILE = "data/webhooks.json"

class InstagramClient:
    def __init__(self):
        self.cl = Client()
        self.is_logged_in = False
        self.username = None
        self.active_tasks = {}
        self._followers_cache = None
        self._cache_expiry_time = 0
        self._CACHE_DURATION_SECONDS = 1800
        self.webhooks = self._load_webhooks()

    def _load_webhooks(self):
        os.makedirs(os.path.dirname(WEBHOOK_FILE), exist_ok=True)
        if os.path.exists(WEBHOOK_FILE):
            with open(WEBHOOK_FILE, 'r') as f:
                return json.load(f)
        return []

    def _save_webhooks(self):
        with open(WEBHOOK_FILE, 'w') as f:
            json.dump(self.webhooks, f, indent=4)

    async def add_webhook(self, url: str):
        if url not in self.webhooks:
            self.webhooks.append(url)
            await asyncio.to_thread(self._save_webhooks)
            return True
        return False

    async def remove_webhook(self, url: str):
        if url in self.webhooks:
            self.webhooks.remove(url)
            await asyncio.to_thread(self._save_webhooks)
            return True
        return False

    async def trigger_webhooks(self, payload: dict):
        async with httpx.AsyncClient() as client:
            tasks = [client.post(url, json=payload) for url in self.webhooks]
            await asyncio.gather(*tasks, return_exceptions=True)

    async def login_with_credentials(self, username, password):
        try:
            session_dir = "sessions"
            os.makedirs(session_dir, exist_ok=True)
            session_file = os.path.join(session_dir, f"{username}_session.json")

            # Use a new client instance for each login attempt to avoid state issues
            self.cl = Client()

            if os.path.exists(session_file):
                self.cl.load_settings(session_file)

            result = await asyncio.to_thread(self.cl.login, username, password)
            if not result: # Handles 2FA
                # In a real app, you would now need a separate flow to handle the 2FA code.
                # For now, we will treat this as a clear failure state.
                return False, "Two-factor authentication is enabled. Please use the session login method for now."

            self.cl.dump_settings(session_file)
            self.is_logged_in = True
            self.username = username
            await self.get_followers(force_refresh=True)
            return True, f"Successfully logged in as {username}"
        except ChallengeRequired as e:
            # For simplicity in this version, we will not handle the challenge interactively.
            # We will instruct the user to resolve it manually or use the session method.
            return False, "Challenge required. Please log in via the Instagram app or website to resolve it, then try again or use the session login method."
        except Exception as e:
            self.is_logged_in = False
            return False, str(e)

    async def login_with_session_id(self, session_json: str):
        try:
            cookies = json.loads(session_json)
            if not isinstance(cookies, list):
                return False, "Invalid format. Expected a JSON array of cookies from Cookie-Editor."

            # Construct a proper settings object for instagrapi
            settings = {
                "cookies": {cookie["name"]: cookie["value"] for cookie in cookies}
            }

            # Use a new client to avoid state contamination
            self.cl = Client()
            await asyncio.to_thread(self.cl.load_settings, settings)

            # The login call is necessary to populate user info
            user_id = self.cl.user_id_from_username(self.cl.username)
            await asyncio.to_thread(self.cl.user_info, user_id)

            self.is_logged_in = True
            self.username = self.cl.username
            await self.get_followers(force_refresh=True)
            return True, f"Successfully loaded session for user {self.cl.username}."
        except json.JSONDecodeError:
            return False, "Invalid JSON format. Please paste the entire content of the exported JSON file."
        except LoginRequired:
            self.is_logged_in = False
            return False, "The provided session is invalid or expired. Please export a fresh one."
        except Exception as e:
            self.is_logged_in = False
            return False, f"An unexpected error occurred during session load: {str(e)}"

    async def logout(self):
        if self.is_logged_in:
            for task_id in list(self.active_tasks.keys()):
                await self.stop_automation(task_id)
            username = self.username
            self.cl = Client()
            self.is_logged_in = False
            self.username = None
            return True, f"Successfully logged out from {username}."
        return False, "Not logged in."

    def start_automation(self, **kwargs):
        task_id = str(uuid.uuid4())
        task = AutomationTask(instagram_client=self, **kwargs)
        loop = asyncio.get_event_loop()
        asyncio_task = loop.create_task(task.run())
        self.active_tasks[task_id] = {"task_obj": task, "asyncio_task": asyncio_task}
        return task_id, f"Automation task {task_id} started."

    async def stop_automation(self, task_id: str):
        task_info = self.active_tasks.pop(task_id, None)
        if task_info:
            task_info["asyncio_task"].cancel()
            await task_info["task_obj"].stop()
            return True, f"Automation task {task_id} stopped."
        return False, "Task ID not found."

    async def get_followers(self, force_refresh=False):
        current_time = time.time()
        if force_refresh or not self._followers_cache or current_time > self._cache_expiry_time:
            try:
                if self.is_logged_in:
                    followers_map = await asyncio.to_thread(self.cl.user_followers, self.cl.user_id)
                    self._followers_cache = set(followers_map.keys())
                    self._cache_expiry_time = current_time + self._CACHE_DURATION_SECONDS
            except Exception as e:
                print(f"Error refreshing followers cache: {e}")
                return self._followers_cache or set()
        return self._followers_cache

    async def reply_to_comment(self, comment_id: str, text: str):
        if not self.is_logged_in:
            raise LoginRequired("You must be logged in to reply.")
        try:
            await asyncio.to_thread(self.cl.comment_reply, comment_id, text)
            return True
        except Exception as e:
            print(f"Error replying to comment {comment_id}: {e}")
            return False

    async def is_follower(self, user_id: str):
        if not self.is_logged_in:
            raise LoginRequired("You must be logged in.")
        followers = await self.get_followers()
        return user_id in followers

    async def send_dm(self, user_id: str, text: str):
        if not self.is_logged_in:
            raise LoginRequired("You must be logged in.")
        try:
            await asyncio.to_thread(self.cl.direct_send, text, user_ids=[user_id])
            return True
        except Exception as e:
            print(f"Error sending DM to user {user_id}: {e}")
            return False

class AutomationTask:
    def __init__(self, instagram_client, post_url: str, keywords: list, comment_replies: list, dm_replies: list, followers_only: bool, follow_message: str):
        self.parent_client = instagram_client
        self.cl = self.parent_client.cl
        self.post_url = post_url
        self.post_pk = self.cl.media_pk_from_url(post_url)
        self.keywords = [k.lower() for k in keywords]
        self.comment_replies = comment_replies
        self.dm_replies = dm_replies
        self.followers_only = followers_only
        self.follow_message = follow_message
        self.processed_comments = set()
        self.is_running = False
        self.status = "initializing"

    async def _process_comment(self, comment: Comment):
        if comment.has_liked or comment.pk in self.processed_comments:
            return
        self.processed_comments.add(comment.pk)
        if not any(keyword in comment.text.lower() for keyword in self.keywords):
            return
        await self.parent_client.trigger_webhooks(comment.dict())
        user_pk = str(comment.user.pk)
        if self.followers_only:
            our_followers = await self.parent_client.get_followers()
            if user_pk not in our_followers:
                if self.follow_message:
                    await asyncio.to_thread(self.cl.direct_send, self.follow_message, user_ids=[user_pk])
                return
        if self.comment_replies:
            await asyncio.sleep(random.uniform(5, 15))
            reply_text = random.choice(self.comment_replies)
            await asyncio.to_thread(self.cl.comment_reply, comment.pk, reply_text)
        if self.dm_replies:
            await asyncio.sleep(random.uniform(5, 15))
            dm_text = random.choice(self.dm_replies)
            await asyncio.to_thread(self.cl.direct_send, dm_text, user_ids=[user_pk])

    async def run(self):
        self.is_running = True
        self.status = "running"
        while self.is_running:
            try:
                comments = await asyncio.to_thread(self.cl.media_comments, self.post_pk, amount=20)
                for comment in comments:
                    if not self.is_running:
                        break
                    await self._process_comment(comment)
                await asyncio.sleep(random.uniform(60, 100))
            except LoginRequired:
                self.status = "relogin_required"
                self.is_running = False
            except Exception:
                self.status = "error"
                self.is_running = False

    async def stop(self):
        self.is_running = False
        self.status = "stopped"
