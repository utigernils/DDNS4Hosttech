import requests

class PublicIp:
    def __init__(self):
        self.base_url = "https://api.my-ip.io/v2"
        self.headers = {
            "Content-Type": "application/json"
        }

    def get(self):
        """Get current public IP address"""
        url = f"{self.base_url}/ip.json"
        try:
            response = requests.get(url, headers=self.headers, timeout=5)
            response.raise_for_status()
            try:
                return response.json().get('ip', None)
            except ValueError:
                return None
        except requests.RequestException:
            return None
