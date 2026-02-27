"""
Open a local file (image, HTML, etc.) in the browser and take a screenshot.

Usage: python file_screenshot.py input_file output.png
"""
import sys
import os
from playwright.sync_api import sync_playwright

input_file = os.path.abspath(sys.argv[1])
output_path = sys.argv[2]

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1280, 'height': 900})
    page.goto(f'file:///{input_file}')
    page.wait_for_timeout(1000)
    page.screenshot(path=output_path)
    print(f'Saved: {output_path}')
    browser.close()
