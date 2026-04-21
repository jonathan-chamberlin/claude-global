Improve skills used this session based on my corrections. Run fully autonomously — no user confirmation at any step.

Re-read our entire conversation from the beginning. Identify every **skill**, **command**, **hook**, **MCP server/tool**, **subagent**, **rule**, and **memory entry** that was used, fired, or should have been used during this session.

## Where things live

| Kind | Path | Signal that it "was used" |
|------|------|---------------------------|
| Skill | `~/.claude/skills/<name>/SKILL.md`, project `.claude/skills/` | Explicit `/name` invocation or auto-trigger from description |
| Command | `~/.claude/commands/*.md`, project `.claude/commands/` | Same as skills — `.md` files invoked via `/name`, reviewed the same way |
| Hook | `~/.claude/settings.json` / `.claude/settings.json` / `.claude/settings.local.json`; scripts in `~/.claude/hooks/` or `.claude/hooks/` | `<user-prompt-submit-hook>` / `SessionStart:` system-reminders, blocked/modified/warned tool calls, post-tool injections, any system-reminder that looks like local-script output |
| MCP | `~/.claude.json` / `.mcp.json`; companion reference skills (`canvas`, `superwall`, `notion-tasks`, etc.) | `mcp__<server>__<tool>` tool calls; session-start `instructions` blocks |
| Subagent | `~/.claude/agents/*.md` with frontmatter | `Agent` tool calls with `subagent_type` |
| Rule | `~/.claude/rules/*.md` loaded globally via `~/.claude/CLAUDE.md` | Behavioral defaults applied without per-skill opt-in |
| Memory | `~/.claude/projects/-Users-jonathanchamberlin/memory/*.md`, indexed by `MEMORY.md` | Recall of prior-session facts |

## Step 1: list what you found

Print every item that was used or is relevant to corrections made this session, grouped by kind, each with its file/path. Then proceed.

For each item, review what I sent AFTER it ran — corrections, re-launches, "not quite what I wanted," verification prompts, format requests. These are gaps to bake in:

- **Corrections** — the thing should have happened automatically.
- **Verification prompts** ("are you sure", "is that right") — if I had to verify, bake in an explicit check so I don't ask next time.
- **Format/behavior requests** ("give me a list", "bullet points") — if I had to ask for it, the skill should have produced it automatically. Add when universally helpful.

Read a bit of conversation, update one thing, go back — don't batch everything at once. For ambiguous corrections (one-off vs pattern), err toward including.

## Step 2: print a summary of changes

Single numbered list across everything, grouped by item name as a header line. Each entry names the file path, runs the **Placement Debate** (see Routing Decision section) inline, then describes the fix. Run the audits below to populate the list — each audit's findings become items under their source item.

**skill-name** (skill/command/hook/agent/…) — `path/to/file`
1. Gap: <one line>
   Candidates:
     - <container A> — PRO: <one line>; CON: <one line>
     - <container B> — PRO: <one line>; CON: <one line>
   Decision: <chosen home + file path>. Accepting: <tradeoff>.
   Fix: <what changed>
2. Gap: …

**other-item** — `path/to/file`
3. …

Skip the debate block ONLY for fixes that patch an already-decided home (bug in an existing script, typo in an existing template, stale field in an existing memory). For those, one line is fine.

For extractions, include before/after line counts (e.g. "Extracted Canvas cross-reference from daily-tasks/SKILL.md to CANVAS.md — 218 → 94 lines"). For token-waste fixes, include estimated savings per run.

## Step 3: apply every edit immediately

Before writing any SKILL.md edit, ensure it conforms to `~/.claude/skills/create_update_skill/SKILL.md` (required frontmatter, folder structure, extraction rule). If frontmatter is missing, add it as part of the update.

---

# Audits

Run each audit against every item of its kind touched this session.

## Boilerplate Extraction Audit (applies to every reviewed SKILL.md)

Every line in `SKILL.md` is read on every invocation — anything not on the default path is pure tax. Sweep each reviewed `SKILL.md` in full (not just session-added content) and flag sections matching:

1. **Conditionally-read blocks** — gated on a trigger/mode/flag ("help mode", "verbose", "canvas", "when user asks for X"). ≥15 lines and not default path → extract.
2. **Verbatim boilerplate** — prompt footers, dispatch blocks, completion messages, commit scaffolds. Extract to `templates/<name>.md` and reference.
3. **Rarely-used reference data** — schema tables, API catalogs, tool dictionaries, enum lists, example galleries. Extract to `REFERENCE.md` or named file (`CANVAS.md`, `HELP_MODE.md`).
4. **Mechanical payload construction** — fixed-structure API payloads or property dicts (per `~/.claude/rules/mechanical-mutations.md`). Belongs in `scripts/<action>.py` that the skill calls.

For each extraction, write content to the sibling file, then replace in `SKILL.md` with:

```
## <Section> (only when <trigger>)

Follow `~/.claude/skills/<skill>/<FILE>.md`. Do NOT read it or run its steps unless <trigger>.
```

Skip extraction if <15 lines AND runs on every invocation — pointer indirection isn't worth it.

If the skill generated inline code during the session (scripts, utilities, helpers), extract to `scripts/` inside the skill's directory and reference by path.

## Internal Redundancy Audit (applies to every reviewed SKILL.md)

Boilerplate Extraction moves bloat OUT of `SKILL.md`. This audit deletes duplication WITHIN it. Same goal: every line read on every invocation should carry unique signal. Repeated instructions dilute each one and give the model permission to skim.

Scan the full `SKILL.md` (not just session edits) and flag:

1. **Repeated footer/header instructions** — the same closing line appearing under every subsection ("include this in the summary", "then proceed", "report back when done"). If the instruction is universal to the skill, state it once at the top or bottom. Delete every other copy.
2. **Same rule stated in multiple sections** — guidance that appears in two or more sections with slightly different wording (e.g. model-selection logic in both an Agent section and a Model Selection section). Pick the canonical home, replace others with a one-line cross-reference ("see <section>").
3. **Overlapping audits / checklists with differently-worded duplicates** — two checklists whose items cover the same ground from different angles. Merge into one. If a single issue appears in both lists, the model will either double-count it or treat the variants as distinct checks and miss the unified fix.
4. **Redundant autonomy / meta-instructions** — "do not wait for approval", "run autonomously", "proceed immediately" repeated across sections. State once at the top; delete every other copy.
5. **Restated concepts in explanatory prose** — the same extraction rule / routing rule / severity ordering explained in three places "for emphasis." Pick the fullest statement; others become pointers.
6. **Per-section "where to look" that re-specifies a shared enumeration** — if Step 1 already enumerated the targets, each audit doesn't need its own scavenger hunt. Collapse to one line: "per Step 1 enumeration."

For each redundancy, in Step 2 report: the redundant passages (section names + rough line ranges), which copy becomes canonical, what was replaced with a pointer vs. deleted outright, and net line savings.

**Heuristic threshold:** if the same instruction (or near-identical paraphrase) appears ≥3 times, it's redundant regardless of length. If it appears exactly twice, redundant only when both copies are ≥2 lines or when the two contexts are close enough that one pointer would suffice.

**What is NOT redundant:** parallel structure across genuinely distinct audits (e.g. every audit section having a numbered list of flag-items is a pattern, not a duplication — each item is unique). Don't flatten structure that aids scanning.

## Hook Audit

1. **Fired but failed / warned non-actionably** — warning I ignored or non-zero exit I worked around. Tighten message or trigger.
2. **Missing a case** — I manually corrected something the hook should have caught. Widen the pattern.
3. **Too noisy** — fired on irrelevant tool calls. Narrow the matcher.
4. **Message ordering** — PreToolUse must lead DATA CORRUPTION → CORRECTNESS → STYLE (per `CLAUDE.md` gotchas). Reorder if buried.
5. **Missing hook** — repeated "from now on when X" request belongs in a hook. Flag for creation via `update-config`.

## MCP Audit

1. **Tool used incorrectly** — wrong params, missing required field, guessed enum. Companion skill should document the correct shape. Fixed-structure payloads → `scripts/` (mechanical-mutations rule), not prose.
2. **Tool returned unexpected shape** — document actual response in companion skill's reference.
3. **Missing companion skill** — MCP used multiple times with no reference skill for tools/IDs/enums. Flag creation (NEW SKILL NEEDED). Especially with mechanical values.
4. **Stale reference data** — cached IDs/enums wrong. Re-query MCP and refresh.
5. **Redundant MCP calls** — same lookup repeated in a session. Cache inline or instruct reuse.
6. **Auth / preflight issues** — if MCP is flagged MISSING often, belongs in a hook or reference skill, not live debugging.
7. **Server-level instructions out of sync** — session-start `instructions` conflicted with actual use. Document the override in the companion skill (server's own instructions aren't editable).

## Agent Audit

Review messages I sent after each subagent returned — corrections, re-launches, "not quite what I wanted," follow-up work it should have done.

1. **Returned the wrong thing** — I had to re-launch, correct output, or do it myself. Bake correction into the agent's `.md`.
2. **Wrong tool set** — lacked a needed tool, or had tools it shouldn't use. Update `tools:` frontmatter.
3. **Wrong model** — see Model Selection Audit.
4. **Missing context in prompt** — terse or missing background. Update the skill that launched it to paste more context inline.
5. **Over/under-scoped** — `description:` too narrow (widen) or wrong agent picked (update caller's routing).
6. **Redundant file reads in subagent** — subagent read a file the main agent already had in context (tone guidelines, source material, draft). Paste inline instead. Report token savings in Step 2 item.
7. **Oversized input** — subagent got the entire file when it needed an excerpt. Extract and paste only the relevant portion.
8. **Duplicated work across subagents** — multiple subagents read the same file independently. Paste inline once per subagent.
9. **Unnecessary subagent** — short task main agent could have done inline (e.g. tone-checking 3 paragraphs). Add a length threshold where main handles directly.
10. **Missing subagent** — class of work happened 2+ times this session and would benefit from a dedicated agent (context isolation, specialized tools, specific model). Flag creation.

## Rules Audit

1. **Genuinely universal correction** — applies to every project/session (not a specific tool, MCP, or domain). Belongs in a rule. Most corrections don't qualify — walk the Routing Decision first.
2. **Existing rule needs refinement** — session correction contradicted or extended a rule. Update. Lead with rule, then why, then how to apply.
3. **Rule conflicts with a skill** — resolve. Skill usually wins for its domain; rule covers only the universal default.
4. **Over-reach candidates** — "rule" that only applies in one project/tool → demote to skill or project CLAUDE.md.

## Memory Audit

Memory persists across conversations. Types: user, feedback, project, reference.

1. **Stale memory** — names a function/file/ID that no longer exists. Fix or delete. Per `CLAUDE.md`, trust current state over stale memory.
2. **Missing memory** — durable non-obvious fact about user/project/feedback/external reference. Save. Skip anything derivable from code, git history, or CLAUDE.md.
3. **Duplicate memory** — consolidate overlapping files.
4. **Misfiled memory** — "feedback" that's really project detail (or vice versa). Rename and re-categorize.
5. **Index drift** — `MEMORY.md` pointers to deleted files, or memory files without index entries. Reconcile both.

## Discoverability Audit

Signal: I did something manually when a skill exists that should have auto-triggered, OR I had to explicitly type `/skill-name` when the description should have matched my phrasing.

1. **Description too narrow** — widen to include my phrasing (e.g. "push the build" vs "ship to TestFlight").
2. **Missing trigger examples** — add 2-3 concrete example phrases when absent.
3. **Two skills competing** — disambiguate descriptions. "Use this NOT that" lines.
4. **Dead skills** — unused in recent sessions, overlapping with a newer skill, or domain absorbed elsewhere. Flag for deletion/consolidation. Err toward keeping.
5. **Redundant skills** — near-duplicates. Merge, delete the loser, update references.

## Scripts & Templates Audit

Scripts and templates are the source of truth once extracted — the fix belongs there, not back in `SKILL.md`.

1. **Script produced wrong output** — bug is in the script. Fix it; don't add "then manually adjust X" to SKILL.md.
2. **Script missing a case** — payload script omitted a field, wrong default, mis-formatted value. Fix script; add a test fixture if possible.
3. **Template drift** — wrong footer, missing section, wrong order. Fix the template.
4. **Inline reconstruction despite existing script/template** — SKILL.md still tells the LLM to rebuild the payload. Delete the inline block; point to the script.
5. **Script has no shebang / not executable / wrong interpreter** — verify it runs. `python3` not `python`.

## Model Selection Audit

Per `~/.claude/rules/performance.md`: route by quality, not cost. Mechanical → Haiku (conserve cap). Judgment → Opus/Sonnet. Applies to skills, subagents, and commands — anything with `model:` frontmatter.

1. **Over-powered** — mechanical work (formatting, lookup, simple transforms, rule-checking, routing decisions) on Opus/Sonnet. Drop to Haiku. Example: `daily-tasks` is mechanical routing.
2. **Under-powered** — judgment work (multi-file reasoning, architecture, nuanced writing, security review) on Haiku. Bump.
3. **Unset when it should be set** — skill that always wants a specific model should declare in frontmatter, not inherit.

## Form Conversion Audit

Ask: is this correction in the right container?

1. **Skill ↔ Hook** — skill doing something that should run automatically without invocation (pre-commit validation, post-write formatting, path guardrail) → Hook. Hook gating a judgment call needing LLM reasoning ("should this Notion task be rescheduled?") → Skill.
2. **Skill ↔ Subagent** — skill work that needs context isolation (large reads, research) or a specialized toolset → Subagent. Subagent used inline for a short task main agent could handle → Skill.
3. **Skill ↔ Rule** — truly universal skill advice → Rule (rare). Narrow rule → Skill.

---

# Routing Decision: debate before you edit

For every correction, enumerate ≥2 candidate homes, write one-line PRO + one-line CON for each, pick one, name the tradeoff you're accepting. Then edit. The debate block is the required output format for each item in Step 2.

The 1→5 cascade below is the **tiebreaker** when candidates look equal — NOT a first-match shortcut. A higher-priority match only wins if its CON in the table below doesn't disqualify it for this specific correction (e.g. judgment required → hooks disqualified regardless of cascade position). Skipping the debate is how narrow guidance ends up in CLAUDE.md (see the DS2500 footnote at the bottom of this section).

## Placement tradeoffs (reference for the debate)

| Container | PRO | CON / failure mode |
|---|---|---|
| Extend existing hook | Zero main-context cost; deterministic at tool-call layer; reuses working infra | Widening matcher risks false positives → noise → model learns to ignore hooks. Can't encode judgment. Needs detectable payload shape. |
| New hook | Deterministic; clean separation from unrelated hooks | Setup cost (script + settings + test). Harder to debug than skills. Narrow matcher misses cases; broad matcher nags. |
| Edit existing skill's SKILL.md | Loads exactly when relevant; supports judgment; cheap one-line fix | Every added line is tax on every invocation; bloats fast; buries earlier rules; model skims. |
| Extract to sibling (REFERENCE.md, CANVAS.md, HELP_MODE.md) | Keeps SKILL.md lean; loads only on the trigger path | Pointer indirection not worth it under ~15 lines or when always-on. |
| New skill | Dedicated domain container; own scripts/templates/reference | Discoverability gamble — description must match future phrasing. New maintenance surface. Dilutes the skill registry. |
| Subagent | Context isolation; parallelism; specialized model/tools | Expensive cold-start; overkill for short/mechanical work; prompt-engineering burden. |
| Rule / CLAUDE.md | Loads every turn, every repo — truly global | MAX tax — every line costs in ~all conversations. Narrow guidance here is pure waste. |
| Memory | Persists across conversations; tailors recall | Recall only, not enforcement. Stale memory actively misleads. |
| Script / template (mechanical-mutations) | Removes drift surface entirely; canonical | Only fits structured/mechanical mutations, not judgment calls. |

## Cascade (tiebreaker when candidates look equal)

1. **Is there a hook-shaped fix?** (Payload shape is detectable; no LLM judgment required.)
   - **Check existing hooks first.** List scripts in `~/.claude/hooks/` matching this tool. If one already runs on the footgun's tool, prefer extending its payload inspection over creating a new file — cheaper, one canonical place per tool, no new settings.json entry.
   - **New hook** only if no existing hook matches the tool, OR the existing one has a different concern and extending would bloat it past coherence.
   - Either way: targeted matcher, payload inspection, warn only when the footgun shape is present. Always-on nag walls train the model to ignore hooks.
   - Example (new): Notion date-field writes destroy existing time → `~/.claude/hooks/notion-date-preservation.sh` matched on `mcp__notion__update_page`, NOT CLAUDE.md.
   - Example (extension): `~/.claude/hooks/notion-markdown-guardrails.sh` started with one check and accumulated more as new footgun shapes appeared on the same tool.

2. **Is there a skill already loaded (or would be) in the exact circumstances the correction applies?**
   - If yes: the correction goes in that skill's `SKILL.md` or a sibling reference file. Example: UTC→ET on Canvas `due_at` → `~/.claude/skills/canvas/SKILL.md`, NOT CLAUDE.md. Zero cost outside that path.
   - ≥15 lines or conditionally-read → extract to sibling per Boilerplate Extraction Audit.

3. **Is there an MCP companion skill that loads when that MCP is used?** Same reasoning as #2.

4. **Is the correction TRULY universal — applies to every session regardless of project/tool/topic?**
   - Only then does it belong in CLAUDE.md. Qualifying: `python3` not `python`, no `--no-verify` unless asked, no Co-Authored-By. Everywhere.
   - NOT qualifying: anything naming a specific MCP tool, file format, course, API. These have narrower homes.

5. **If you're about to put something in CLAUDE.md, STOP and re-check #1–#3.** The instinct is to reach for CLAUDE.md because it "feels global"; that instinct is wrong. If a hook could catch it or a skill could carry it, that is strictly better. (Exact mistake from the 2026-04-19 DS2500 session — Notion date-write rule and UTC→ET rule both went in CLAUDE.md despite having obvious narrower homes.)

## Hook extension checklist (when #1 picks "extend existing hook")

- Open the hook's script; locate the existing payload check.
- Add the new footgun detection as an additional clause — preserve existing match logic, do not rewrite.
- Re-test BOTH the pre-existing footgun (should still warn) and the new one (should warn) with synthetic payloads. Also confirm a safe-shape payload still exits silently.
- Confirm the combined warning message preserves severity ordering (DATA CORRUPTION → CORRECTNESS → STYLE) and the new clause does not bury a higher-severity existing one.
- No `settings.json` change — the matcher is unchanged.

## Hook creation checklist (when #1 picks "create a hook")

- Script in `~/.claude/hooks/<name>.sh`: `set -euo pipefail`, read payload from stdin, parse `tool_name` + `tool_input` fields with `jq`, exit 0 silently on non-matching payloads, emit `{hookSpecificOutput: {hookEventName, additionalContext}}` via `jq -nc` only when the footgun shape is present.
- Warning text leads with severity tag (`DATA CORRUPTION:`, `CORRECTNESS:`, `STYLE:`).
- Register in `~/.claude/settings.json` under `hooks.PreToolUse` (or relevant event) with the most specific matcher possible — no `.*` or broad unions unless the footgun truly applies to all.
- Test immediately: pipe synthetic bad-shape payload (should warn), pipe synthetic safe-shape payload (should exit silently).

## Universal-rule additions

If a correction survives to #4, one-sentence addition to `~/.claude/CLAUDE.md`. More than one sentence means it's miscategorized — walk the tree again.
