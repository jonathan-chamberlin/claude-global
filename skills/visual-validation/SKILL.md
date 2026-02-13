---
name: visual-validation
description: Take screenshots of web pages and validate visual appearance. Use when the user asks to check how something looks, verify UI changes, or capture a web page state.
---

Capture and analyze screenshots of web pages to validate visual appearance.

## Workflow

1. **Navigate** — Open the target URL using agent-browser or Playwright
2. **Wait** — Let the page fully load (wait for network idle)
3. **Screenshot** — Capture the page to a temporary PNG file
4. **Analyze** — Read the screenshot image (Claude is multimodal) and check for:
   - Layout issues (overlapping elements, broken alignment)
   - Text visibility and readability
   - Color contrast problems
   - Missing elements or broken images
   - Responsive layout issues
5. **Report** — Describe findings with specific element references

## Comparison Mode

For validating changes:
1. Take a "before" screenshot
2. Apply the code changes
3. Take an "after" screenshot
4. Read both images and compare visually
5. Report what changed and whether it looks correct

## Screenshot Methods

### Method 1: agent-browser (if available)
```bash
agent-browser open <url>
agent-browser screenshot <output-path>
```

### Method 2: Playwright Python (fallback)
```bash
python -c "
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1280, 'height': 720})
    page.goto('URL_HERE')
    page.wait_for_load_state('networkidle')
    page.screenshot(path='screenshot.png', full_page=True)
    browser.close()
"
```

### Method 3: Node.js Playwright
```bash
node -e "
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
  await page.goto('URL_HERE');
  await page.waitForLoadState('networkidle');
  await page.screenshot({ path: 'screenshot.png', fullPage: true });
  await browser.close();
})();
"
```

## Common Checks

- **Text visibility**: All text should be readable against its background
- **Color contrast**: WCAG AA minimum 4.5:1 for normal text, 3:1 for large text
- **Responsive**: Check at common breakpoints (320px, 768px, 1024px, 1280px)
- **Element alignment**: Headers, buttons, inputs should be aligned consistently
- **Image loading**: All images should render (no broken image icons)

## Notes

- Always save screenshots to a temporary location, not the repo
- Delete screenshots after analysis to avoid repo bloat
- For animated content, take multiple screenshots with delays
