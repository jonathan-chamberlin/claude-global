## General

Before writing a new script or utility, check `.claude/scripts/` and existing skill folders for reusable tools.

## Communication
No bullshit. Be honest. Dont try to impress me.

When launching subagents, paste content the main agent already has directly into the prompt instead of having subagents re-read files via tools.

## Secrets & Credentials

Never hardcode API tokens, bot tokens, or chat IDs in scripts — always read from process.env, even in quick prototypes.

When creating or saving credential files (.pem, .key, .env, client_secret*, etc.), verify they are covered by .gitignore and not tracked by git. If already tracked, warn before proceeding.

Before making the first commit in a new repo, scan all staged files for secrets using Grep (patterns: api_key, token, secret, password, private_key, API_KEY, Bearer, sk-, ANTHROPIC_API_KEY, and similar). Also check any .json, .env, .yaml, .toml, and config files individually. Add any files containing secrets to .gitignore and unstage them before committing.

## Structured Output

When reporting task results, use this format:

```
## Result
- **Status**: SUCCESS | FAILURE | PARTIAL
- **Changes**: [list of files modified]
- **Errors**: [list of errors, or "none"]
- **Next Steps**: [what to do next, or "none"]
```

## Debugging

When fixing a bug where data isn't reaching the UI, trace the full pipeline end-to-end in one pass: data production → state/storage → API/message response fields → UI polling triggers → UI rendering branches.

When the user reports a bug and you can't identify the root cause after 2 failed fix attempts, use `/delegate` to hand off rather than continuing to hypothesize at the same layer.

## Git Commits

Do not include a Co-Authored-By line in commit messages.

When asked to commit, stage all changes — do not selectively pick files.

When merging a worktree branch that contains temporary identification changes (e.g., renamed manifest.json), immediately revert those changes and commit after the merge.

Lead commit messages with the significant purpose or impact of the change (the "why" or "so what"), then follow with the specific tasks. Example:
- Good: "Clarify that Phase 1 is self-coding, Phase 2 is agent-building; restructure from 6 to 5 phases"
- Bad: "Restructure plan from 6 to 5 phases, add emojis, merge HackerRank/SQL"
