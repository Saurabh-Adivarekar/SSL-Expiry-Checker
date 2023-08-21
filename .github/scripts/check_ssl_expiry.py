import os
import sys
import ssl
import socket
import datetime

def get_remaining_days(expiry_date):
    current_date = datetime.datetime.now()
    remaining_days = (expiry_date - current_date).days
    return remaining_days

def main():
    domains = sys.argv[1].split(",")
    alerts = []  # To store alerts for SSL expiry
    
    for domain in domains:
        try:
            ctx = ssl.create_default_context()
            with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
                s.connect((domain, 443))
                cert = s.getpeercert()
                expiry_date = datetime.datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z")
                days_to_expire = get_remaining_days(expiry_date)
                
                if days_to_expire <= 30:
                    alert_message = (
                        f"SSL Expiry Alert\n"
                        f" * Domain : {domain}\n"
                        f" * Warning : The SSL certificate for {domain} will expire in {days_to_expire} days."
                    )
                    alerts.append(alert_message)
        except Exception as e:
            print(f"Error checking SSL for {domain}: {e}")
    
    # Print alerts to be captured as output
    print("\n".join(alerts))

if __name__ == "__main__":
    main()
