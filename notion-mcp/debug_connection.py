"""Debug script for Notion connection issues."""

import os
from dotenv import load_dotenv
import httpx

load_dotenv()

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
NOTION_VERSION = "2022-06-28"

headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": NOTION_VERSION,
    "Content-Type": "application/json",
}

print(f"API Key: {NOTION_API_KEY[:10]}...{NOTION_API_KEY[-4:]}")
print(f"Database ID: {NOTION_DATABASE_ID}")
print()

# Try with dashes
db_id_with_dashes = NOTION_DATABASE_ID
# Try without dashes
db_id_no_dashes = NOTION_DATABASE_ID.replace("-", "")

print("=== Test 1: Get database with dashes ===")
with httpx.Client() as client:
    resp = client.get(f"https://api.notion.com/v1/databases/{db_id_with_dashes}", headers=headers)
    print(f"Status: {resp.status_code}")
    if resp.status_code != 200:
        print(f"Error: {resp.text[:200]}")
    else:
        data = resp.json()
        print(f"Database title: {data.get('title', [{}])[0].get('plain_text', 'Unknown')}")

print()
print("=== Test 2: Get database without dashes ===")
with httpx.Client() as client:
    resp = client.get(f"https://api.notion.com/v1/databases/{db_id_no_dashes}", headers=headers)
    print(f"Status: {resp.status_code}")
    if resp.status_code != 200:
        print(f"Error: {resp.text[:200]}")
    else:
        data = resp.json()
        print(f"Database title: {data.get('title', [{}])[0].get('plain_text', 'Unknown')}")

print()
print("=== Test 3: Search for all databases the integration can access ===")
with httpx.Client() as client:
    resp = client.post(
        "https://api.notion.com/v1/search",
        headers=headers,
        json={"filter": {"property": "object", "value": "database"}}
    )
    print(f"Status: {resp.status_code}")
    if resp.status_code == 200:
        data = resp.json()
        results = data.get("results", [])
        print(f"Found {len(results)} database(s):")
        for db in results:
            db_id = db.get("id", "unknown")
            title = db.get("title", [{}])
            title_text = title[0].get("plain_text", "Untitled") if title else "Untitled"
            print(f"  - {title_text} (ID: {db_id})")
    else:
        print(f"Error: {resp.text[:200]}")
