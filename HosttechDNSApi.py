import requests

class HosttechDNSAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.ns1.hosttech.eu/api/user/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    class Get:
        def __init__(self, parent):
            self.parent = parent

        def list_zones(self):
            """Get all DNS zones"""
            url = f"{self.parent.base_url}/zones"
            response = requests.get(url, headers=self.parent.headers)
            return response

        def list_records(self, zone_id):
            """Get all DNS records for a specific zone"""
            url = f"{self.parent.base_url}/zones/{zone_id}/records"
            response = requests.get(url, headers=self.parent.headers)
            return response

    class Set:
        def __init__(self, parent):
            self.parent = parent

        def create_record(self, zone_id, name, ipv4, type="A", ttl=3600, comment="Managed by HosttechDNSAPI Python Client"):
            """Create a new DNS record"""
            data = {
                      "type": type,
                      "name": name,
                      "ipv4": ipv4,
                      "ttl": ttl,
                      "comment": comment
                    }
            url = f"{self.parent.base_url}/zones/{zone_id}/records"
            response = requests.post(url, headers=self.parent.headers, json=data)
            return response.json()

        def update_record(self, zone_id, record_id, ipv4, ttl=3600, comment="Managed by HosttechDNSAPI Python Client"):
            """Update a DNS record"""
            data = {
                      "ipv4": ipv4,
                      "ttl": ttl,
                      "comment": comment
                    }
            url = f"{self.parent.base_url}/zones/{zone_id}/records/{record_id}"
            response = requests.put(url, headers=self.parent.headers, json=data)
            return response.json()



