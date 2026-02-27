"""
Render text/HTML content in the browser and take a screenshot.
Useful for screenshotting raw file contents, code output, etc.
Auto-crops whitespace after rendering.

Usage: python content_screenshot.py input_file output.png [--full] [--no-crop]
  --full: full-page screenshot (default: viewport only)
  --no-crop: skip auto-cropping whitespace
"""
import sys
from playwright.sync_api import sync_playwright

input_file = sys.argv[1]
output_path = sys.argv[2]
full_page = '--full' in sys.argv
no_crop = '--no-crop' in sys.argv

with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Escape HTML special chars for safe rendering in <pre>
content = content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1280, 'height': 900})
    page.set_content(f'<pre style="font-size:12px;padding:20px;">{content}</pre>')
    page.screenshot(path=output_path, full_page=full_page)
    browser.close()

# Auto-crop whitespace
if not no_crop:
    try:
        from PIL import Image, ImageOps
        img = Image.open(output_path)
        inv = ImageOps.invert(img.convert('RGB'))
        bbox = inv.getbbox()
        if bbox:
            padding = 20
            left = max(0, bbox[0] - padding)
            top = max(0, bbox[1] - padding)
            right = min(img.width, bbox[2] + padding)
            bottom = min(img.height, bbox[3] + padding)
            cropped = img.crop((left, top, right, bottom))
            cropped.save(output_path)
            print(f'Saved (cropped {img.size} -> {cropped.size}): {output_path}')
        else:
            print(f'Saved (no content to crop): {output_path}')
    except ImportError:
        print(f'Saved (Pillow not available, skipped crop): {output_path}')
else:
    print(f'Saved: {output_path}')
