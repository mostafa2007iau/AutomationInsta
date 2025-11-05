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
            if os.path.exists(session_file):
                await asyncio.to_thread(self.cl.load_settings, session_file)
            await asyncio.to_thread(self.cl.login, username, password)
            await asyncio.to_thread(self.cl.dump_settings, session_file)
            self.is_logged_in = True
            self.username = username
            await self.get_followers(force_refresh=True)
            return True, f"Successfully logged in as {username}"
        except Exception as e:
            self.is_logged_in = False
            return False, str(e)

    async def login_with_session_id(self, session_id: str):
        try:
            if not isinstance(session_id, str) or len(session_id) < 50:
                return False, "Invalid session ID format. Please provide a valid sessionid string."

            await asyncio.to_thread(self.cl.login_by_sessionid, session_id)

            # Verify the session is valid by making a test call
            await asyncio.to_thread(self.cl.get_timeline_feed)

            self.is_logged_in = True
            self.username = self.cl.username
            await self.get_followers(force_refresh=True) # Pre-populate cache
            return True, f"Successfully logged in with session as {self.cl.username}"
        except LoginRequired:
            self.is_logged_in = False
            return False, "The provided session ID is invalid or has expired."
        except Exception as e:
            self.is_logged_in = False
            return False, f"An unexpected error occurred: {str(e)}"

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

    def start_automation(self, background_tasks, **kwargs):
        task_id = str(uuid.uuid4())
        task = AutomationTask(instagram_client=self, **kwargs)
        self.active_tasks[task_id] = task
        background_tasks.add_task(task.run)
        return task_id, f"Automation task {task_id} started."

    async def stop_automation(self, task_id: str):
        task = self.active_tasks.pop(task_id, None)
        if task:
            await task.stop()
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
        while self.is_running:
            try:
                comments = await asyncio.to_thread(self.cl.media_comments, self.post_pk, amount=20)
                for comment in comments:
                    await self._process_comment(comment)
                await asyncio.sleep(random.uniform(60, 100))
            except Exception as e:
                print(f"An error occurred in automation task: {e}")
                await asyncio.sleep(300)

    async def stop(self):
        self.is_running = False
