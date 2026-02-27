"""Generate a PDF from a markdown file with embedded images.

Reads a markdown file, finds backtick-only lines referencing image files
(e.g., `diagram.png`), replaces them with base64-encoded <img> tags,
converts to HTML, and renders to PDF via Playwright.

Usage:
    python generate_pdf.py <markdown_file> <output_pdf>

Requirements:
    pip install markdown playwright
    playwright install chromium
"""
import sys
import os
import re
import base64
import asyncio

try:
    import markdown
except ImportError:
    print("ERROR: 'markdown' package not installed. Run: pip install markdown")
    sys.exit(1)


def read_markdown(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def embed_images(md_text, files_dir):
    """Replace backtick-only lines referencing images with base64 <img> tags."""
    lines = md_text.split("\n")
    result = []
    img_extensions = (".png", ".jpg", ".jpeg", ".gif", ".bmp", ".svg")

    for line in lines:
        stripped = line.strip()
        # Match lines that are just a backtick reference to an image file
        match = re.match(r"^`([^`]+)`$", stripped)
        if match:
            filename = match.group(1)
            if filename.lower().endswith(img_extensions):
                img_path = os.path.join(files_dir, filename)
                if os.path.exists(img_path):
                    ext = os.path.splitext(filename)[1].lower().lstrip(".")
                    if ext == "svg":
                        mime = "image/svg+xml"
                    elif ext in ("jpg", "jpeg"):
                        mime = "image/jpeg"
                    else:
                        mime = f"image/{ext}"
                    with open(img_path, "rb") as img_f:
                        b64 = base64.b64encode(img_f.read()).decode("utf-8")
                    result.append(
                        f'<img src="data:{mime};base64,{b64}" '
                        f'alt="{filename}" style="max-width:100%; display:block; '
                        f'margin: 1em auto;" />'
                    )
                    continue
                else:
                    print(f"WARNING: Image not found: {img_path}")
        result.append(line)

    return "\n".join(result)


def md_to_html(md_text):
    """Convert markdown to HTML with a clean template."""
    html_body = markdown.markdown(md_text, extensions=["extra", "tables"])
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
    body {{
        font-family: Arial, Helvetica, sans-serif;
        font-size: 12pt;
        line-height: 1.5;
        max-width: 7.5in;
        margin: 0 auto;
        padding: 0.5in;
        color: #222;
    }}
    h1 {{ font-size: 18pt; margin-top: 1.2em; }}
    h2 {{ font-size: 15pt; margin-top: 1em; }}
    h3 {{ font-size: 13pt; margin-top: 0.8em; }}
    table {{
        border-collapse: collapse;
        width: 100%;
        margin: 1em 0;
        font-size: 10pt;
    }}
    th, td {{
        border: 1px solid #ccc;
        padding: 6px 10px;
        text-align: left;
    }}
    th {{ background-color: #f5f5f5; font-weight: bold; }}
    img {{
        max-width: 100%;
        display: block;
        margin: 1em auto;
        page-break-inside: avoid;
    }}
    hr {{ border: none; border-top: 1px solid #ddd; margin: 1.5em 0; }}
    code {{
        background: #f4f4f4;
        padding: 2px 5px;
        border-radius: 3px;
        font-size: 0.9em;
    }}
</style>
</head>
<body>
{html_body}
</body>
</html>"""


async def html_to_pdf(html_content, output_path):
    """Render HTML to PDF using Playwright."""
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        print("ERROR: 'playwright' package not installed. Run: pip install playwright && playwright install chromium")
        sys.exit(1)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.set_content(html_content, wait_until="networkidle")
        await page.pdf(
            path=output_path,
            format="Letter",
            margin={"top": "0.5in", "bottom": "0.5in", "left": "0.5in", "right": "0.5in"},
            print_background=True,
        )
        await browser.close()


def main():
    if len(sys.argv) < 3:
        print(f"Usage: python {sys.argv[0]} <markdown_file> <output_pdf>")
        sys.exit(1)

    md_path = sys.argv[1]
    pdf_path = sys.argv[2]

    if not os.path.exists(md_path):
        print(f"ERROR: Markdown file not found: {md_path}")
        sys.exit(1)

    # Determine files/ directory (sibling to markdown file or subfolder)
    md_dir = os.path.dirname(os.path.abspath(md_path))
    files_dir = os.path.join(md_dir, "files")
    if not os.path.isdir(files_dir):
        files_dir = md_dir  # fall back to same directory

    print(f"Reading: {md_path}")
    print(f"Images dir: {files_dir}")

    md_text = read_markdown(md_path)
    md_with_images = embed_images(md_text, files_dir)
    html = md_to_html(md_with_images)

    print(f"Generating PDF: {pdf_path}")
    asyncio.run(html_to_pdf(html, pdf_path))

    size_kb = os.path.getsize(pdf_path) / 1024
    print(f"Done. PDF saved: {pdf_path} ({size_kb:.0f} KB)")


if __name__ == "__main__":
    main()
