from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64
from src.logger_manager import LoggerManager

class EmailService:

    """
    Service to send Email.
    """

    def __init__(self, auth_manager):
        self.auth_manager = auth_manager
        self.service = None
        self.logger = LoggerManager().get_logger()

    def _get_service(self):

        """
        Authenticate for sending email.

        Returns:
            service : Authentication handle.
        """
    
        if not self.service:
            creds = self.auth_manager.get_credentials()
            self.service = build('gmail', 'v1', credentials=creds)
        return self.service

    def send_email(self, sender, recipient, subject, body):

        """
        Send Email with the questions to be revised for the current date.
        
        Args:
            sender (str) : Email-ID of the sender.
            recipient (str) : Email-ID of the recipient.
            subject (str) : Subject of the Email.
            body (str) : Body of the Email.

        """
    
        service = self._get_service()

        message = MIMEText(body)
        message['to'] = recipient
        message['from'] = sender
        message['subject'] = subject

        raw = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        message_body = {'raw': raw}

        try:
            message = service.users().messages().send(userId='me', body=message_body).execute()
            self.logger.info(f"Email sent successfully to {recipient}. Message Id: {message['id']}")
        except Exception as error:
            self.logger.error(f"An error occurred while sending email to {recipient}: {error}")
