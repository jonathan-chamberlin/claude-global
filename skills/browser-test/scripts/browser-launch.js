// Launch Chromium with the FocusContract extension loaded
// Stays running in background with CDP on port 9222
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const EXTENSION_PATH = path.resolve(__dirname, '../../extension');
const USER_DATA_DIR = path.resolve(__dirname, '../../.browser-profile');
const STATE_FILE = path.resolve(__dirname, '../../.browser-state.json');
const PORT = 9222;

(async () => {
  // Clean up stale state
  if (fs.existsSync(STATE_FILE)) fs.unlinkSync(STATE_FILE);

  console.log(`Launching Chromium with extension: ${EXTENSION_PATH}`);
  console.log(`CDP port: ${PORT}`);

  const context = await chromium.launchPersistentContext(USER_DATA_DIR, {
    headless: false,
    args: [
      `--disable-extensions-except=${EXTENSION_PATH}`,
      `--load-extension=${EXTENSION_PATH}`,
      `--remote-debugging-port=${PORT}`,
      '--no-first-run',
      '--no-default-browser-check',
    ],
  });

  // Get the extension ID from the service worker
  let extensionId = null;
  let retries = 0;
  while (!extensionId && retries < 10) {
    for (const sw of context.serviceWorkers()) {
      const url = sw.url();
      const match = url.match(/chrome-extension:\/\/([a-z]+)/);
      if (match) {
        extensionId = match[1];
        break;
      }
    }
    if (!extensionId) {
      await new Promise(r => setTimeout(r, 500));
      retries++;
    }
  }

  // Save state for other scripts
  const state = {
    port: PORT,
    extensionId: extensionId || 'unknown',
    pid: process.pid,
    launchedAt: new Date().toISOString(),
  };
  fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));

  console.log(`Extension ID: ${extensionId || 'not detected'}`);
  console.log(`State saved to: ${STATE_FILE}`);
  console.log('Browser running. Press Ctrl+C to stop.');

  // Keep process alive
  process.on('SIGINT', async () => {
    console.log('Closing browser...');
    if (fs.existsSync(STATE_FILE)) fs.unlinkSync(STATE_FILE);
    await context.close();
    process.exit(0);
  });
})();
