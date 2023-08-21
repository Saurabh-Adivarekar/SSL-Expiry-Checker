import ssl
import socket
import datetime
import os
import sys

def get_remaining_days(expiry_date):
    today = datetime.datetime.now()
    remaining_days = (expiry_date - today).days
    return remaining_days

def main():
    domains = sys.argv[1].split(",")
    
    for domain in domains:
        try:
            ctx = ssl.create_default_context()
            with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
                s.con                print(f"Domain: {domain}")
                print(f"Days to expire: {days_to_expire}")
                
                if days_to_expire <= 30:
                    print("SSL certificate is expiring soon!")
        except Exception as e:
            print(f"Error checking SSL for {domain}: {e}")

if __name__ == "__main__":
    main()


