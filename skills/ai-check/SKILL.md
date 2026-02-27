---
name: ai-check
description: Check text for AI detection using QuillBot's AI content detector. Extracts flagged sentences, rewrites them using voice_analysis.md, and rechecks until clean. Use when user wants to check if their writing passes AI detection, or after draft-and-revise completes.
---

# ai-check

Check text against QuillBot's AI content detector. Extract flagged sentences, rewrite them, recheck until clean.

## When to Use

- User asks to check text for AI detection
- User mentions QuillBot, AI detector, or AI detection
- After draft-and-revise completes, as a final validation step
- User says "ai check", "check for ai", "run ai detection"

## Script

The Playwright automation script lives at:
```
~/.claude/skills/ai-check/quillbot_check.py
```

### Usage
```bash
python ~/.claude/skills/ai-check/quillbot_check.py <text_file> [--paragraph N] [--debug]
```

- `<text_file>` — path to a markdown or text file to check
- `--paragraph N` — only check paragraph N (0-indexed). Omit to check all paragraphs.
- `--debug` — opens headed browser, saves extra screenshots, prints debug info to stderr

### Output
- JSON to stdout with results per paragraph
- Screenshots saved to cwd as `ai-check-p{N}.png` (viewport-only, shows QuillBot results area)

### What the script does
1. Splits text into paragraphs (40+ words each, skips headers/metadata)
2. Opens QuillBot AI detector in Chromium via Playwright
3. For each paragraph: pastes text via clipboard simulation into the React contenteditable editor, clicks the "Detect" button, waits 8 seconds for analysis
4. Extracts flagged sentences (orange-highlighted spans with `rgb(254, 177, 83)`) and overall AI/Human percentages
5. Returns JSON with `is_clean`, `flagged_sentences`, and `overall` percentages per paragraph

### Key DOM details (discovered during testing)
- Editor: `div#aidr-input-editor` (`data-testid="aidr-input-editor"`, MUI contenteditable div)
- Upload button overlay intercepts clicks — script uses JavaScript `ClipboardEvent` paste to bypass
- Scan button: matches `button:has-text("Detect")`
- Flagged text: `<span>` elements with `background-color: rgb(254, 177, 83)` (orange)
- Results show three categories: AI-generated %, Human-written & AI-refined %, Human-written %

## Workflow

### Step 1: Setup

1. Read `C:\Users\Jonathan Chamberlin\.claude\skills\draft-and-revise\references\voice_analysis.md` — this is the style reference for rewrites.
2. Get the text to check:
   - If the user provided a file path or the IDE selection contains text, use that
   - If args contain a file path, read that file
   - Otherwise, ask the user what text to check
3. Track each paragraph's status: `unchecked`, `clean`, `dirty`, `rewriting`, `failed`

### Step 2: Run the script

Run the script on the text file:
```bash
python ~/.claude/skills/ai-check/quillbot_check.py <text_file>
```

Parse the JSON output. For each paragraph, check `is_clean` and `overall.ai_generated`.

### Step 3: Rewrite Flagged Sentences

For each paragraph where `is_clean` is false:

1. Look at `flagged_sentences` — these are the specific sentences QuillBot highlighted
2. Rewrite each flagged sentence using voice_analysis.md patterns:
   - **Add burstiness**: Break long uniform sentences into short punch + longer explanation
   - **Use plain diction**: Replace academic/formal words with concrete equivalents (see diction table in voice_analysis.md)
   - **Apply signature moves**: "matters because", "could have... but", thinking-process reveals
   - **Break symmetry**: If sentences have parallel structure, make them asymmetric
   - **Use contractions**: "it's", "don't", "can't" instead of formal forms
   - **Vary sentence openers**: Start with "I", concrete subjects, or "But" pivots
3. Replace the flagged sentence in the paragraph text with the rewrite

### Step 4: Recheck Dirty Paragraphs

For each rewritten paragraph (max 3 attempts per paragraph):

1. Save the updated text to a temp file
2. Run the script again with `--paragraph N` to check only that paragraph
3. If clean → done
4. If still flagged → rewrite the newly flagged sentences, try again
5. After 3 failed attempts → status = `failed`, flag for manual review

**Skip paragraphs already marked clean** — don't recheck them.

### Step 5: Save & Report

1. Reassemble all paragraphs (clean + rewritten) back into the full text
2. Save to the original file
3. Report to user:
   - Total paragraphs checked
   - Paragraphs clean on first pass
   - Paragraphs that needed rewriting (list which ones and what changed)
   - Paragraphs that failed after 3 attempts (if any)
   - Screenshots taken (user can view `ai-check-p{N}.png` files)

## Important Notes

- **One paragraph at a time**. Don't paste the full text — check paragraph by paragraph to isolate issues.
- **voice_analysis.md only**. Do NOT read or use tone_style_guidelines.md — it is archived.
- **Preserve meaning**. Rewrites must keep the same argument and evidence. Only change structure and word choice.
- **Don't over-rewrite**. If a sentence is clean, leave it alone. Only touch flagged sentences.
- **Max 3 attempts**. If a paragraph won't pass after 3 rewrites, stop and tell the user.
- **Minimum 40 words**. QuillBot requires at least 40 words per check. Paragraphs shorter than that are skipped.
