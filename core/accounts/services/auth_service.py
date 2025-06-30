import requests

from config import settings


class AuthService:
    def __init__(self):
        self.base_url = f'{settings.DOCUMENTLM_AUTH_EP}/api'
        res = requests.post(
            f"${self.base_url}/auth/sign-in/email",
            headers={
                "Content-Type": "application/json"
            },
            json={
                "email": "tech@rhobots.ai",
                "password": "Q;-cPe/9Z804"
            }
        )
        self.token = res.json()['token']

    def create_organization(self, name: str, slug: str, created_by: str, private_metadata=None, max_allowed_memberships=1):
        res = requests.post(
            f"{self.base_url}/auth/organization/create",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.token}"
            },
            json={
                "name": name,
                "slug": slug,
                "userId": created_by,
                "metadata": private_metadata
            }
        )
        return res.json()