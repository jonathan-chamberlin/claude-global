"""Inspect database properties and sample data."""

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

print("=== Database Properties ===")
with httpx.Client(timeout=30) as client:
    resp = client.get(f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}", headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        title = data.get("title", [{}])
        title_text = title[0].get("plain_text", "Untitled") if title else "Untitled"
        print(f"Database: {title_text}")
        print()
        print("Properties:")
        props = data.get("properties", {})
        for name, prop in props.items():
            prop_type = prop.get("type", "unknown")
            print(f"  - {name} ({prop_type})")
            if prop_type == "multi_select":
                options = prop.get("multi_select", {}).get("options", [])
                if options:
                    print(f"    Options: {[o.get('name') for o in options[:10]]}")
                    if len(options) > 10:
                        print(f"    ... and {len(options) - 10} more")
            elif prop_type == "select":
                options = prop.get("select", {}).get("options", [])
                if options:
                    print(f"    Options: {[o.get('name') for o in options[:10]]}")
    else:
        print(f"Error: {resp.status_code} - {resp.text[:200]}")

print()
print("=== Sample Pages (first 5) ===")
with httpx.Client(timeout=30) as client:
    resp = client.post(
        f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query",
        headers=headers,
        json={"page_size": 5}
    )
    if resp.status_code == 200:
        data = resp.json()
        pages = data.get("results", [])
        print(f"Total pages in response: {len(pages)}")
        for page in pages:
            props = page.get("properties", {})
            # Find title
            title = "Untitled"
            for prop in props.values():
                if prop.get("type") == "title":
                    title_arr = prop.get("title", [])
                    if title_arr:
                        title = title_arr[0].get("plain_text", "Untitled")
                    break
            # Find Tags
            tags = []
            if "Tags" in props:
                tag_prop = props["Tags"]
                if tag_prop.get("type") == "multi_select":
                    tags = [t.get("name") for t in tag_prop.get("multi_select", [])]
            print(f"  - {title}")
            print(f"    Tags: {tags}")
    else:
        print(f"Error: {resp.status_code} - {resp.text[:200]}")
