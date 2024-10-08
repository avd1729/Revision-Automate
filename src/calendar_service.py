from googleapiclient.discovery import build
from datetime import datetime
import pytz
from src.logger_manager import LoggerManager


class CalendarService:

    """
    Service to create calendar events for the revision questions.
    """

    def __init__(self, auth_manager):
        self.auth_manager = auth_manager
        self.service = None
        self.logger = LoggerManager().get_logger()

    
    def _get_service(self):

        """
        Authenticate for creating calendar events.

        Returns:
            service : Authentication handle.
        """
        
        if not self.service:
            creds = self.auth_manager.get_credentials()
            self.service = build('calendar', 'v3', credentials=creds)
        return self.service

    def add_event(self, title, url, event_date=None):
        
        """
        Create events in calendar.
        
        Args:
            title (str) : Title of the Event.
            url (str) : URL of the revision problem.
            event_date (datetime) : Current date.

        """
        
        service = self._get_service()

        if event_date is None:
            event_date = datetime.now(pytz.utc).date()
        else:
            event_date = event_date.date()

        event_date_str = event_date.strftime('%Y-%m-%d')

        event = {
            'summary': title,
            'description': f'Problem URL: {url}',
            'start': {
                'date': event_date_str,
                'timeZone': 'UTC',
            },
            'end': {
                'date': event_date_str,
                'timeZone': 'UTC',
            },
        }

        try:
            event = service.events().insert(calendarId='primary', body=event).execute()
            self.logger.info(f"Event created: {event.get('htmlLink')}")
        except Exception as error:
            self.logger.error(f"An error occurred while creating calendar event for '{title}': {error}")
