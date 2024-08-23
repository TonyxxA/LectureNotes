from dotenv import load_dotenv
import os


class SecurityServices:
    def __init__(self):
        load_dotenv()
        self.username = os.getenv("APP_USERNAME")
        self.password = os.getenv("APP_PASSWORD")
        self.allowed_ips = os.getenv("ALLOWED_IPS").split(",")

    def check_auth(self, username: str, password: str) -> bool:
        return username == self.username and password == self.password

    def check_ip(self, ip: str) -> bool:
        return ip in self.allowed_ips
