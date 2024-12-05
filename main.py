from src.config import Config
from src.notion_client import NotionClient
from src.data_processor import DataProcessor
from src.email_service import EmailService
from src.calendar_service import CalendarService
from src.auth_manager import AuthManager
from src.logger_manager import LoggerManager
from datetime import datetime
# import pandas as pd

def main():

    # Initialize logger (will ensure only one instance)
    logger_manager = LoggerManager()
    logger = logger_manager.get_logger()
    logger.info("Application started.")
    
    current_date = datetime.now().date()
    logger.info(f"Date set to {current_date.strftime('%Y-%m-%d')}")

    config = Config()
    auth_manager = AuthManager(config)
    
    notion_client = NotionClient(config.NOTION_KEY)
    data_processor = DataProcessor()
    email_service = EmailService(auth_manager)
    calendar_service = CalendarService(auth_manager)

    # Fetch and process Notion data
    logger.info("Fetching pages from Notion...")
    notion_pages = notion_client.fetch_all_pages()
    
    logger.info("Processing Notion data...")
    processed_data = data_processor.process_notion_data(notion_pages)

    logger.info(f"Filtering data by current date - {current_date} ...")
    filtered_data = data_processor.filter_data_by_date(processed_data, current_date)

    if not filtered_data.empty:
        logger.info(f"Found {len(filtered_data)} reminders for {current_date.strftime('%Y-%m-%d')}")

        # Send email
        email_body = data_processor.format_email_body(filtered_data)
        sender = "your_email@gmail.com"
        logger.info("Sending email...")
        email_service.send_email(sender, config.EMAIL_ID, f"DSA Reminder - {current_date.strftime('%Y-%m-%d')}", email_body)

        # Add events to calendar
        logger.info("Adding events to calendar...")
        for _, row in filtered_data.iterrows():
            # Log the problem title and URL
            problem_title = row['Problem Title']
            problem_url = row['URL']
            # Add the event to the calendar
            calendar_service.add_event(problem_title, problem_url)
    else:
        logger.info(f"No reminders for {current_date.strftime('%Y-%m-%d')}.")

if __name__ == "__main__":
    main()
