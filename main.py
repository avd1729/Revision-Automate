from src.config import Config
from src.notion_client import NotionClient
from src.data_processor import DataProcessor
from src.email_service import EmailService
from src.calendar_service import CalendarService
from src.auth_manager import AuthManager
import pandas as pd

def main():
    # Set the test date
    test_date = pd.to_datetime('2024-05-10')

    config = Config()
    auth_manager = AuthManager(config)
    
    notion_client = NotionClient(config.NOTION_KEY)
    data_processor = DataProcessor()
    email_service = EmailService(auth_manager)
    calendar_service = CalendarService(auth_manager)

    # Fetch and process Notion data
    notion_pages = notion_client.fetch_all_pages()
    processed_data = data_processor.process_notion_data(notion_pages)
    filtered_data = data_processor.filter_data_by_date(processed_data, current_date=test_date)

    if not filtered_data.empty:
        # Send email
        email_body = data_processor.format_email_body(filtered_data)
        sender = "your_email@gmail.com"
        email_service.send_email(sender, config.EMAIL_ID, f"DSA Reminder - {test_date.strftime('%Y-%m-%d')}", email_body)

        # Add events to calendar
        for _, row in filtered_data.iterrows():
            calendar_service.add_event(row['Problem Title'], row['URL'], event_date=test_date)
    else:
        print(f"No reminders for {test_date.strftime('%Y-%m-%d')}.")

if __name__ == "__main__":
    main()