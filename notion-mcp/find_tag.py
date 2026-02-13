"""Find tags matching a pattern."""

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

with httpx.Client(timeout=30) as client:
    resp = client.get(f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}", headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        props = data.get("properties", {})
        tags_prop = props.get("Tags", {})
        options = tags_prop.get("multi_select", {}).get("options", [])

        print(f"Total tags: {len(options)}")
        print()

        # Search for matching tags
        search_terms = ["project", "programming", "idea", "code", "dev"]
        print("Tags containing 'project', 'programming', 'idea', 'code', or 'dev':")
        found = []
        for opt in options:
            name = opt.get("name", "")
            name_lower = name.lower()
            if any(term in name_lower for term in search_terms):
                found.append(name)
                print(f"  - {name}")

        if not found:
            print("  (none found)")
            print()
            print("All available tags:")
            for opt in options:
                print(f"  - {opt.get('name')}")
