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
python ~/.claude/skills/ai-check/quillbot_check.py <text_file> [--paragraph N] [--per-paragraph] [--debug]
```

- `<text_file>` — path to a markdown or text file to check
- `--paragraph N` — only check paragraph N (0-indexed)
- `--per-paragraph` — force checking one paragraph at a time (less accurate, see below)
- `--debug` — opens headed browser, saves extra screenshots, prints debug info to stderr

### Default behavior (smart chunking)

The script automatically decides how to scan based on word count:

1. Count total words across all paragraphs (40+ words each, headers/metadata skipped)
2. **If total <= 1200 words** (QuillBot free tier limit): paste the entire text in one scan. This is the most accurate mode because QuillBot analyzes cross-paragraph patterns.
3. **If total > 1200 words**: group consecutive paragraphs into chunks, each <= 1200 words, always ending on a paragraph boundary (never splits mid-paragraph). Each chunk is scanned separately.

**Why chunked over per-paragraph**: QuillBot gives different results for isolated paragraphs vs. full text. A paragraph that passes alone can fail when surrounded by other text. Scanning the largest possible chunks catches these cross-paragraph detection patterns.

### Output
- JSON to stdout with results per chunk (or per paragraph in `--per-paragraph` mode)
- `mode` field: `"chunked"`, `"per-paragraph"`, or `"single"`
- `total_words` field: total word count of the text
- Screenshots saved to cwd as `ai-check-p{N}.png` (viewport-only, shows QuillBot results area)

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

Run the script on the text file (default smart chunking handles word count automatically):
```bash
python ~/.claude/skills/ai-check/quillbot_check.py <text_file>
```

Parse the JSON output. Check `is_clean` and `overall.ai_generated` for each chunk. The `flagged_sentences` array contains the specific sentences QuillBot highlighted.

### Step 3: Rewrite Flagged Sentences

For each chunk where `is_clean` is false:

1. Look at `flagged_sentences` — these are the specific sentences QuillBot highlighted
2. Rewrite each flagged sentence using voice_analysis.md patterns:
   - **Add burstiness**: Break long uniform sentences into short punch + longer explanation
   - **Use plain diction**: Replace academic/formal words with concrete equivalents (see diction table in voice_analysis.md)
   - **Apply signature moves**: "matters because", "could have... but", thinking-process reveals
   - **Break symmetry**: If sentences have parallel structure, make them asymmetric
   - **Use contractions**: "it's", "don't", "can't" instead of formal forms
   - **Vary sentence openers**: Start with "I", concrete subjects, or "But" pivots
3. Replace the flagged sentence in the file with the rewrite

### Step 4: Recheck (max 3 attempts)

After rewriting, run the script again on the updated file. The script will re-chunk and re-scan automatically.

1. If all chunks clean → done
2. If still flagged → rewrite the newly flagged sentences, run again
3. After 3 full passes with remaining flags → status = `failed`, flag for manual review

### Step 5: Save & Report

1. Save the final text to the original file
2. Report to user:
   - Total words / number of chunks used
   - Chunks clean on first pass
   - Sentences that needed rewriting (list what changed)
   - Chunks that failed after 3 attempts (if any)
   - Screenshots taken (user can view `ai-check-p{N}.png` files)

## Important Notes

- **Chunked by default**. Always scan the largest possible text per QuillBot call. Per-paragraph checking gives false negatives because it misses cross-paragraph patterns.
- **voice_analysis.md only**. Do NOT read or use tone_style_guidelines.md — it is archived.
- **Preserve meaning**. Rewrites must keep the same argument and evidence. Only change structure and word choice.
- **Don't over-rewrite**. If a sentence is clean, leave it alone. Only touch flagged sentences.
- **Max 3 attempts**. If text won't pass after 3 rewrite rounds, stop and tell the user.
- **Minimum 40 words**. QuillBot requires at least 40 words per check. Paragraphs shorter than that are skipped by the script.
