---
name: draft-and-revise
description: Automates iterative drafting, self-evaluation, and revision for assignments with evaluation criteria. Supports both written and visual assignments (diagrams, charts). Use when the user asks to "do the assignment," "complete the assignment," or wants polished output without manual back-and-forth.
---

# draft_and_revise

## When to Use

- User asks to "do the assignment" or "complete the assignment"
- User wants polished output without manual back-and-forth
- Clear assignment criteria exist to evaluate against
- Assignment requires visual output (diagrams, charts, flowcharts)

## Token Efficiency

The main agent reads tone guidelines, assignment instructions, and source material in Phase 1-2. Subagents should NEVER re-read these files. Paste all needed content directly into subagent prompts. Exception: Phase 6 fact-checking for sources not yet read.

## Workflow

### Phase 1: Setup

**Short assignments** (under 500 words, fewer than 3 source files): The main agent should read files directly with parallel Read/Glob calls instead of launching Explore subagents. Save subagents for larger assignments.

1. Read `references/voice_analysis.md` in this skill's directory. This is the ONLY style reference. Do NOT read `tone_style_guidelines.md` — it is archived and no longer used.
2. Read assignment file: extract description, evaluation criteria, word count, specific requirements.
3. Read any source material (texts, PDFs, articles).
4. **Verify sources available in full** before drafting. Don't proceed until every secondary source is read as a complete article. If missing, search for accessible versions and ask user.
5. **Extract page numbers** (only for Works Cited assignments): Find PDF-to-journal-page mapping for real page numbers. Don't leave `[pg#]` placeholders.
6. **Determine output type**: Text-only (markdown/PDF), Visual (generated images in PDF), or Mixed. If ER diagrams needed, switch to `er-diagrams` skill.
7. **Visual setup** (skip if text-only): Create `files/` subfolder, check available Python libraries, plan generation approach. Images referenced on own lines using backtick syntax.

### Phase 2: Initial Draft

Write complete first draft following style guidelines, assignment requirements, and proper word count.

**Multi-problem assignments**: Launch one subagent per problem in parallel. Each receives (pasted inline) its problem description, shared instructions, and file paths. Integrate outputs after.

### Phase 3: Self-Evaluation Loop (max 10 cycles)

**Part A — Rubric Grid**: List each assignment criterion + always include "Tone & Style Adherence." Rate each: Fail / Low / At Standard / Good / Excellent. A draft cannot get an A if it violates tone guidelines. If grade = A, skip to Phase 4.

For engw3309 assignments without explicit criteria, evaluate: Passage/Evidence Selection, Observation, Judgment, Thick Logic, Question (if required), Word Count.

**Part B — Written Commentary** (3-5 sentences):
- Debatability test: Is this surprising? Could a reader disagree?
- "How?" and "Why?" check: Does the draft explain mechanism and significance, not just observation?
- Strongest-moment push: Could the best passage go deeper?

**Revise**: Generate specific suggestions referencing specific sentences. Apply them. Re-evaluate. Continue until A or 10 cycles.

### Phase 4: Polish Pass (mandatory even after content reaches A)

Sentence-by-sentence scan applying `voice_analysis.md` patterns. For each issue: quote the problematic sentence, show the fix, make the edit.

Key scans:
- **AI patterns**: negation pairs, symmetrical structures, clean triplets, exhaustive lists, capstone sentences, stacked "could" conditionals
- **Abstraction**: replace vague phrases ("the system," "recognizing") with concrete meaning
- **Jargon**: swap academic words for plain equivalents
- **Completeness**: fill in missing subjects, connecting words, concrete modifiers

**Word Count Guard**: If polish pass trimmed below minimum, add substantive content to weakest paragraph.

### Phase 5: Parallel Review

Skip if Phase 4 already handled tone inline (drafts 6 paragraphs or fewer). For longer drafts: split into chunks, launch parallel subagents using template at `templates/tone_review.md`. Paste guidelines and text inline. Apply fixes that improve tone without breaking coherence.

### Phase 6: Factual Verification

1. Enumerate every factual claim (quotes, paraphrases, statistics, descriptions).
2. Verify from context first (sources already read). Mark CONFIRMED or flag.
3. Group unverified claims by source. Launch subagents in parallel for remaining claims.
4. Compile verification table. Fix inaccuracies or flag to user.

### Phase 7: Skeptical Professor Review

Launch fresh subagent(s) to grade independently. Use template at `templates/skeptical_professor_text.md` (text) or `templates/skeptical_professor_visual.md` (visual). Paste draft, assignment description, and voice_analysis.md inline. Do NOT give revision history.

**For drafts under 500 words**, use `model: "haiku"` for the skeptical professor subagent — grading short drafts against a rubric is mechanical enough for a smaller model.

If below A: apply top suggestions. Always include full analysis in report.

### Phase 8: Output

1. Verify no placeholders remain (`[pg#]`, `[citation needed]`, `TODO`).
2. Save final draft to assignment file.
3. Generate PDF: text-only uses Playwright HTML-to-PDF; visual/mixed uses `scripts/generate_pdf.py <markdown_file> <output_pdf>`.
4. Report to user: both grades, revision cycles, polish fixes, professor suggestions, fact-check summary, phase-by-phase changelog, PDF path.
5. Extract submission instructions from assignment description. Present as numbered steps (where to upload, file naming, due date).

## Important Notes

- Run all cycles autonomously. Do NOT ask user for input during the loop.
- Only save the final version. Each revision is targeted, not a full rewrite.
