"""
QuillBot AI Content Detector automation script.
Usage: python quillbot_check.py <text_file> [--paragraph N] [--debug]

Pastes text into QuillBot's AI detector, waits for results,
extracts flagged sentences, and screenshots the results.

If --paragraph N is given, only checks that paragraph (0-indexed).
Otherwise checks all paragraphs sequentially.

Output: JSON to stdout with results per paragraph.
Screenshots saved to current directory as ai-check-p{N}.png
Debug mode (--debug) saves extra screenshots and prints to stderr.
"""

import sys
import json
import time
from playwright.sync_api import sync_playwright


DEBUG = False


def debug(msg):
    if DEBUG:
        print(f"[DEBUG] {msg}", file=sys.stderr)


def split_paragraphs(text):
    """Split text into paragraphs, skipping headers and metadata.

    Requires minimum 40 words per paragraph (QuillBot's minimum).
    """
    lines = text.strip().split('\n')
    paragraphs = []
    current = []

    for line in lines:
        stripped = line.strip()
        # Skip headers, metadata lines
        if stripped.startswith('#') or stripped.startswith('Response to'):
            continue
        if stripped == '':
            if current:
                paragraphs.append(' '.join(current))
                current = []
        else:
            current.append(stripped)

    if current:
        paragraphs.append(' '.join(current))

    # QuillBot requires minimum ~40 words
    return [p for p in paragraphs if len(p.split()) >= 40]


def paste_text_via_clipboard(page, text):
    """Paste text using clipboard simulation — works with React contenteditable."""
    # Set clipboard content and paste it
    page.evaluate("""(text) => {
        // Focus the editor
        const el = document.getElementById('aidr-input-editor')
            || document.querySelector('[data-testid="aidr-input-editor"]')
            || document.querySelector('[contenteditable="true"]');
        if (el) {
            // Clear existing content
            el.focus();
            document.execCommand('selectAll', false, null);
            document.execCommand('delete', false, null);
        }
    }""", text)
    time.sleep(0.3)

    # Use Playwright's clipboard paste
    page.evaluate("""(text) => {
        const el = document.getElementById('aidr-input-editor')
            || document.querySelector('[data-testid="aidr-input-editor"]')
            || document.querySelector('[contenteditable="true"]');
        if (el) {
            el.focus();
            // Create a paste event with the text
            const clipboardData = new DataTransfer();
            clipboardData.setData('text/plain', text);
            const pasteEvent = new ClipboardEvent('paste', {
                bubbles: true,
                cancelable: true,
                clipboardData: clipboardData
            });
            el.dispatchEvent(pasteEvent);
        }
    }""", text)
    time.sleep(0.5)

    # Verify text was set — if paste event didn't work, try insertText
    content = page.evaluate("""() => {
        const el = document.getElementById('aidr-input-editor')
            || document.querySelector('[data-testid="aidr-input-editor"]')
            || document.querySelector('[contenteditable="true"]');
        return el ? el.textContent.trim() : '';
    }""")

    if len(content) < 10:
        debug("Paste event didn't populate editor, trying insertText command")
        page.evaluate("""(text) => {
            const el = document.getElementById('aidr-input-editor')
                || document.querySelector('[data-testid="aidr-input-editor"]')
                || document.querySelector('[contenteditable="true"]');
            if (el) {
                el.focus();
                document.execCommand('selectAll', false, null);
                document.execCommand('insertText', false, text);
            }
        }""", text)
        time.sleep(0.5)

        # Check again
        content = page.evaluate("""() => {
            const el = document.getElementById('aidr-input-editor')
                || document.querySelector('[data-testid="aidr-input-editor"]')
                || document.querySelector('[contenteditable="true"]');
            return el ? el.textContent.trim() : '';
        }""")

    if len(content) < 10:
        debug("insertText also failed, falling back to keyboard typing")
        # Last resort: click the editor area with force and type
        editor = page.locator('#aidr-input-editor, [data-testid="aidr-input-editor"], [contenteditable="true"]').first
        try:
            editor.click(force=True)
            time.sleep(0.3)
            page.keyboard.type(text, delay=5)
            time.sleep(0.5)
        except Exception as e:
            debug(f"Keyboard typing failed: {e}")

    return content


def check_paragraph(page, text, paragraph_index, screenshot_dir='.'):
    """Paste text into QuillBot and extract results."""
    debug(f"Checking paragraph {paragraph_index}: {text[:80]}...")

    # Take pre-input screenshot in debug mode
    if DEBUG:
        page.screenshot(path=f'{screenshot_dir}/ai-check-p{paragraph_index}-before.png', full_page=False)

    # Paste text into the editor
    content = paste_text_via_clipboard(page, text)
    debug(f"Editor content after paste ({len(content)} chars): {content[:60]}...")

    # Take post-input screenshot
    if DEBUG:
        page.screenshot(path=f'{screenshot_dir}/ai-check-p{paragraph_index}-after-paste.png', full_page=False)

    time.sleep(1)

    # Find and click the scan button
    scan_btn = None
    for selector in [
        'button:has-text("Check for AI")',
        'button:has-text("Scan for AI")',
        'button:has-text("Scan")',
        'button:has-text("Check")',
        'button:has-text("Analyze")',
        'button:has-text("Detect")',
        '[data-testid*="scan"]',
        '[data-testid*="check"]',
        '[data-testid*="detect"]',
        '[data-testid*="submit"]',
    ]:
        try:
            btn = page.locator(selector).first
            if btn.is_visible(timeout=1000):
                scan_btn = btn
                debug(f"Found scan button with selector: {selector}")
                break
        except Exception:
            continue

    if scan_btn is None:
        # Try finding any prominent button that looks like a scan action
        debug("Trying fallback button search...")
        buttons = page.locator('button').all()
        for btn in buttons:
            btn_text = (btn.text_content() or '').strip()
            if btn_text:
                debug(f"  Found button: '{btn_text}'")
            if any(word in btn_text.lower() for word in ['scan', 'check', 'analyze', 'detect', 'submit']):
                scan_btn = btn
                debug(f"Found scan button via text search: '{btn_text}'")
                break

    if scan_btn:
        try:
            scan_btn.click()
            debug("Clicked scan button")
        except Exception as e:
            debug(f"Click failed, trying force click: {e}")
            scan_btn.click(force=True)
    else:
        debug("Could not find scan button!")
        # Dump all visible buttons for debugging
        buttons = page.locator('button').all()
        btn_texts = [(btn.text_content() or '').strip() for btn in buttons]
        debug(f"All buttons on page: {btn_texts}")
        return {"error": "Could not find scan button", "paragraph_index": paragraph_index,
                "buttons_found": btn_texts}

    # Wait for results — QuillBot takes a few seconds to analyze
    debug("Waiting for results...")
    time.sleep(8)

    # Scroll to top so results are visible in viewport screenshot
    page.evaluate("window.scrollTo(0, 0)")
    time.sleep(0.5)

    # Screenshot — viewport only (not full page) to see the results area
    screenshot_path = f'{screenshot_dir}/ai-check-p{paragraph_index}.png'
    page.screenshot(path=screenshot_path, full_page=False)
    debug(f"Screenshot saved to {screenshot_path}")

    # Extract flagged sentences using multiple strategies
    flagged = page.evaluate("""() => {
        const results = [];

        // Strategy 1: Look for highlighted spans/elements with background colors
        const allSpans = document.querySelectorAll('span, mark');
        for (const el of allSpans) {
            const style = getComputedStyle(el);
            const bg = style.backgroundColor;
            const text = el.textContent.trim();

            if (!text || text.length < 10) continue;
            if (bg === 'rgba(0, 0, 0, 0)' || bg === 'transparent' || bg === 'rgb(255, 255, 255)') continue;

            const match = bg.match(/rgb\\((\\d+),\\s*(\\d+),\\s*(\\d+)\\)/);
            if (match) {
                const [_, r, g, b] = match.map(Number);
                // Yellow/orange/red highlights
                if (r > 200 && b < 150) {
                    results.push({ text, bg, tag: el.tagName, cls: el.className });
                }
                // Pink/purple highlights
                if (r > 200 && b > 150 && g < 150) {
                    results.push({ text, bg, tag: el.tagName, cls: el.className });
                }
            }
        }

        // Strategy 2: Elements with AI-detection classes
        const aiElements = document.querySelectorAll(
            '[class*="highlight"], [class*="ai-"], [class*="flag"], ' +
            '[class*="detected"], [class*="human"], [class*="generated"]'
        );
        for (const el of aiElements) {
            const text = el.textContent.trim();
            if (text && text.length > 10) {
                results.push({
                    text,
                    bg: getComputedStyle(el).backgroundColor,
                    tag: el.tagName,
                    cls: el.className,
                    method: 'class-match'
                });
            }
        }

        // Strategy 3: Percentage/score elements
        const scoreElements = document.querySelectorAll(
            '[class*="score"], [class*="percent"], [class*="result"], ' +
            '[class*="meter"], [class*="gauge"], [class*="progress"]'
        );
        const scores = [];
        for (const el of scoreElements) {
            const text = el.textContent.trim();
            if (text) scores.push(text);
        }

        // Deduplicate by text
        const seen = new Set();
        const unique = results.filter(r => {
            if (seen.has(r.text)) return false;
            seen.add(r.text);
            return true;
        });

        return { flagged: unique, scores };
    }""")

    # Get overall AI percentage — QuillBot shows three categories
    overall = page.evaluate("""() => {
        const body = document.body.textContent;
        const result = {};

        // QuillBot shows: "AI-generated X%", "Human-written & AI-refined X%",
        // "Human-written X%" — extract each
        const aiGen = body.match(/AI-generated[\\s\\u00a0]*(\\d+)%/i);
        const aiRef = body.match(/Human-written\\s*&\\s*AI-refined[\\s\\u00a0]*(\\d+)%/i);
        const human = body.match(/Human-written[\\s\\u00a0]*(\\d+)%/i);

        if (aiGen) result.ai_generated = parseInt(aiGen[1]);
        if (aiRef) result.ai_refined = parseInt(aiRef[1]);
        if (human) result.human_written = parseInt(human[1]);

        // Also check for "X% of text is likely AI"
        const likelyAI = body.match(/(\\d+)%\\s*of text is likely AI/i);
        if (likelyAI) result.likely_ai_pct = parseInt(likelyAI[1]);

        // Check for the big percentage in the donut chart area
        const bigPct = body.match(/(\\d+)%\\s*of text/i);
        if (bigPct) result.headline_pct = parseInt(bigPct[1]);

        return Object.keys(result).length > 0 ? result : null;
    }""")

    return {
        "paragraph_index": paragraph_index,
        "text_checked": text[:100] + '...' if len(text) > 100 else text,
        "flagged_sentences": flagged.get('flagged', []),
        "scores": flagged.get('scores', []),
        "overall": overall,
        "screenshot": screenshot_path,
        "is_clean": len(flagged.get('flagged', [])) == 0
    }


def prepare_browser(p_instance):
    """Launch browser, navigate to QuillBot, dismiss modals, verify editor."""
    browser = p_instance.chromium.launch(headless=not DEBUG)
    context = browser.new_context(
        viewport={'width': 1280, 'height': 900},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                   'AppleWebKit/537.36 (KHTML, like Gecko) '
                   'Chrome/122.0.0.0 Safari/537.36'
    )
    page = context.new_page()

    debug("Navigating to QuillBot AI detector...")
    page.goto(
        'https://quillbot.com/ai-content-detector',
        wait_until='domcontentloaded', timeout=60000
    )
    time.sleep(5)

    if DEBUG:
        page.screenshot(path='ai-check-landing.png', full_page=False)
        debug("Landing page screenshot saved")

    # Dismiss cookie/modal if present
    try:
        for sel in [
            'button:has-text("Accept")',
            'button:has-text("Accept All")',
            'button:has-text("Got it")',
            'button:has-text("Close")',
            '[aria-label="Close"]',
            'button:has-text("I agree")',
        ]:
            btn = page.locator(sel).first
            if btn.is_visible(timeout=1000):
                btn.click()
                debug(f"Dismissed modal with: {sel}")
                time.sleep(0.5)
                break
    except Exception:
        pass

    # Verify editor exists
    editor_info = page.evaluate("""() => {
        const el = document.getElementById('aidr-input-editor')
            || document.querySelector('[data-testid="aidr-input-editor"]')
            || document.querySelector('[contenteditable="true"]');
        if (!el) {
            const editables = document.querySelectorAll('[contenteditable]');
            const textareas = document.querySelectorAll('textarea');
            return {
                found: false,
                editables: Array.from(editables).map(
                    e => ({tag: e.tagName, id: e.id,
                           class: e.className,
                           testid: e.getAttribute('data-testid')})
                ),
                textareas: Array.from(textareas).map(
                    e => ({id: e.id, class: e.className,
                           placeholder: e.placeholder})
                )
            };
        }
        return {
            found: true, tag: el.tagName, id: el.id,
            class: el.className,
            testid: el.getAttribute('data-testid'),
            visible: el.offsetParent !== null,
            rect: el.getBoundingClientRect()
        };
    }""")
    debug(f"Editor info: {json.dumps(editor_info)}")

    return browser, page


# QuillBot free tier limit (words)
QUILLBOT_WORD_LIMIT = 1200


def build_chunks(paragraphs):
    """Group paragraphs into chunks that fit QuillBot's word limit.

    Keeps paragraphs together — never splits mid-paragraph.
    Returns list of (chunk_text, paragraph_indices) tuples.
    """
    chunks = []
    current_text_parts = []
    current_indices = []
    current_words = 0

    for i, para in enumerate(paragraphs):
        para_words = len(para.split())
        if current_words + para_words > QUILLBOT_WORD_LIMIT and current_text_parts:
            chunks.append(('\n\n'.join(current_text_parts), current_indices[:]))
            current_text_parts = []
            current_indices = []
            current_words = 0
        current_text_parts.append(para)
        current_indices.append(i)
        current_words += para_words

    if current_text_parts:
        chunks.append(('\n\n'.join(current_text_parts), current_indices[:]))

    return chunks


def main():
    global DEBUG

    if len(sys.argv) < 2:
        print("Usage: python quillbot_check.py <text_file> "
              "[--paragraph N] [--full-text] [--debug]")
        sys.exit(1)

    text_file = sys.argv[1]
    paragraph_filter = None
    full_text_mode = '--full-text' in sys.argv

    if '--debug' in sys.argv:
        DEBUG = True

    if '--paragraph' in sys.argv:
        idx = sys.argv.index('--paragraph')
        paragraph_filter = int(sys.argv[idx + 1])

    with open(text_file, 'r', encoding='utf-8') as f:
        text = f.read()

    paragraphs = split_paragraphs(text)
    debug(f"Found {len(paragraphs)} paragraphs (40+ words each)")
    for i, p_text in enumerate(paragraphs):
        debug(f"  P{i}: {len(p_text.split())} words — {p_text[:60]}...")

    if not paragraphs:
        print(json.dumps({"error": "No paragraphs found with 40+ words"}))
        sys.exit(1)

    total_words = sum(len(p_text.split()) for p_text in paragraphs)
    debug(f"Total words: {total_words}")

    with sync_playwright() as pw:
        browser, page = prepare_browser(pw)
        results = []

        if full_text_mode:
            # Paste as much text as fits QuillBot's limit per chunk
            chunks = build_chunks(paragraphs)
            debug(f"Full-text mode: {len(chunks)} chunk(s)")
            for ci, (chunk_text, indices) in enumerate(chunks):
                debug(f"Chunk {ci}: paragraphs {indices}, "
                      f"{len(chunk_text.split())} words")
                result = check_paragraph(
                    page, chunk_text, ci,
                    screenshot_dir='.'
                )
                result['mode'] = 'full-text'
                result['paragraph_indices'] = indices
                results.append(result)
                time.sleep(1)
        elif paragraph_filter is not None:
            if paragraph_filter < len(paragraphs):
                result = check_paragraph(
                    page, paragraphs[paragraph_filter], paragraph_filter
                )
                results.append(result)
            else:
                debug(f"Paragraph {paragraph_filter} out of range "
                      f"(only {len(paragraphs)} paragraphs)")
        else:
            for i, para in enumerate(paragraphs):
                result = check_paragraph(page, para, i)
                results.append(result)
                time.sleep(1)

        browser.close()

    print(json.dumps({
        "paragraphs": results,
        "total": len(paragraphs),
        "mode": "full-text" if full_text_mode else "per-paragraph"
    }, indent=2))


if __name__ == '__main__':
    main()
