"""
Take a screenshot of Yahoo search results for a given query.
Yahoo is used because Google, Bing, DuckDuckGo, Brave, and Startpage
all CAPTCHA headless browsers.

Usage: python yahoo_search_screenshot.py "search query" output.png
"""
import sys
from playwright.sync_api import sync_playwright

query = sys.argv[1]
output_path = sys.argv[2]

with sync_playwright() as p:
    browser = p.chromium.launch(
        args=['--disable-blink-features=AutomationControlled']
    )
    context = browser.new_context(
        viewport={'width': 1280, 'height': 900},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    )
    page = context.new_page()
    page.add_init_script('Object.defineProperty(navigator, "webdriver", {get: () => undefined})')

    url = 'https://search.yahoo.com/search?p=' + query.replace(' ', '+')
    page.goto(url, wait_until='domcontentloaded', timeout=20000)
    page.wait_for_timeout(3000)
    page.screenshot(path=output_path)
    print(f'Saved: {output_path}')
    browser.close()
