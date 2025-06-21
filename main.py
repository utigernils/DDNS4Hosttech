import HosttechDNSApi
import PublicIp

import time

import os
from dotenv import load_dotenv

class Main:
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

        self.current_ip = "0.0.0.0"

        self.zone_id = self.check_domain(self.domain)

        if not self.zone_id:
            print(f"Zone {self.domain} not found.")
            return
        else:
            print(f"Zone '{self.domain}' found with ID: {self.zone_id}")

        self.record_id = self.check_record(self.zone_id, self.subdomain)

        if not self.record_id:
            print(f"Record '{self.subdomain}' not found in zone '{self.domain}'. Creating new record.")
            print(self.set_api.create_record(self.zone_id, self.subdomain, self.public_ip.get(), type="A", ttl=self.ttl))
            self.record_id = self.check_record(self.zone_id, self.subdomain)
            if not self.record_id:
                print(f"Failed to create record '{self.subdomain}' in zone '{self.domain}'.")
                return
            else:
                print(f"Record '{self.subdomain}' created successfully in zone '{self.domain}'.")
        else:
            print(f"Record '{self.subdomain}' found with ID: {self.record_id}")

        while True:
            self.current_ip = self.check_record_ip(self.zone_id, self.record_id)

            if self.current_ip != self.public_ip.get():
                print("Public IP has changed, updating DNS record...")
                self.update_record()
                self.current_ip = self.public_ip.get()
            else:
                print(f"Public IP of the DNS is still '{self.current_ip}' and has not changed, no update needed.")
            time.sleep(30)

    def check_domain(self, domain):
        response = self.get_api.list_zones()
        data = response.json()
        zones = data.get("zones") or data.get("data") or data
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

    def check_record_ip(self, zone_id, record_id):
        response = self.get_api.get_record(zone_id, record_id)
        data = response
        if isinstance(data, dict):
            if 'ipv4' in data:
                return data['ipv4']
            if 'data' in data and isinstance(data['data'], dict) and 'ipv4' in data['data']:
                return data['data']['ipv4']
        return None

    def update_record(self):
        ipv4 = self.public_ip.get()
        if not ipv4:
            print("Failed to retrieve public IP address.")
            return

        self.set_api.update_record(self.zone_id, self.record_id, ipv4, ttl=self.ttl)
        print(f"Record '{self.subdomain}' updated successfully with IP {ipv4} in zone '{self.domain}'.")

main = Main()

