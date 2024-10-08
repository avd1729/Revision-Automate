import os
import requests
import json
import pandas as pd
import datetime
import pytz
from googleapiclient.discovery import build
from dotenv import load_dotenv
import base64
# import google.auth
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email.mime.text import MIMEText


load_dotenv()
EMAIL_ID = os.getenv("EMAIL_ID")
PASS_WD = os.getenv("PASS_WD")
NOTION_KEY = os.getenv("NOTION_KEY")

headers = {
    'Authorization': f"Bearer {NOTION_KEY}",
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28'
}

def fetch_all_pages():
    all_results = []
    next_cursor = None
    has_more = True

    while has_more:
        search_params = {
            "page_size": 100,  # Notion's max limit per request
            "filter": {"value": "page", "property": "object"}
        }

        if next_cursor:
            search_params["start_cursor"] = next_cursor

        search_response = requests.post(
            f'https://api.notion.com/v1/search',
            json=search_params,
            headers=headers
        )

        search_response_data = search_response.json()
        all_results.extend(search_response_data.get('results', []))
        next_cursor = search_response_data.get('next_cursor')
        has_more = search_response_data.get('has_more')

    return all_results

results = fetch_all_pages()

json_file = "out/response_output.json"
with open(json_file, 'w') as file:
    json.dump(results, file, indent=4)

print(f"JSON file '{json_file}' created successfully!")

file_path = "C:/Users/Aravind/PROJECTS/notion-dsa-reminder-workflow/out/response_output.json"

with open(file_path, 'r') as file:
    data = json.load(file)

df = pd.DataFrame(data)

new_df = pd.DataFrame({
    "Date": df["properties"].apply(lambda x: x["Date"]["date"]["start"] if x["Date"] and x["Date"]["date"] else None),
    "Problem Title": df["properties"].apply(lambda x: x["Problem"]["title"][0]["text"]["content"] if x["Problem"] and x["Problem"]["title"] else None),
    "URL":df['url']
})

new_df['Date'] = pd.to_datetime(new_df['Date'])

# Sorting the dataframe by 'Date'
sorted_df = new_df.sort_values(by='Date')



# Function to create a subset of the DataFrame
def create_date_subsets(df):
    # Getting the current date
    current_date = pd.to_datetime('2024-05-10')
    
    # Creating time intervals
    two_days_before = current_date - pd.Timedelta(days=2)
    seven_days_before = current_date - pd.Timedelta(days=7)
    fourteen_days_before = current_date - pd.Timedelta(days=14)
    thirty_days_before = current_date - pd.Timedelta(days=30)
    
    # Filtering the dataframe based on the date ranges
    df_filtered = df[
        (df['Date'] == two_days_before) |
        (df['Date'] == seven_days_before) |
        (df['Date'] == fourteen_days_before) |
        (df['Date'] == thirty_days_before)
    ]
    
    return df_filtered

filtered_df = create_date_subsets(sorted_df)



# Function to format the DataFrame data into a readable email format
def format_dataframe(df):
    email_body = ""
    for idx, row in df.iterrows():
        email_body += f"Question {idx + 1}:\n"
        email_body += f"Date: {row['Date'].strftime('%Y-%m-%d')}\n"
        email_body += f"Problem Title: {row['Problem Title']}\n"
        email_body += f"URL: {row['URL']}\n"  # You can replace with actual URLs if available
        email_body += "\n"  # Line break between questions
    return email_body

# Get the current date for the email subject
current_date = datetime.datetime.now().strftime('%Y-%m-%d')
subject = f"DSA Reminder - {current_date}"


def add_event_to_calendar(creds, title, url):
    service = build('calendar', 'v3', credentials=creds)
    
    utc_now = datetime.datetime.now(pytz.utc)  # Get the current UTC time
    current_date = utc_now.date()
    event_date = current_date.strftime('%Y-%m-%d')

    # Create the event with title and description including the URL
    event = {
        'summary': title,
        'description': f'Problem URL: {url}',  # Include URL in the description
        'start': {
            'date': event_date,  # All-day event using current date
            'timeZone': 'UTC',   # Adjust timezone as needed
        },
        'end': {
            'date': event_date,  # All-day event using current date
            'timeZone': 'UTC',
        },
    }
    
    # Insert the event into the user's calendar
    event = service.events().insert(calendarId='primary', body=event).execute()
    print(f"Event created: {event.get('htmlLink')}")

# Define the scope for Gmail API
SCOPES = [
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/calendar.events'
]


# Path to credentials.json from the Google Cloud Console
CREDENTIALS_FILE = 'C:/Users/Aravind/PROJECTS/notion-dsa-reminder-workflow/secrets/credentials.json'

# Function to authenticate and get the credentials
def authenticate():
    creds = None
    token_file = 'C:/Users/Aravind/PROJECTS/notion-dsa-reminder-workflow/secrets/token.json'

    # Load previously stored credentials if they exist
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)

    # If no valid credentials are available, ask the user to log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for future use
        with open(token_file, 'w') as token:
            token.write(creds.to_json())

    return creds

# Function to send an email
def send_email(creds, sender_email, recipient_email, subject, body):
    service = build('gmail', 'v1', credentials=creds)

    # Create the email message
    message = MIMEText(body)
    message['to'] = recipient_email
    message['from'] = sender_email
    message['subject'] = subject

    # Encode the message
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    message_body = {'raw': raw}

    # Send the email
    try:
        message = service.users().messages().send(userId='me', body=message_body).execute()
        print(f"Message sent successfully! Message Id: {message['id']}")
    except Exception as error:
        print(f"An error occurred: {error}")

if __name__ == '__main__':
    
    # Assuming 'subset_df' is the filtered DataFrame
    sender = "your_email@gmail.com"
    recipient = EMAIL_ID
    
    # Generate email body from the DataFrame
    body = format_dataframe(filtered_df)

    # Get the current date for the email subject
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    subject = f"DSA Reminder - {current_date}"

    # Authenticate and send the email
    creds = authenticate()
    for idx, row in filtered_df.iterrows():
        title = row['Problem Title']
        url = row['URL']  # Fetch the URL from the DataFrame
        
        # Add event to calendar
        add_event_to_calendar(creds, title, url)  # Always creates for today
    send_email(creds, sender, recipient, subject, body)
