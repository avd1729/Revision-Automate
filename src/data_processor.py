import pandas as pd
from datetime import datetime, timedelta

class DataProcessor:
    def process_notion_data(self, notion_pages):
        df = pd.DataFrame(notion_pages)
        return pd.DataFrame({
            "Date": df["properties"].apply(lambda x: x["Date"]["date"]["start"] if x["Date"] and x["Date"]["date"] else None),
            "Problem Title": df["properties"].apply(lambda x: x["Problem"]["title"][0]["text"]["content"] if x["Problem"] and x["Problem"]["title"] else None),
            "URL": df['url']
        })

    def filter_data_by_date(self, df, current_date=None):
        df['Date'] = pd.to_datetime(df['Date'])
        if current_date is None:
            current_date = datetime.now().date()
        else:
            current_date = pd.to_datetime(current_date).date()
        
        date_ranges = [2, 7, 14, 30]
        return df[df['Date'].dt.date.isin([current_date - timedelta(days=d) for d in date_ranges])]

    def format_email_body(self, df):
        email_body = ""
        for idx, row in df.iterrows():
            email_body += f"Question {idx + 1}:\n"
            email_body += f"Date: {row['Date'].strftime('%Y-%m-%d')}\n"
            email_body += f"Problem Title: {row['Problem Title']}\n"
            email_body += f"URL: {row['URL']}\n\n"
        return email_body