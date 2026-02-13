## General

Before writing a new script or utility, check `.claude/scripts/` and existing skill folders for reusable tools.

## Secrets & Credentials

Never hardcode API tokens, bot tokens, or chat IDs in scripts — always read from process.env, even in quick prototypes.

When creating or saving credential files (.pem, .key, .env, client_secret*, etc.), verify they are covered by .gitignore and not tracked by git. If already tracked, warn before proceeding.

## Structured Output

When reporting task results, use this format:

```
## Result
- **Status**: SUCCESS | FAILURE | PARTIAL
- **Changes**: [list of files modified]
- **Errors**: [list of errors, or "none"]
- **Next Steps**: [what to do next, or "none"]
```

## Git Commits

Do not include a Co-Authored-By line in commit messages.

When asked to commit, stage all changes — do not selectively pick files.

Lead commit messages with the significant purpose or impact of the change (the "why" or "so what"), then follow with the specific tasks. Example:
- Good: "Clarify that Phase 1 is self-coding, Phase 2 is agent-building; restructure from 6 to 5 phases"
- Bad: "Restructure plan from 6 to 5 phases, add emojis, merge HackerRank/SQL"
