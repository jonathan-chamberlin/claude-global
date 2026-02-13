---
name: openclaw
description: Reference for building with OpenClaw (aka Clawdbot) — the agent runtime for skills, Telegram bots, and cron jobs. Use when creating skills, configuring the gateway, setting up cron, or debugging why a skill doesn't work in the bot.
---

# OpenClaw / Clawdbot — Architecture Reference

## Critical Constraint: Skills Cannot Execute Code

The embedded agent (Gemini Flash via OpenRouter) has these tools ONLY:
`read`, `write`, `edit`, `browser`, `cron`, `message`, `sessions_list`, `sessions_history`, `sessions_send`, `sessions_spawn`, `web_search`, `web_fetch`

**There is NO bash, exec, or shell tool.** The agent cannot `import()` JavaScript modules or run Node.js scripts. Skills are documentation — their SKILL.md is injected into the system prompt as XML, and the agent reads them with the `read` tool. Skills describe what the bot can do using its existing tools, they don't add new executable capabilities.

If you need code to run on a schedule, use a **standalone script + OS-level scheduler** (Windows Task Scheduler / cron), not clawdbot cron. See "Workaround: Standalone Scripts" below.

## Skill Loading Pipeline

1. `loadSkillsFromDir()` (pi-coding-agent) recursively discovers `SKILL.md` files
2. `loadSkillEntries()` merges from bundled, managed, and workspace `skills/` dirs
3. `shouldIncludeSkill()` filters by env vars, binaries, OS, config
4. `buildWorkspaceSkillCommandSpecs()` generates command specs for user-invocable skills
5. `formatSkillsForPrompt()` creates XML: `<available_skills><skill><name>...<description>...</skill></available_skills>`

### Frontmatter Gotchas

**`requires.env` in standard YAML frontmatter is NOT parsed by clawdbot.** The gateway's `resolveClawdbotMetadata()` looks for a `metadata` frontmatter field containing JSON5 with a `clawdbot` object. Standard YAML `requires.env` is ignored — `entry.clawdbot` defaults to `undefined`, so the env check is skipped and the skill loads regardless.

To actually gate a skill on env vars, use the `metadata` JSON5 format (check clawdbot source for current syntax). In practice, most workspace skills load unconditionally.

**Skills without dashes in their names load silently.** The "Sanitized skill command name" debug log only fires for names containing dashes (e.g., "email-skill" logs, "kalshi" does not). Don't assume a skill isn't loading just because it doesn't appear in the log.

### SKILL.md Frontmatter

```yaml
---
name: my-skill           # Must match parent directory name, lowercase a-z/0-9/hyphens
description: What it does # Shown in skill list
user-invocable: true      # Set true so users can trigger it via /my-skill in Telegram
---
```

## Cron System

### Payload Kinds

- `agentTurn` — sends a message to the LLM agent (isolated or main session)
- `systemEvent` — triggers a system-level event

**There is no `script` or `exec` payload kind.** Cron jobs send messages to the agent, which can only use its available tools (no shell). This means cron CANNOT directly execute JavaScript functions.

### Cron Job Config

Jobs live at `~/.openclaw/cron/jobs.json`. Add via `clawdbot cron add` CLI or edit directly.

```json
{
  "name": "Job Name",
  "enabled": true,
  "schedule": { "kind": "cron", "expr": "*/30 * * * *", "tz": "America/New_York" },
  "sessionTarget": "isolated",
  "wakeMode": "next-heartbeat",
  "payload": {
    "kind": "agentTurn",
    "message": "Your prompt to the agent",
    "deliver": true,
    "channel": "telegram",
    "to": "CHAT_ID"
  }
}
```

## Workaround: Standalone Scripts

For code that needs to run on a schedule (API calls, data processing, sending alerts):

1. Write a standalone Node.js script that imports your functions directly
2. Read credentials from `process.env` via `import 'dotenv/config'` (never hardcode)
3. Send to Telegram via the bot HTTP API: `https://api.telegram.org/bot{TOKEN}/sendMessage`
4. Schedule with **Windows Task Scheduler** (`schtasks`) or OS cron
5. Use a `.bat` wrapper for Task Scheduler on Windows

```
schtasks /create /tn "Job Name" /tr "path\to\wrapper.bat args" /sc minute /mo 30 /f
```

On Git Bash, prefix with `MSYS_NO_PATHCONV=1` to prevent path mangling of `/create`, `/tn`, etc.

**Disable the corresponding clawdbot cron job** (set `enabled: false` in `jobs.json`) to avoid the LLM receiving messages it can't act on.

## Gateway

### Config Locations

| File | Purpose |
|------|---------|
| `~/.clawdbot/clawdbot.json` | Gateway config (workspace, model, Telegram bot token, native skills) |
| `~/.clawdbot/.env` | Gateway environment variables (loaded at boot) |
| `~/.openclaw/cron/jobs.json` | Cron job definitions |
| `~/.openclaw/agents/main/sessions/*.jsonl` | Session logs with usage/cost data |

### Starting the Gateway

```bash
cd /path/to/workspace && npx clawdbot gateway run
```

Useful flags:
- `--verbose` — enables debug logging (subsystem logs for channel startup, skill loading, etc.)
- `--force` — overrides the gateway lock file. Essential in Docker where a previous container may have left a stale lock.

There is no `--daemon` flag. For background operation, use a process manager or run in a background terminal.

### Docker Deployment

The official OpenClaw Docker setup uses:
- Base image: `node:22-bookworm` (Debian, not Alpine)
- Command: `node dist/index.js gateway`
- User: `node` (UID 1000)
- Setup: `docker-setup.sh` script or manual `docker compose run --rm openclaw-cli onboard`
- Telegram: `channels add --channel telegram --token <token>` CLI, or manually set `channels.telegram.botToken` in `clawdbot.json`

**Memory:** The gateway needs ~450MB RAM minimum. On memory-constrained VMs (e.g., Oracle Cloud Free Tier 1GB), it may never finish initializing if swap is exhausted — producing zero output and no logs.

**Config writing gotcha:** Writing `clawdbot.json` from a shell heredoc (especially over SSH) can mangle JSON quotes, producing invalid JSON5. Use Python `json.dump()` or `node -e 'fs.writeFileSync(..., JSON.stringify(config, null, 2))'` instead.

Example `clawdbot.json` for Docker with Telegram:

```json
{
  "meta": { "lastTouchedVersion": "2026.1.24-3" },
  "gateway": { "mode": "local" },
  "channels": { "telegram": { "botToken": "YOUR_BOT_TOKEN" } },
  "commands": { "native": "auto", "nativeSkills": "auto" }
}
```

### Known Stability Issues

- **`TypeError: fetch failed`** — recurring unhandled promise rejection (likely Telegram polling or bonjour). Mitigate with `NODE_OPTIONS="--unhandled-rejections=warn"` but gateway may still crash.
- **Bonjour name conflicts** — multiple gateway instances on the same machine cause hostname conflicts. Kill all instances before restarting.
- **Telegram polling stolen** — if an old gateway instance is still running, it steals the Telegram polling connection from the new one. Always kill old processes first.

### Useful Commands

```bash
# Start gateway
npx clawdbot gateway run

# Add cron job
npx clawdbot cron add

# List cron jobs
npx clawdbot cron list

# Check gateway status
npx clawdbot gateway status
```

## Telegram Integration

### Token Resolution Priority

The gateway resolves the Telegram bot token in this order (from `dist/telegram/token.js`):

1. `channels.telegram.accounts.<id>.tokenFile` — path to a file containing the token
2. `channels.telegram.accounts.<id>.botToken` — inline token for a specific account
3. `channels.telegram.tokenFile` — path to a file containing the token (global)
4. `channels.telegram.botToken` — inline token (global) ← **most common for single-bot setups**
5. `TELEGRAM_BOT_TOKEN` environment variable — fallback

**WARNING:** `providers.telegram.token` does NOT work — clawdbot rejects it with "Unrecognized key: providers". Use `channels.telegram.botToken` in `clawdbot.json`.

The channel plugin's `isConfigured` check (`dist/channels/plugins/telegram.js`) requires `Boolean(account.token?.trim())`, so the token must be a non-empty string.

For standalone scripts that bypass the gateway, call the Telegram API directly:

```javascript
const resp = await fetch(`https://api.telegram.org/bot${TOKEN}/sendMessage`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    chat_id: CHAT_ID,
    text: message.slice(0, 4096),
    parse_mode: 'Markdown',
  }),
});
// If Markdown parsing fails, retry without parse_mode
```

## Summary: What Goes Where

| Need | Solution |
|------|----------|
| Bot answers questions about a topic | Write a skill (SKILL.md with documentation) |
| Bot reads/writes files on command | Skill using the agent's `read`/`write` tools |
| Run code on a schedule | Standalone Node.js script + OS scheduler |
| Send alerts to Telegram | Standalone script calling bot API directly |
| LLM-powered conversation on schedule | Clawdbot cron with `agentTurn` payload |
