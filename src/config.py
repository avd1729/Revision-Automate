import os
from dotenv import load_dotenv


class Config:
    """
    Config class to access the necessary global variables.
    """
    def __init__(self):
        load_dotenv()
        self.EMAIL_ID = os.getenv("EMAIL_ID")
        self.PASS_WD = os.getenv("PASS_WD")
        self.NOTION_KEY = os.getenv("NOTION_KEY")
        self.CREDENTIALS_FILE = 'secrets/credentials.json'
        self.TOKEN_FILE = 'secrets/token.json'
        self.SCOPES = [
            'https://www.googleapis.com/auth/gmail.send',
            'https://www.googleapis.com/auth/calendar',
            'https://www.googleapis.com/auth/calendar.events'
        ]