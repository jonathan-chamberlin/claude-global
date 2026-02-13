"""Test script for Notion MCP server functionality."""

import os
import sys
from dotenv import load_dotenv

# Add the server directory to path
sys.path.insert(0, os.path.dirname(__file__))

load_dotenv()

from server import list_project_ideas, read_project_idea, NOTION_API_KEY, NOTION_DATABASE_ID

def test_config():
    """Test that configuration is loaded."""
    print("=== Testing Configuration ===")
    assert NOTION_API_KEY and NOTION_API_KEY != "your_integration_secret_here", "API key not set"
    assert NOTION_DATABASE_ID, "Database ID not set"
    print(f"API Key: {NOTION_API_KEY[:10]}...{NOTION_API_KEY[-4:]}")
    print(f"Database ID: {NOTION_DATABASE_ID}")
    print("[OK] Configuration loaded\n")

def test_list_ideas():
    """Test listing project ideas."""
    print("=== Testing list_project_ideas ===")
    result = list_project_ideas()
    print(result)
    print()
    return result

def test_read_idea(page_id: str):
    """Test reading a specific idea."""
    print(f"=== Testing read_project_idea ({page_id}) ===")
    result = read_project_idea(page_id)
    print(result[:500] + "..." if len(result) > 500 else result)
    print()

def main():
    print("Notion MCP Server Test\n")

    # Test config
    test_config()

    # Test listing
    result = test_list_ideas()

    # If we found ideas, try reading the first one
    if "ID:" in result:
        # Extract first page ID
        import re
        match = re.search(r"ID: ([a-f0-9-]+)", result)
        if match:
            page_id = match.group(1)
            test_read_idea(page_id)

    print("=== All tests completed ===")

if __name__ == "__main__":
    main()
