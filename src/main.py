import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
NOTION_KEY = os.getenv("NOTION_KEY")
headers = {'Authorization': f"Bearer {NOTION_KEY}", 
           'Content-Type': 'application/json', 
           'Notion-Version': '2022-06-28'}
search_params = {"filter": {"value": "page", "property": "object"}}
search_response = requests.post(
    f'https://api.notion.com/v1/search', 
    json=search_params, headers=headers)

# print(search_response.json())
search_response_data = search_response.json()
json_file = "out/response_output.json"

with open(json_file, 'w') as file:
    json.dump(search_response_data, file, indent=4) 

print(f"JSON file '{json_file}' created successfully!")