---
description: Explain the current problem and what you've tried so I can hand it off to another LLM
---

Stop working on the problem. Instead, write a handoff briefing that I can paste into another LLM to get help.

## What to include

1. **Problem statement** — What is the goal, and what specific thing isn't working or needs to be done? Be concrete (file paths, function names, error messages).

2. **What's been tried** — List every approach attempted this session and why each one failed or was insufficient. Include the actual results, not just "it didn't work."

3. **Current state** — What does the code look like right now? Include the relevant code snippets inline (don't just reference file paths — the other LLM can't see my files).

4. **Constraints** — Anything the other LLM needs to know: language/framework, OS (Windows), project structure conventions, things that must not change.

5. **What I need** — State the specific question or ask. "Fix this" is too vague. "Why does X return Y when I expect Z" is good.

## Format

Output the briefing as a single copyable block inside a markdown code fence, so I can select-all and paste it. Do not put anything outside the fence — no preamble, no follow-up commentary.

## Rules

- Include actual code, actual error messages, actual output. No summaries or paraphrases.
- If you have a hypothesis about the root cause, include it — but label it as your hypothesis, not fact.
- Keep it as short as possible while being complete. The other LLM doesn't need the full file if only 10 lines matter.
