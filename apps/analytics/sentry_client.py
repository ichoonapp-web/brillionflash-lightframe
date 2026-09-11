import requests
import os

class SentryAutomation:
    def __init__(self):
        self.base_url = "https://sentry.io/api/0"
        self.headers = {'Authorization': f'Bearer {os.getenv("SENTRY_TOKEN", "")}'}
        self.org = os.getenv("SENTRY_ORG", "")

    def get_unresolved_issues(self, project, limit=10):
        url = f"{self.base_url}/projects/{self.org}/{project}/issues/"
        params = {'query': 'is:unresolved', 'sort': 'date', 'limit': limit}
        try:
            response = requests.get(url, headers=self.headers, params=params)
            return response.json()
        except Exception:
            return []
