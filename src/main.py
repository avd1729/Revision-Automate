import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

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
