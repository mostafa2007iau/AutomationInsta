from instagrapi import Client
from instagrapi.exceptions import LoginRequired
import os
import json

import uuid

import time

class InstagramClient:
    """
    A wrapper class for the instagrapi.Client to manage Instagram interactions,
    including login, logout, and automation tasks.
    """
    def __init__(self):
        self.cl = Client()
        self.is_logged_in = False
        self.username = None
        self.active_tasks = {} # To store and manage running automation tasks
        # Centralized cache for followers list
        self._followers_cache = None
        self._cache_expiry_time = 0
        self._CACHE_DURATION_SECONDS = 1800 # 30 minutes

    async def login_with_credentials(self, username, password):
        """
        Logs in to Instagram using username and password.
        Dumps the session to a JSON file for future use.
        """
        try:
            session_dir = "sessions"
            os.makedirs(session_dir, exist_ok=True)
            session_file = os.path.join(session_dir, f"{username}_session.json")

            # instagrapi login methods are synchronous, so we can't make the whole block async without running it in an executor.
            # For simplicity, we will keep the login part synchronous and handle the async cache call carefully.
            # This is a compromise. A full async implementation would require an async-native Instagram library.

            if os.path.exists(session_file):
                self.cl.load_settings(session_file)
                self.cl.login(username, password) # Re-login to verify session
            else:
                self.cl.login(username, password)

            self.cl.dump_settings(session_file) # Always dump to refresh the session
            self.is_logged_in = True
            self.username = username
            await self.get_followers(force_refresh=True) # Pre-populate cache on login
            return True, f"Successfully logged in as {username}"
        except Exception as e:
            self.is_logged_in = False
            return False, str(e)

    def login_with_session(self, session_json_data):
        """
        Logs in to Instagram using session data provided as a JSON string or dict.
        """
        try:
            # The session data is loaded into the client
            self.cl.load_settings_from_dict(session_json_data)
            # A test request to verify the session is valid
            self.cl.get_timeline_feed()

            self.is_logged_in = True
            self.username = self.cl.username
            return True, f"Successfully logged in with session as {self.cl.username}"
        except LoginRequired:
            self.is_logged_in = False
            return False, "The provided session is invalid or has expired. Please log in again."
        except Exception as e:
            self.is_logged_in = False
            return False, str(e)

    def logout(self):
        """
        Logs out from the current session and stops all running tasks.
        """
        if self.is_logged_in:
            # Stop all running tasks
            for task_id in list(self.active_tasks.keys()):
                self.stop_automation(task_id)

            username = self.username

            # Reset the client to clear session data
            self.cl = Client()
            self.is_logged_in = False
            self.username = None

            return True, f"Successfully logged out from {username} and stopped all tasks."
        return False, "Not logged in."

    def start_automation(self, background_tasks, post_url: str, keywords: list, comment_replies: list, dm_replies: list, followers_only: bool, follow_message: str):
        """
        Starts a new automation task in the background.
        """
        if not self.is_logged_in:
            return None, "You must be logged in to start an automation task."

        task_id = str(uuid.uuid4())
        task = AutomationTask(
            instagram_client=self,
            post_url=post_url,
            keywords=keywords,
            comment_replies=comment_replies,
            dm_replies=dm_replies,
            followers_only=followers_only,
            follow_message=follow_message
        )
        self.active_tasks[task_id] = task

        # Use FastAPI's BackgroundTasks to run the task without blocking
        background_tasks.add_task(task.run)

        return task_id, f"Automation task {task_id} started successfully for post {post_url}."

    def stop_automation(self, task_id: str):
        """
        Stops a running automation task.
        """
        if task_id not in self.active_tasks:
            return False, "Task ID not found."

        task = self.active_tasks[task_id]
        task.stop()
        del self.active_tasks[task_id]

        return True, f"Automation task {task_id} stopped successfully."

    async def get_followers(self, force_refresh=False):
        """
        Returns a set of follower user IDs, using a time-based cache.
        """
        current_time = time.time()
        if force_refresh or not self._followers_cache or current_time > self._cache_expiry_time:
            print(f"Refreshing followers cache (Force: {force_refresh})...")
            try:
                if not self.is_logged_in:
                    print("Cannot refresh followers, not logged in.")
                    return set()
                followers_map = self.cl.user_followers(self.cl.user_id)
                self._followers_cache = set(followers_map.keys())
                self._cache_expiry_time = current_time + self._CACHE_DURATION_SECONDS
                print(f"Followers cache refreshed successfully. Found {len(self._followers_cache)} followers.")
            except Exception as e:
                print(f"Error refreshing followers cache: {e}")
                return self._followers_cache or set()

        return self._followers_cache

import asyncio
import random
from instagrapi.types import Comment

class AutomationTask:
    """
    A class to hold the state and logic of a single automation task.
    """
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
        """
        Processes a single comment based on the automation rules.
        """
        # 1. Check if comment has keywords and has not been processed
        if any(keyword in comment.text.lower() for keyword in self.keywords) and comment.pk not in self.processed_comments:
            user_pk = str(comment.user.pk)

            # 2. Check follower status if required
            if self.followers_only:
                our_followers = await self.parent_client.get_followers()
                if user_pk not in our_followers:
                    # Send DM asking to follow
                    if self.follow_message:
                        self.cl.direct_send(self.follow_message, user_ids=[user_pk])
                    self.processed_comments.add(comment.pk)
                    return # Stop processing this comment

            # 3. Reply to the comment
            if self.comment_replies:
                reply_text = random.choice(self.comment_replies)
                self.cl.comment_reply(comment.pk, reply_text)

            # 4. Send a DM
            if self.dm_replies:
                dm_text = random.choice(self.dm_replies)
                self.cl.direct_send(dm_text, user_ids=[user_pk])

            # 5. Mark as processed
            self.processed_comments.add(comment.pk)
            print(f"Processed comment {comment.pk} from user {comment.user.username}")


    async def run(self):
        """
        The main loop for the automation task. Runs until stopped.
        """
        self.is_running = True
        print(f"Starting automation for post {self.post_pk}...")
        while self.is_running:
            try:
                # Fetch recent comments for the post
                comments = self.cl.media_comments(self.post_pk, amount=20)
                for comment in comments:
                    await self._process_comment(comment)

                # Wait for a while before checking for new comments again
                await asyncio.sleep(60) # Check every 60 seconds
            except Exception as e:
                print(f"An error occurred in automation task: {e}")
                # Optional: stop the task on error or just wait and retry
                await asyncio.sleep(300) # Wait 5 minutes before retrying on error


    def stop(self):
        """
        Stops the automation task.
        """
        self.is_running = False
        print(f"Stopping automation for post {self.post_pk}.")
