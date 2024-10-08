from googleapiclient.discovery import build
from datetime import datetime
import pytz

class CalendarService:
    def __init__(self, auth_manager):
        self.auth_manager = auth_manager
        self.service = None

    def _get_service(self):
        if not self.service:
            creds = self.auth_manager.get_credentials()
            self.service = build('calendar', 'v3', credentials=creds)
        return self.service

    def add_event(self, title, url, event_date=None):
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
            print(f"Event created: {event.get('htmlLink')}")
        except Exception as error:
            print(f"An error occurred while creating calendar event: {error}")