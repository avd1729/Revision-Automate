from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64

class EmailService:
    def __init__(self, auth_manager):
        self.auth_manager = auth_manager
        self.service = None

    def _get_service(self):
        if not self.service:
            creds = self.auth_manager.get_credentials()
            self.service = build('gmail', 'v1', credentials=creds)
        return self.service

    def send_email(self, sender, recipient, subject, body):
        service = self._get_service()

        message = MIMEText(body)
        message['to'] = recipient
        message['from'] = sender
        message['subject'] = subject

        raw = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        message_body = {'raw': raw}

        try:
            message = service.users().messages().send(userId='me', body=message_body).execute()
            print(f"Message sent successfully! Message Id: {message['id']}")
        except Exception as error:
            print(f"An error occurred while sending email: {error}")