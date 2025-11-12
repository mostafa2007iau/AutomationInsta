import json
from typing import Dict, List
from instagram_client import InstagramClient

class AccountManager:
    def __init__(self, accounts_file: str = "backend/data/accounts.json"):
        self.accounts_file = accounts_file
        self.accounts: Dict[str, InstagramClient] = {}
        self.load_accounts()

    def load_accounts(self):
        """Loads account configurations from the JSON file and initializes InstagramClient instances."""
        try:
            with open(self.accounts_file, "r") as f:
                accounts_data = json.load(f)

            for acc_data in accounts_data:
                username = acc_data.get("username")
                if username:
                    client = InstagramClient(
                        username=username,
                        password=acc_data.get("password"),
                        session_json=acc_data.get("session_json"),
                        settings=acc_data.get("settings", {}),
                        tasks=acc_data.get("tasks", [])
                    )
                    # Restore the last known status
                    client.status = acc_data.get("status", "logged_out")
                    self.accounts[username] = client
        except (FileNotFoundError, json.JSONDecodeError):
            # If the file doesn't exist or is empty, start with an empty list.
            self.save_accounts_to_file()

    def save_accounts_to_file(self):
        """Saves the current state of all account configurations to the JSON file."""
        accounts_data = []
        for client in self.accounts.values():
            # Create a dictionary representation of the client's state
            acc_data = {
                "username": client.username,
                "password": client.password,
                "session_json": client.session_json,
                "settings": client.settings,
                "status": client.status,
                "tasks": client.tasks
            }
            accounts_data.append(acc_data)

        with open(self.accounts_file, "w") as f:
            json.dump(accounts_data, f, indent=4)

    def get_account(self, username: str) -> InstagramClient:
        """Retrieves a specific account's client by username."""
        return self.accounts.get(username)

    def get_all_accounts(self) -> List[InstagramClient]:
        """Returns a list of all managed Instagram clients."""
        return list(self.accounts.values())

    async def update_account_status(self, username: str, new_status: str):
        """Updates the status of an account and saves the change to the file."""
        account = self.get_account(username)
        if account:
            account.status = new_status
            # For simplicity, we save the entire accounts list.
            # In a larger application, you might want to update just the specific account.
            self.save_accounts_to_file()
            # Also log this important event
            from logger import log_activity
            await log_activity(username, "status_change", {"new_status": new_status})


# A single instance to be used across the application
account_manager = AccountManager()
