import HosttechDNSApi
import PublicIp
import os
from dotenv import load_dotenv

class Main:
    def check_domain(self, domain):
        response = self.get_api.list_zones()
        data = response.json()
        zones = data.get("zones") or data.get("data") or data  # Fallback falls Struktur anders ist
        for zone in zones:
            if isinstance(zone, dict) and zone.get('name') == domain:
                return zone.get('id')
        return None

    def check_record(self, zone_id, subdomain):
        response = self.get_api.list_records(zone_id)
        data = response.json()
        records = data.get("records") or data.get("data") or data
        for record in records:
            if isinstance(record, dict) and record.get('name') == subdomain and record.get('type') == 'A':
                return record.get('id')
        return None

    def __init__(self):
        load_dotenv()

        self.api_key = os.getenv('HOSTTECH_API_KEY')
        self.domain = os.getenv('DOMAIN')
        self.subdomain = os.getenv('SUBDOMAIN')
        self.ttl = int(os.getenv('TTL', 3600))

        self.dns_api = HosttechDNSApi.HosttechDNSAPI(self.api_key)

        self.get_api = self.dns_api.Get(self.dns_api)
        self.set_api = self.dns_api.Set(self.dns_api)

        self.public_ip = PublicIp.PublicIp()

        self.zone_id = self.check_domain(self.domain)
        self.record_id = self.check_record(self.zone_id, self.subdomain)

        print(self.record_id)

main = Main()

