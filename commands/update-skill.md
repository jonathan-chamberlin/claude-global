Improve skills used this session based on my corrections.

Re-read our entire conversation from the beginning. Identify every skill and command (slash command) that was used during this session. These may live anywhere — check both the user-level directory (`~/.claude/commands/`) and any project-level `.claude/commands/` directories.

Note: "skills" and "commands" are different things but both are `.md` files invoked via `/name`. Both should be reviewed and updated using the same process.

**Before doing anything else**, list out all the skills and commands you identified that were used this session. For each one, note whether it's a skill or command and where its `.md` file lives. Then ask me: "Are these all the skills/commands, or are there others I should investigate to see if they should be udpated?" Wait for confirmation before proceeding.

For each confirmed skill, review the messages I sent AFTER invoking it, or after claude automatically invoked it. These messages represent corrections, adjustments, or additional instructions I had to give to get the result I actually wanted. These are gaps in the skill's prompt.

For each skill, update its `.md` file to incorporate those corrections so they happen automatically next time. It's fine to bounce back and forth — read part of the conversation, update a skill, then go back to reading more of the conversation and update again. Don't try to batch everything at once.

1. Read the current skill file
2. Identify what I had to manually correct or ask for after the skill ran
3. Update the skill's instructions so those corrections are baked in
4. If multiple skills were used, update each one

Also capture any verification prompts I send — even questions like "are you sure this is good?" or "is that right?". If I felt the need to verify, that means the skill should include an explicit validation or verification step so I don't have to ask next time. Even if Claude's response was "yes, it's correct," the fact that I asked means the skill's output wasn't obviously correct and needs a built-in check.

Also look for user prompts that describe a desired behavior or output format (e.g. "give me a list of functions and arguments", "print it as bullet points"). If the user had to explicitly ask for a format or behavior that the skill should have produced automatically, that's a gap in the skill. Proactively propose baking these into the skill when they might be universally helpful.

Before making changes, ask me the following for changed that would not obviously be benefical for all future skill/command uses:
- Which corrections should be added to the skill vs. left as manual steps I handle myself
- Whether any of my feedback was one-off (shouldn't be in the skill) vs. a pattern I'd always want. 

Give me a summary of each proposed change before writing them. Use a single numbered list across all skills so the user can easily reference items by number (e.g., "do all except 3 and 5"). Group by skill using the skill name as a header line before its items:

**skill-name** (skill/command) — `path/to/file`
1. Description of gap and proposed fix
2. Description of gap and proposed fix

**other-skill** (skill/command) — `path/to/file`
3. Description of gap and proposed fix

If a skill generated code (scripts, utilities, helpers) during the session to accomplish a task, propose extracting that code into a `scripts/` folder inside the skill's directory. The skill's `.md` file should then reference the script by path instead of containing inline code. This keeps skills clean and makes the scripts reusable.

## Token Efficiency Audit

In addition to behavioral corrections, audit each skill for token waste. For every subagent launch observed during the session, check for these patterns:

1. **Redundant file reads**: Did a subagent read a file (tone guidelines, assignment description, source material, the draft itself) that the main agent already had in context? If so, the skill should be updated to paste that content inline into the subagent prompt instead.
2. **Oversized input**: Did a subagent receive an entire file when it only needed a few paragraphs or specific excerpts? If so, the skill should instruct the main agent to extract and paste only the relevant portion.
3. **Overpowered model**: Was a subagent using the default model for a mechanical task (rule-checking, formatting validation, simple lookup) that haiku could handle? If so, suggest adding `model: "haiku"` to that subagent launch.
4. **Unnecessary subagent**: Was a subagent launched for a task the main agent could have done inline, especially for short inputs (e.g., tone-checking 3 paragraphs)? If so, suggest adding a length threshold where the main agent handles it directly.
5. **Duplicated work across subagents**: Did multiple subagents each read the same file independently (e.g., tone guidelines read by 3 separate tone reviewers)? If so, the content should be pasted inline once per subagent rather than read via tools 3 times.

For each token waste pattern found, include it in the numbered proposal list with an estimated token savings (e.g., "~5k tokens saved per run by pasting guidelines inline instead of re-reading").

Also review the session for corrections to general behavior (not specific to any skill) — such as git workflow, code style, or communication preferences. If found, recommend a one-sentence addition to `~/.claude/CLAUDE.md`. Detailed or skill-specific fixes belong in their respective skill files, not CLAUDE.md.

**IMPORTANT: After presenting the summary, STOP and wait for explicit user approval before editing any files.** Do not write changes until the user confirms which proposed improvements to apply. The user may approve all, reject some, or modify the proposals.
