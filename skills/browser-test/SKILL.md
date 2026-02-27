---
name: browser-test
description: Browser automation for testing web apps and Chrome extensions. Use when you need to navigate websites, interact with pages, take screenshots, test Chrome extensions, fill forms, or extract information from web pages. Combines agent-browser CLI with a Playwright fallback for Windows.
---

# Browser Test — Web & Extension Testing Toolkit

Two approaches available. **Try agent-browser first** (more features). If it fails with socket/daemon errors on Windows, **fall back to the Playwright scripts**.

---

## Approach 1: agent-browser CLI (preferred)

### Quick start

```bash
agent-browser open <url>        # Navigate to page
agent-browser snapshot -i       # Get interactive elements with refs
agent-browser click @e1         # Click element by ref
agent-browser fill @e2 "text"   # Fill input by ref
agent-browser close             # Close browser
```

### Chrome extension testing

```bash
agent-browser --extension ./extension --headed open <url>
# Or set env var: AGENT_BROWSER_EXTENSIONS="./extension"
```

### Core workflow

1. Navigate: `agent-browser open <url>`
2. Snapshot: `agent-browser snapshot -i` (returns elements with refs like `@e1`, `@e2`)
3. Interact using refs from the snapshot
4. Re-snapshot after navigation or significant DOM changes

### Navigation

```bash
agent-browser open <url>      # Navigate to URL (auto-prepends https://)
agent-browser back            # Go back
agent-browser forward         # Go forward
agent-browser reload          # Reload page
agent-browser close           # Close browser
agent-browser connect 9222    # Connect to browser via CDP port
```

### Snapshot (page analysis)

```bash
agent-browser snapshot            # Full accessibility tree
agent-browser snapshot -i         # Interactive elements only (recommended)
agent-browser snapshot -c         # Compact output
agent-browser snapshot -d 3       # Limit depth to 3
agent-browser snapshot -s "#main" # Scope to CSS selector
```

### Interactions (use @refs from snapshot)

```bash
agent-browser click @e1           # Click
agent-browser dblclick @e1        # Double-click
agent-browser focus @e1           # Focus element
agent-browser fill @e2 "text"     # Clear and type
agent-browser type @e2 "text"     # Type without clearing
agent-browser press Enter         # Press key
agent-browser press Control+a     # Key combination
agent-browser hover @e1           # Hover
agent-browser check @e1           # Check checkbox
agent-browser uncheck @e1         # Uncheck checkbox
agent-browser select @e1 "value"  # Select dropdown option
agent-browser scroll down 500     # Scroll page (default: down 300px)
agent-browser scrollintoview @e1  # Scroll element into view
agent-browser drag @e1 @e2        # Drag and drop
agent-browser upload @e1 file.pdf # Upload files
```

### Get information

```bash
agent-browser get text @e1        # Get element text
agent-browser get html @e1        # Get innerHTML
agent-browser get value @e1       # Get input value
agent-browser get attr @e1 href   # Get attribute
agent-browser get title           # Get page title
agent-browser get url             # Get current URL
agent-browser get count ".item"   # Count matching elements
agent-browser get box @e1         # Get bounding box
agent-browser get styles @e1      # Get computed styles
```

### Check state

```bash
agent-browser is visible @e1      # Check if visible
agent-browser is enabled @e1      # Check if enabled
agent-browser is checked @e1      # Check if checked
```

### Screenshots & PDF

```bash
agent-browser screenshot          # Save to a temporary directory
agent-browser screenshot path.png # Save to a specific path
agent-browser screenshot --full   # Full page
agent-browser pdf output.pdf      # Save as PDF
```

### Video recording

```bash
agent-browser record start ./demo.webm    # Start recording
agent-browser click @e1                   # Perform actions
agent-browser record stop                 # Stop and save video
```

### Wait

```bash
agent-browser wait @e1                     # Wait for element
agent-browser wait 2000                    # Wait milliseconds
agent-browser wait --text "Success"        # Wait for text
agent-browser wait --url "**/dashboard"    # Wait for URL pattern
agent-browser wait --load networkidle      # Wait for network idle
agent-browser wait --fn "window.ready"     # Wait for JS condition
```

### Semantic locators (alternative to refs)

```bash
agent-browser find role button click --name "Submit"
agent-browser find text "Sign In" click
agent-browser find label "Email" fill "user@test.com"
agent-browser find placeholder "Search" type "query"
agent-browser find testid "submit-btn" click
```

### Browser settings

```bash
agent-browser set viewport 1920 1080          # Set viewport size
agent-browser set device "iPhone 14"          # Emulate device
agent-browser set geo 37.7749 -122.4194       # Set geolocation
agent-browser set offline on                  # Toggle offline mode
agent-browser set media dark                  # Emulate color scheme
```

### Cookies & Storage

```bash
agent-browser cookies                     # Get all cookies
agent-browser cookies set name value      # Set cookie
agent-browser cookies clear               # Clear cookies
agent-browser storage local               # Get all localStorage
agent-browser storage local key           # Get specific key
agent-browser storage local set k v       # Set value
```

### Network

```bash
agent-browser network route <url>              # Intercept requests
agent-browser network route <url> --abort      # Block requests
agent-browser network route <url> --body '{}'  # Mock response
agent-browser network requests                 # View tracked requests
agent-browser network requests --filter api    # Filter requests
```

### Tabs, Frames, Dialogs

```bash
agent-browser tab                 # List tabs
agent-browser tab new [url]       # New tab
agent-browser tab 2               # Switch to tab by index
agent-browser frame "#iframe"     # Switch to iframe
agent-browser frame main          # Back to main frame
agent-browser dialog accept       # Accept dialog
agent-browser dialog dismiss      # Dismiss dialog
```

### JavaScript

```bash
agent-browser eval "document.title"   # Run JavaScript
```

### Global options

```bash
agent-browser --session <name> ...    # Isolated browser session
agent-browser --json ...              # JSON output for parsing
agent-browser --headed ...            # Show browser window
agent-browser --full ...              # Full page screenshot
agent-browser --cdp <port> ...       # Connect via CDP
agent-browser --proxy <url> ...       # Use proxy server
agent-browser --extension <path> ...  # Load browser extension (repeatable)
```

### Sessions (parallel browsers)

```bash
agent-browser --session test1 open site-a.com
agent-browser --session test2 open site-b.com
agent-browser session list
```

### Debugging

```bash
agent-browser --headed open example.com   # Show browser window
agent-browser console                     # View console messages
agent-browser errors                      # View page errors
agent-browser highlight @e1               # Highlight element
agent-browser trace start                 # Start recording trace
agent-browser trace stop trace.zip        # Stop and save trace
```

### HTTPS Certificate Errors

```bash
agent-browser open https://localhost:8443 --ignore-https-errors
```

### Environment variables

```bash
AGENT_BROWSER_SESSION="mysession"
AGENT_BROWSER_EXECUTABLE_PATH="/path/chrome"
AGENT_BROWSER_EXTENSIONS="/ext1,/ext2"
AGENT_BROWSER_PROVIDER="your-cloud-browser-provider"
```

---

## Approach 2: Playwright Scripts (Windows fallback)

Use these when `agent-browser` daemon fails to start (common on Windows due to socket issues).

**Requires**: `playwright` npm package + `npx playwright install chromium`

### Launch browser with Chrome extension

```bash
# Run in background — starts Chromium with extension loaded, CDP on port 9222
node <project>/.claude/scripts/browser-launch.js &
```

This auto-detects the extension ID and saves state to `.browser-state.json`.

### Commands (while browser is running)

```bash
# Take screenshot (saved to .screenshots/, returns filepath — use Read tool to view)
node <project>/.claude/scripts/browser-cmd.js screenshot [filename.png]

# Get accessibility tree (JSON with roles, names — for finding elements)
node <project>/.claude/scripts/browser-cmd.js snapshot

# Navigate to extension popup (auto-uses detected extension ID)
node <project>/.claude/scripts/browser-cmd.js popup

# Navigate to any URL
node <project>/.claude/scripts/browser-cmd.js navigate <url>

# Click by CSS selector
node <project>/.claude/scripts/browser-cmd.js click <selector>

# Click by accessibility role
node <project>/.claude/scripts/browser-cmd.js click-role button "Start Work Session"

# Fill an input
node <project>/.claude/scripts/browser-cmd.js fill <selector> <text>

# Get text content
node <project>/.claude/scripts/browser-cmd.js text [selector]

# Run JavaScript on page
node <project>/.claude/scripts/browser-cmd.js eval "document.title"

# List open pages
node <project>/.claude/scripts/browser-cmd.js pages

# Switch to page by index
node <project>/.claude/scripts/browser-cmd.js switch <index>

# Get current URL
node <project>/.claude/scripts/browser-cmd.js url

# Wait milliseconds
node <project>/.claude/scripts/browser-cmd.js wait <ms>

# Close current page
node <project>/.claude/scripts/browser-cmd.js close-page
```

### Typical Playwright workflow

1. Launch browser in background: `node <project>/.claude/scripts/browser-launch.js &`
2. Open the popup: `node <project>/.claude/scripts/browser-cmd.js popup`
3. Screenshot to see it: `node <project>/.claude/scripts/browser-cmd.js screenshot popup.png`
4. View screenshot: use Read tool on `.screenshots/popup.png`
5. Click a button: `node <project>/.claude/scripts/browser-cmd.js click-role button "Start Work Session"`
6. Screenshot again to verify
7. Navigate to test blocking: `node <project>/.claude/scripts/browser-cmd.js navigate https://youtube.com`
8. Screenshot to verify redirect to blocked.html

### Playwright script files

- `<project>/.claude/scripts/browser-launch.js` — Launcher (persistent context + CDP)
- `<project>/.claude/scripts/browser-cmd.js` — Command runner (connects via CDP)
- `.browser-state.json` — Runtime state (extension ID, port, PID)
- `.screenshots/` — Screenshots directory
- `.browser-profile/` — Chromium user data directory

### Troubleshooting

- "Failed to connect" → Browser not running, launch it first
- Extension ID wrong → Check `.browser-state.json` after launch
- Screenshots blank → Page may not be loaded yet, add `wait 1000` before screenshot

---

## Extension testing tips

- **Popup**: Can't interact with toolbar popup bubble directly. Open `chrome-extension://<id>/popup.html` as a full page instead.
- **Extension ID**: After loading, find it from `chrome://extensions` or `.browser-state.json` (Playwright approach auto-detects it).
- **Service worker**: Debug indirectly — verify effects (storage changes, network requests, DOM modifications) rather than inspecting the worker itself.
- **Webcam/media**: Use `agent-browser set` commands or Playwright launch args for media permissions.

For extension-specific debugging patterns (storage inspection, hidden elements, manifest issues, multi-worktree testing), see `~/.claude/skills/chrome-ext-test/SKILL.md`.
