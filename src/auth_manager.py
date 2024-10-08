import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class AuthManager:
    def __init__(self, config):
        self.config = config
        self.creds = None

    def get_credentials(self):
        if os.path.exists(self.config.TOKEN_FILE):
            self.creds = Credentials.from_authorized_user_file(self.config.TOKEN_FILE, self.config.SCOPES)
        
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.config.CREDENTIALS_FILE, self.config.SCOPES)
                self.creds = flow.run_local_server(port=0)

            with open(self.config.TOKEN_FILE, 'w') as token:
                token.write(self.creds.to_json())

        return self.creds