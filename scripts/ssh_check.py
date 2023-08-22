#!/usr/bin/env python3
import ssl
import socket
import datetime
import os
import requests

WEBHOOK_URL = os.environ["SLACK_WEBHOOK_URL"]
DOMAINS_SECRET = os.environ["DOMAINS"]

def ssl_expiry(domain):
    try:
        context = ssl.create_default_context()
        conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=domain)
        conn.connect((domain, 443))
        cert = conn.getpeercert()
        return datetime.datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z")
    except Exception as e:
        return None

def main():
    domains = DOMAINS_SECRET.strip().split('\n')
    
    for domain in domains:
        expiry_date = ssl_expiry(domain)
        if expiry_date:
            days_left = (expiry_date - datetime.datetime.now()).days
            alert_message = f"SSL Expiry Alert\n   * Domain: {domain}\n   * Warning: The SSL certificate will expire in {days_left} days."
            payload = {"text": alert_message}
            response = requests.post(WEBHOOK_URL, json=payload)
            if response.status_code == 200:
                print(f"Alert sent for {domain}")
            else:
                print(f"Failed to send alert for {domain}")
        else:
            print(f"Failed to retrieve SSL expiry for {domain}")

if __name__ == "__main__":
    main()
