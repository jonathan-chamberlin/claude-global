---
name: chrome-ext-test
description: Debug and test Chrome/Chromium extensions using Playwright. Use when verifying extension popup UI, testing button clicks, checking tab navigation, debugging service workers, or visually validating extension changes. Triggers on "test the extension", "check the popup", "debug the extension", "verify the UI", or after making changes to extension files (popup.html, popup.js, background.js, manifest.json, settings.html).
---

# Chrome Extension Test & Debug

Extension-specific testing workflows and debugging patterns. Uses the Playwright scripts from the **browser-test** skill for browser automation — see `~/.claude/skills/browser-test/SKILL.md` (Approach 2: Playwright Scripts) for full command reference and setup.

## Quick Reference

The browser-test scripts live in `<project>/.claude/scripts/`. If missing, copy from `~/.claude/skills/browser-test/scripts/`:

```bash
node <project>/.claude/scripts/browser-launch.js &   # Launch with extension
node <project>/.claude/scripts/browser-cmd.js <cmd>   # Run commands
```

Key commands for extension testing: `popup`, `screenshot`, `click`, `navigate`, `pages`, `eval`, `wait`.

**No `reload` command exists.** To reload after code changes, re-navigate:

```bash
node <project>/.claude/scripts/browser-cmd.js navigate "chrome-extension://<id>/popup.html"
```

Get `<id>` from `<project>/.browser-state.json`.

## Getting Extension ID (Manifest V3)

**CRITICAL**: For Manifest V3 extensions, get the extension ID from the service worker URL, NOT from chrome://extensions page scraping.

```javascript
// Playwright code
const browser = await chromium.launchPersistentContext('', {
  headless: false,
  args: [
    `--disable-extensions-except=${extensionPath}`,
    `--load-extension=${extensionPath}`,
    '--no-sandbox'
  ]
});

// Get extension ID from service worker (CORRECT WAY)
let serviceWorker = browser.serviceWorkers()[0];
if (!serviceWorker) {
  serviceWorker = await browser.waitForEvent('serviceworker');
}
const extensionId = serviceWorker.url().split('/')[2];
console.log(`Extension ID: ${extensionId}`);
```

**Why this works**: Service worker URL format is `chrome-extension://{extensionId}/_generated_background_page.html`, so splitting on `/` and taking index 2 gives the ID.

**Do NOT scrape chrome://extensions**: Shadow DOM structure is unreliable and changes between Chrome versions.

## Extension Testing Workflow

### 1. Launch and verify popup

```bash
node <project>/.claude/scripts/browser-launch.js &
sleep 5
node <project>/.claude/scripts/browser-cmd.js popup
node <project>/.claude/scripts/browser-cmd.js wait 1500
node <project>/.claude/scripts/browser-cmd.js screenshot popup.png
```

Use the Read tool on `.screenshots/popup.png` to visually verify.

### 2. Test button clicks open correct URLs

```bash
node <project>/.claude/scripts/browser-cmd.js click "#btn-id"
node <project>/.claude/scripts/browser-cmd.js wait 2000
node <project>/.claude/scripts/browser-cmd.js pages
```

Verify the expected URL appears in the tab list.

### 3. Test after code changes

```bash
node <project>/.claude/scripts/browser-cmd.js navigate "chrome-extension://<id>/popup.html"
node <project>/.claude/scripts/browser-cmd.js wait 1500
node <project>/.claude/scripts/browser-cmd.js screenshot after-change.png
```

## Debugging Patterns

### Popup shows wrong state

Inspect chrome.storage:

```bash
node <project>/.claude/scripts/browser-cmd.js eval "new Promise(r => chrome.storage.local.get(null, r))"
```

### Button not visible

Check if hidden by JS (e.g., `display:none`):

```bash
node <project>/.claude/scripts/browser-cmd.js eval "document.getElementById('btn-id')?.style.display"
```

Search for `style.display` in popup.js to find conditional visibility logic.

### Service worker errors

```bash
node <project>/.claude/scripts/browser-cmd.js navigate "chrome://extensions"
node <project>/.claude/scripts/browser-cmd.js screenshot extensions-page.png
```

### Manifest issues

Common problems:
- Missing permissions (check `manifest.json` `permissions` array)
- Wrong `web_accessible_resources` (pages won't load if not listed)
- Service worker not registered (check `background.service_worker` path)

## Multi-Worktree Testing

Tag each extension's manifest name to distinguish them in `chrome://extensions`:

```json
"name": "My Extension [branch-name]"
```

Revert the name before merging to main.

Each worktree has its own `extension/` folder. Load each as a separate unpacked extension.

## Automated Testing with Playwright

### Code Verification vs Visual Verification

**Use code verification for:**
- Checking if files were modified (grep, file existence)
- Counting elements (number of sites, buttons, etc.)
- Verifying data structures (constants, defaults)

**Use visual verification for:**
- UI layout and styling
- User-facing text and messages
- Button placement and visibility
- Overall user experience

**Example: Testing expanded site lists**
```bash
# Code verification (fast, precise)
blocked_count=$(grep -A200 "rewardSites:" extension/constants.js | grep -o "\.com" | wc -l)
echo "Found $blocked_count blocked sites (target: 50+)"

# Visual verification (proves it works for users)
node .claude/scripts/screenshot-test.js
# Then read and inspect .screenshots/settings.png
```

### Testing Implementation Details

**Check for inline vs external styles:**
```bash
# Some extensions use inline <style> tags instead of separate .css files
if ls extension/*.css 2>/dev/null; then
  echo "External CSS files found"
else
  echo "Checking for inline styles..."
  grep -c "<style>" extension/settings.html
fi
```

**Check for elements without IDs:**
```bash
# Implementation might add UI elements without the exact IDs from plan
# Use text content matching instead of ID selectors
grep -i "Blocked Applications" extension/settings.html  # ✓ Works
grep "id=\"blocked-apps-section\"" extension/settings.html  # ✗ Might fail
```

**Native host file formats:**
```bash
# Native hosts can be implemented in multiple languages
ls native-host/*.js    # Node.js
ls native-host/*.ps1   # PowerShell (Windows)
ls native-host/*.py    # Python
ls native-host/*.sh    # Bash (Linux/Mac)
```

### Screenshot-Based Testing Pattern

```javascript
// Create automated screenshot tests for all worktrees
const PHASES = [
  {
    name: 'Phase 8',
    path: path.resolve(__dirname, '../../../worktree-phase8/extension'),
    screenshots: [
      { page: 'settings.html', name: 'phase8-settings.png', scroll: 0 },
      { page: 'settings.html', name: 'phase8-sites.png', scroll: 2000 }
    ]
  }
];

for (const phase of PHASES) {
  const browser = await chromium.launchPersistentContext('', {
    headless: false,
    args: [`--disable-extensions-except=${phase.path}`, `--load-extension=${phase.path}`]
  });

  const serviceWorker = browser.serviceWorkers()[0] || await browser.waitForEvent('serviceworker');
  const extensionId = serviceWorker.url().split('/')[2];

  for (const shot of phase.screenshots) {
    const page = await browser.newPage();
    await page.goto(`chrome-extension://${extensionId}/${shot.page}`);
    await page.waitForTimeout(1500);
    if (shot.scroll) await page.evaluate((s) => window.scrollTo(0, s), shot.scroll);
    await page.screenshot({ path: `.screenshots/${shot.name}` });
    await page.close();
  }

  await browser.close();
}
```

Then use Read tool on `.screenshots/*.png` to visually verify implementations.

### Common Testing Pitfalls

1. **Timing issues**: Always add `waitForTimeout(1500)` after navigating to extension pages to allow scripts to load
2. **Chrome.storage reads**: Use `chrome.storage.local.get()` in evaluate() context, not directly in test code
3. **Service worker wakeup**: Extension service workers sleep; wake them by opening popup or sending a message first
4. **Element selectors**: Prefer data attributes or text content over brittle ID selectors that might change
5. **Persistent context required**: Extensions don't load in regular browser contexts; must use `launchPersistentContext()`

### Testing Checklist

When verifying Chrome extension implementations:

- [ ] Extension loads without errors (check console in background page)
- [ ] Extension ID obtained from service worker URL
- [ ] Screenshots captured of all modified UI pages
- [ ] Visual verification: UI looks correct in screenshots
- [ ] Code verification: grep confirms expected code changes
- [ ] Functional test: Click buttons, modify settings, verify behavior
- [ ] Storage test: Check chrome.storage.local persists settings correctly
- [ ] Multi-worktree test: Load all worktrees simultaneously with unique names
