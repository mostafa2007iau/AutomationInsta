import asyncio
import time
import random
from datetime import datetime, timedelta
from logger import log_activity
import json

class TaskManager:
    """
    Manages and executes automation tasks for a single Instagram account,
    respecting all defined limits and schedules.
    """
    def __init__(self, client):
        self.client = client
        self.tasks = [] # List of automation configurations
        self.is_running = False
        self._activity_log = [] # Tracks timestamps of actions
        self._current_task_index = 0
        self._processed_comments = set()

    def load_tasks(self, tasks_config: list):
        """Loads automation tasks from the account's configuration."""
        self.tasks = tasks_config
        # Load already processed comments from the log file to avoid duplicates on restart
        self._load_processed_comments()

    def _load_processed_comments(self):
        try:
            with open("backend/data/activity_log.json", "r") as f:
                logs = json.load(f)
            for log in logs:
                if log.get("username") == self.client.username and log.get("event") == "action":
                    comment_pk = log.get("details", {}).get("comment_pk")
                    if comment_pk:
                        self._processed_comments.add(comment_pk)
        except (FileNotFoundError, json.JSONDecodeError):
            pass # No logs yet

    async def start(self):
        """Starts the main automation loop."""
        if self.is_running or not self.tasks:
            return

        self.is_running = True
        print(f"[{self.client.username}] Task manager started.")
        asyncio.create_task(self._loop())

    def stop(self):
        """Stops the automation loop."""
        self.is_running = False
        print(f"[{self.client.username}] Task manager stopped.")

    async def _loop(self):
        """The main execution loop that cycles through tasks."""
        while self.is_running:
            if not self.tasks:
                self.stop()
                break

            if "error" in self.client.status:
                print(f"[{self.client.username}] Account has an error ({self.client.status}). Halting automation.")
                self.stop()
                break

            task_config = self.tasks[self._current_task_index]
            await self._execute_task(task_config)

            self._current_task_index = (self._current_task_index + 1) % len(self.tasks)

            # Wait before starting the next cycle to avoid spamming
            await asyncio.sleep(random.uniform(60, 120))

    async def _execute_task(self, task_config):
        """Fetches and processes comments for a single post."""
        post_url = task_config.get("post_url")
        print(f"[{self.client.username}] Executing task for post: {post_url}")

        post_pk = await self.client.get_post_pk_from_url(post_url)
        if not post_pk:
            print(f"[{self.client.username}] Could not get post PK for URL: {post_url}")
            return

        comments = await self.client.get_media_comments(post_pk)

        for comment in comments:
            if not self.is_running:
                break

            if comment.pk in self._processed_comments:
                continue

            keywords = [k.lower() for k in task_config.get("keywords", [])]
            if not any(keyword in comment.text.lower() for keyword in keywords):
                continue

            # If we reach here, the comment is a match.
            await self._process_comment(comment, task_config)


    async def _process_comment(self, comment, task_config):
        """Processes a single matched comment."""

        # Check if an action is allowed by the rate limiter
        if not await self._perform_action_if_allowed():
            return # Paused due to rate limits

        # Mark as processed immediately to prevent race conditions
        self._processed_comments.add(comment.pk)

        # 1. Send Comment Reply
        comment_replies = task_config.get("comment_replies", [])
        if comment_replies:
            reply_text = random.choice(comment_replies)
            success = await self.client.reply_to_comment(comment.pk, reply_text)
            if success:
                await log_activity(self.client.username, "action", {
                    "type": "comment_reply", "comment_pk": comment.pk, "text": reply_text
                })

        # 2. Send DM
        dm_replies = task_config.get("dm_replies", [])
        if dm_replies:
            await asyncio.sleep(random.uniform(5, 15)) # Small delay between reply and DM
            dm_text = random.choice(dm_replies)
            success = await self.client.send_dm(comment.user.pk, dm_text)
            if success:
                await log_activity(self.client.username, "action", {
                    "type": "dm_sent", "target_user_pk": comment.user.pk, "text": dm_text
                })


    async def _perform_action_if_allowed(self):
        """Checks rate limits and applies a delay before returning."""
        settings = self.client.settings

        now = datetime.now()
        hour_ago = now - timedelta(hours=1)
        day_ago = now - timedelta(days=1)

        self._activity_log = [t for t in self._activity_log if t > day_ago]

        hourly_actions = sum(1 for t in self._activity_log if t > hour_ago)
        daily_actions = len(self._activity_log)

        if hourly_actions >= settings.get("max_per_hour", 20):
            print(f"[{self.client.username}] Hourly limit reached. Pausing.")
            await asyncio.sleep(60 * 5) # Pause for 5 minutes if limit is hit
            return False

        if daily_actions >= settings.get("max_per_day", 100):
            print(f"[{self.client.username}] Daily limit reached. Stopping for the day.")
            self.stop()
            return False

        min_delay = settings.get("min_delay_s", 30)
        max_delay = settings.get("max_delay_s", 90)
        delay = random.uniform(min_delay, max_delay)
        print(f"[{self.client.username}] Performing action after {delay:.2f} seconds.")
        await asyncio.sleep(delay)

        self._activity_log.append(now)
        return True
