"""Notion MCP Server - Access Project Programming Ideas from Notion."""

import os
from dotenv import load_dotenv
import httpx
from mcp.server.fastmcp import FastMCP

load_dotenv()

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
NOTION_VERSION = "2022-06-28"

mcp = FastMCP("notion-ideas")


def notion_request(method: str, endpoint: str, json_data: dict = None) -> dict:
    """Make a request to the Notion API."""
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }
    url = f"https://api.notion.com/v1{endpoint}"

    with httpx.Client() as client:
        if method == "GET":
            response = client.get(url, headers=headers)
        elif method == "POST":
            response = client.post(url, headers=headers, json=json_data or {})
        else:
            raise ValueError(f"Unsupported method: {method}")

        response.raise_for_status()
        return response.json()


def extract_title(page: dict) -> str:
    """Extract the title from a Notion page."""
    props = page.get("properties", {})
    for prop in props.values():
        if prop.get("type") == "title":
            title_array = prop.get("title", [])
            if title_array:
                return "".join(t.get("plain_text", "") for t in title_array)
    return "Untitled"


def extract_text_from_block(block: dict) -> str:
    """Extract plain text from a Notion block."""
    block_type = block.get("type")
    if not block_type:
        return ""

    block_data = block.get(block_type, {})

    # Handle rich text blocks
    if "rich_text" in block_data:
        return "".join(t.get("plain_text", "") for t in block_data["rich_text"])

    # Handle special block types
    if block_type == "child_page":
        return f"[Child Page: {block_data.get('title', 'Untitled')}]"
    if block_type == "child_database":
        return f"[Child Database: {block_data.get('title', 'Untitled')}]"
    if block_type == "image":
        return "[Image]"
    if block_type == "divider":
        return "---"
    if block_type == "table_of_contents":
        return "[Table of Contents]"

    return ""


@mcp.tool()
def list_project_ideas() -> str:
    """List all pages tagged with 'Project Programming Idea' from the Notion database.

    Returns a list of project ideas with their IDs and titles.
    """
    query = {
        "filter": {
            "property": "Tags",
            "multi_select": {
                "contains": "Project Programming Idea"
            }
        }
    }

    try:
        result = notion_request("POST", f"/databases/{NOTION_DATABASE_ID}/query", query)
        pages = result.get("results", [])

        if not pages:
            return "No project ideas found with the 'Project Programming Idea' tag."

        output = []
        for page in pages:
            page_id = page["id"]
            title = extract_title(page)
            output.append(f"- {title} (ID: {page_id})")

        return f"Found {len(pages)} project idea(s):\n" + "\n".join(output)

    except httpx.HTTPStatusError as e:
        return f"Error querying Notion: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
def read_project_idea(page_id: str) -> str:
    """Read the full content of a project idea page from Notion.

    Args:
        page_id: The Notion page ID (from list_project_ideas)

    Returns the page title and all text content.
    """
    try:
        # Get page metadata
        page = notion_request("GET", f"/pages/{page_id}")
        title = extract_title(page)

        # Get page content (blocks)
        blocks_result = notion_request("GET", f"/blocks/{page_id}/children")
        blocks = blocks_result.get("results", [])

        content_lines = [f"# {title}\n"]

        for block in blocks:
            block_type = block.get("type", "")
            text = extract_text_from_block(block)

            if not text:
                continue

            # Format based on block type
            if block_type == "heading_1":
                content_lines.append(f"\n## {text}\n")
            elif block_type == "heading_2":
                content_lines.append(f"\n### {text}\n")
            elif block_type == "heading_3":
                content_lines.append(f"\n#### {text}\n")
            elif block_type == "bulleted_list_item":
                content_lines.append(f"- {text}")
            elif block_type == "numbered_list_item":
                content_lines.append(f"1. {text}")
            elif block_type == "to_do":
                checked = block.get("to_do", {}).get("checked", False)
                checkbox = "[x]" if checked else "[ ]"
                content_lines.append(f"- {checkbox} {text}")
            elif block_type == "code":
                lang = block.get("code", {}).get("language", "")
                content_lines.append(f"\n```{lang}\n{text}\n```\n")
            elif block_type == "quote":
                content_lines.append(f"> {text}")
            elif block_type == "callout":
                content_lines.append(f"> **Note:** {text}")
            else:
                content_lines.append(text)

        return "\n".join(content_lines)

    except httpx.HTTPStatusError as e:
        return f"Error reading page: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    mcp.run()
