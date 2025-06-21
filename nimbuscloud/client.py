import requests
from .utils import build_headers, with_diagnostics

class NimbusClient:
    def _init_(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.nimbuscloud.dev/v1"
    @with_diagnostics
    def ping(self):
        url = f"{self.base_url}/ping"
        headers = build_headers(self.api_key)
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    @with_diagnostics
    def list_instances(self):
        url = f"{self.base_url}/instances"
        headers = build_headers(self.api_key)
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
