---
description: Summarize what I did today in one sentence based on git commits and conversation
---

Summarize what I accomplished today, then log it.

## Steps

1. Determine the time window:
   - Run this bash command to get the current hour: `date +%H`
   - If the current hour is 0, 1, 2, or 3 (between 12am-4am), the user is still up from the previous day. Use **yesterday at 6:00 AM** as the start time, and use **yesterday's date** for the log entry.
   - Otherwise, use **today at 6:00 AM** as the start time, and use **today's date** for the log entry.
   - The end time is always the current time.

2. Check existing log for last-checked time:
   - Read the log file at `C:\Repositories for Git\career-search\what-i-did-today.md`.
   - Look at today's date section. If it has a `(last checked HH:MM)` marker, use that time as the `--since` start time instead of 6:00 AM. This avoids re-fetching commits that were already summarized.
   - If there is no section for today yet, use 6:00 AM as the start time.

3. Get git commits across ALL repos on this computer:
   - Run the scan script, passing the correct since-time from step 2:
     ```
     bash ~/.claude/commands/scan-repos.sh YYYY-MM-DD HH:MM
     ```
   - Replace `YYYY-MM-DD` with the correct date and `HH:MM` with the since-time (either from the last-checked marker or 06:00).
   - This captures work across all projects, not just the current repo.

4. Review the conversation history:
   - Look at all the user's messages in this conversation to understand what tasks were worked on, what decisions were made, and what was accomplished.

5. Combine both sources (git commits + conversation context) and write a summary with **one bullet point per repo that had commits**. Each bullet should name the repo and describe what was done in it. Be concrete and specific — mention the actual things built, decisions made, or problems solved. Do not be vague. Skip repos with no meaningful commits (e.g., only gibberish commit messages and no conversation context about them).
   - **Lead each bullet with the significant impact or purpose of the work** — the "why" or "so what" — then follow with the specific tasks. The first clause should answer "what changed about the project at a high level?" not "what mechanical edits were made?"
     - Good: "Clarified that Phase 1 is about coding myself and Phase 2 is about building with agents. Restructured from 6 to 5 phases, added emojis, converted headings to h4."
     - Bad: "Restructured plan.md from 6 to 5 phases, added emojis to headings, converted day-of-week headings to h4, fixed duplicate HackerRank."
   - For repos with many changes, be descriptive: list out the key things that were built/changed rather than summarizing into one vague clause. Use commas or semicolons to separate distinct accomplishments within a bullet.
   - For repos with only 1-2 small changes, keep it brief.

6. Update the log file at `C:\Repositories for Git\career-search\what-i-did-today.md`:
   - First, check if a section for today's date (MM/DD/YY from step 1) already exists.
   - **If the date already exists:** Append the new bullet points directly under the existing bullets for that date. Do NOT add the date line again. Do not duplicate any bullets that already exist — only add new ones. Update the `(last checked HH:MM)` marker to the current time.
   - **If the date does not exist:** Insert a new section directly after the `# What I Did Today` heading (so the most recent day is always at the top). Add a blank line after the heading, then the new entry:
     ```
     MM/DD/YY (last checked HH:MM):
     - **repo-name**: What was done in this repo.
     - **other-repo**: What was done in this repo.
     ```
     Existing older entries below should remain unchanged.
   - The `(last checked HH:MM)` uses 24-hour time and reflects the current time when this command is run.

7. Output the summary to the user.

## Output Format

The date line followed by one bullet per repo. Nothing else. No headers, no extra explanation.

## Example Output

```
02/08/26 (last checked 21:15):
- **macros**: Made AHK scripts modular and maintainable — split into separate files with a main.ahk launcher; built triple-p "commit and push" macro and quadruple-l "git pull origin main" macro; added text expansion hotstrings (jc, eee, ;;date), smart Ctrl+C copy, and RShift+Arrow tab switching for Comet; renamed notion-hotkeys to website-hotkeys with Win+6 for GitHub repos.
- **career-search**: Clarified that Phase 1 is about coding myself and Phase 2 is about building with agents. Restructured plan.md from 6 to 5 phases, added emojis to all headings, converted day-of-week headings to h4, added HackerRank/SQL/open-source content from metalearning gap analysis.
```
