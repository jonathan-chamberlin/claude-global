# Happy-Coder Setup Guide
## Claude Code on Your iPhone

### Overview
Happy-Coder allows you to control Claude Code from your iPhone using your Claude Max subscription tokens (NOT API credits). This setup is **free** beyond your existing Claude Max subscription ($100-200/month).

### Installation Status
- ✅ **Happy-Coder CLI installed** (v0.13.0)
- ✅ **ANTHROPIC_API_KEY not set** (using subscription tokens)
- ✅ **Skills directory accessible** (~/.claude/skills/)
- ✅ **Global instructions loaded** (~/.claude/CLAUDE.md)
- ⚠️ **Authentication needed** (see Step 2 below)
- ⚠️ **GitHub token needed** (see Step 3 below)

---

## Quick Start (5 minutes)

### Step 1: Open Windows Terminal (PowerShell)
**Important:** Don't run Happy-Coder from Git Bash or inside another Claude Code session. Use Windows Terminal with PowerShell.

1. Press `Win + X`
2. Select "Windows Terminal" or "PowerShell"
3. Navigate to your home directory: `cd ~`

### Step 2: Authenticate with Happy-Coder
```powershell
# Check current authentication status
happy auth status

# If not authenticated, login (this will open an interactive prompt)
happy auth login

# Follow the prompts:
# - Select "1. Mobile App" if you want to use iPhone app
# - OR select "2. Web Browser" if you want web access too
```

**Expected output:**
- QR code or pairing code will be displayed
- Keep this terminal window open for Step 4

### Step 3: Set GitHub Token (If Not Already Set)
To push changes from your phone to GitHub, you need a token:

```powershell
# Check if token is set
$env:GITHUB_TOKEN

# If empty, create a GitHub token:
# 1. Go to https://github.com/settings/tokens
# 2. Click "Generate new token (classic)"
# 3. Select scopes: repo, workflow, write:packages
# 4. Generate and copy the token

# Set the token permanently
[System.Environment]::SetEnvironmentVariable('GITHUB_TOKEN', 'your-token-here', 'User')

# Verify it's set
$env:GITHUB_TOKEN
```

### Step 4: Install iOS App & Pair
1. Open App Store on your iPhone
2. Search for "Happy-Coder" or "Happy Coder Claude"
3. Download and install the app
4. Open the app
5. Scan the QR code from Step 2 (or manually enter pairing code)
6. Wait for "Connected" status

### Step 5: Start Your First Session
```powershell
# From Windows Terminal, start Happy-Coder
happy

# This will:
# - Start monitoring for Claude Code requests from your phone
# - Display connection status
# - Show activity when you send prompts from iPhone
```

**Keep this terminal window open** while using Claude Code from your phone.

### Step 6: Test from iPhone
1. Open Happy-Coder app on iPhone
2. Tap "New Session" or similar
3. Send test prompt: "List all available skills in ~/.claude/skills/"
4. Verify you see your skills listed
5. Test a slash command: "/help"

---

## Common Workflows

### Start a New Coding Session
**From iPhone:**
1. Open Happy-Coder app
2. Tap "New Session"
3. Send prompt: "Change to C:\Repositories for Git\[your-repo-name]"
4. Send your coding request: "Add a new function to handle X"

### Commit Changes
**From iPhone:**
```
Please commit these changes with message: "Add feature X"
```

Or use the slash command:
```
/commit
```

### Push to GitHub
**From iPhone:**
```
Push changes to GitHub
```

### Switch Repositories
**From iPhone:**
```
Change to C:\Repositories for Git\[different-repo]
```

### Use Skills
**From iPhone:**
```
/pdf                          # Convert document to PDF
/debug                        # Debug current code
/merge-to-main               # Merge current branch to main
```

### Work with Multiple Repos Simultaneously
**From Windows Terminal:**
```powershell
# Start multiple Happy sessions (in different terminal tabs)
# Tab 1:
happy --resume session-1

# Tab 2 (new terminal):
happy --resume session-2

# Each session can work on a different repo
# Switch between them in the iPhone app
```

---

## Important Reminders

### ⚠️ CRITICAL: Don't Use API Key
**Never set ANTHROPIC_API_KEY** when using Happy-Coder. This would charge you API credits instead of using your Claude Max subscription.

**To verify you're using subscription tokens:**
```powershell
# This should be empty:
$env:ANTHROPIC_API_KEY

# If it shows a value, remove it:
[System.Environment]::SetEnvironmentVariable('ANTHROPIC_API_KEY', $null, 'User')
[System.Environment]::SetEnvironmentVariable('ANTHROPIC_API_KEY', $null, 'Machine')
```

**Monitor your usage:**
- Check https://console.anthropic.com/settings/usage
- You should see subscription usage, NOT API charges
- API usage costs ~$0.80/request × 200 requests/day = $4,800/month
- Claude Max with subscription: $100-200/month
- **Savings: $4,600-4,700/month!**

### 🔒 Security Features
- End-to-end encryption (relay server can't read your data)
- Local key generation
- Secure pairing via QR code or PIN

### 💡 Best Practices
1. **Keep Windows Terminal open** while using Happy-Coder from phone
2. **Use descriptive commit messages** - Claude will draft them, but review before confirming
3. **Test on small changes first** before doing major refactoring from phone
4. **Use skills** - They're available on phone just like desktop (e.g., /commit, /pdf)
5. **Push frequently** - Easier to revert small changes than large ones

---

## Troubleshooting

### "Raw mode is not supported" Error
**Cause:** Running Happy-Coder from Git Bash or inside Claude Code session

**Solution:**
1. Exit Git Bash
2. Open Windows Terminal with PowerShell
3. Run `happy auth login` again

### "Not authenticated" Error
**Cause:** Haven't completed authentication flow

**Solution:**
```powershell
happy auth status          # Check status
happy auth login --force   # Re-authenticate (clears old auth)
```

### Changes Not Pushing to GitHub
**Cause:** GITHUB_TOKEN not set or expired

**Solution:**
```powershell
# Check token
$env:GITHUB_TOKEN

# If empty or invalid, set new token (see Step 3 above)
[System.Environment]::SetEnvironmentVariable('GITHUB_TOKEN', 'your-new-token', 'User')
```

### Skills Not Available
**Cause:** Happy-Coder can't access ~/.claude/skills/ directory

**Solution:**
```powershell
# Verify skills exist
ls ~/.claude/skills/

# If empty, skills might be in wrong location
# Check your Claude Code config
```

### iPhone App Won't Connect
**Cause:** Firewall blocking connection or pairing code expired

**Solutions:**
1. Check Windows Firewall settings
2. Regenerate pairing code: `happy auth login --force`
3. Try web browser option instead of mobile app
4. Ensure both devices have internet connection

### "Cannot launch inside another Claude Code session"
**Cause:** Trying to run Happy-Coder from within active Claude Code

**Solution:**
1. Exit current Claude Code session
2. Open new terminal
3. Run `happy` from fresh terminal

---

## Advanced Usage

### Run Happy-Coder in Background (Daemon Mode)
```powershell
# Start daemon (runs in background)
happy daemon start

# Check status
happy daemon status

# Stop daemon
happy daemon stop

# View logs
happy daemon logs
```

### Use Custom Claude Code Options
```powershell
# Resume previous session
happy --resume

# Run with --yolo mode (skip permission prompts)
happy --yolo

# Use custom API endpoint (e.g., for testing)
happy --claude-env ANTHROPIC_BASE_URL=http://127.0.0.1:3456
```

### Send Push Notifications
```powershell
# Send notification to your phone when task completes
happy notify "Build completed successfully!"
```

### Diagnostics
```powershell
# Run system diagnostics
happy doctor

# This checks:
# - Claude Code installation
# - Authentication status
# - Network connectivity
# - Configuration issues
```

---

## What's Possible from Your Phone

### ✅ You Can:
- Start new Claude Code sessions
- Write and edit code across multiple files
- Run tests and see output
- Commit changes with slash commands (/commit)
- Push to GitHub
- Use all your custom skills from ~/.claude/skills/
- Access CLAUDE.md global instructions
- Switch between different repositories
- Run multiple parallel sessions
- Get real-time output and error messages
- Review diffs before committing

### ❌ You Cannot (inherently limited by phone):
- View large file diffs easily (phone screen size)
- Edit files directly (Claude does it based on your prompts)
- Run GUI applications
- Use IDE features (debugging UI, etc.)

### 💡 Pro Tips for Phone Usage:
- **Use voice dictation** for longer prompts
- **Be specific** in your requests (harder to review on phone)
- **Ask Claude to explain** code before making changes
- **Use /commit often** - smaller commits are easier to review
- **Request summaries** after complex operations

---

## Cost Summary

| Item | Cost | Notes |
|------|------|-------|
| Claude Max Subscription | $100-200/month | Required, you already have this |
| Happy-Coder Software | **FREE** | Open-source, MIT license |
| Happy Relay Server | **FREE** | Included with Happy-Coder |
| iOS App | **FREE** | Available on App Store |
| GitHub | **FREE** | For public repos |
| **Total Additional Cost** | **$0/month** | No extra charges! |

### If You Used API Instead (DON'T DO THIS):
| Usage Pattern | API Cost | Subscription Cost | Waste |
|---------------|----------|-------------------|-------|
| 200 requests/day | ~$4,800/month | $100-200/month | **$4,600-4,700/month** |
| 100 requests/day | ~$2,400/month | $100-200/month | **$2,200-2,300/month** |
| 50 requests/day | ~$1,200/month | $100-200/month | **$1,000-1,100/month** |

**Bottom line:** Using your subscription tokens saves thousands per month!

---

## Quick Reference Commands

### Windows Terminal (PowerShell)
```powershell
# Start Happy-Coder
happy

# Resume previous session
happy --resume

# Check authentication
happy auth status

# Re-authenticate
happy auth login --force

# Run diagnostics
happy doctor

# Start daemon
happy daemon start

# Check GitHub token
$env:GITHUB_TOKEN

# Check API key (should be empty!)
$env:ANTHROPIC_API_KEY
```

### iPhone App
- **New Session:** Tap "+" or "New Session"
- **Switch Sessions:** Swipe or tap session list
- **Send Prompt:** Type or use voice dictation
- **View Output:** Scroll through response
- **Pause/Stop:** Tap pause or stop button

---

## Getting Help

### Happy-Coder Support
- GitHub: https://github.com/happy-tools/happy-coder
- Documentation: https://happy.engineering/
- Issues: https://github.com/happy-tools/happy-coder/issues

### Claude Code Support
- Help: Run `/help` from Claude Code
- GitHub: https://github.com/anthropics/claude-code
- Feedback: https://github.com/anthropics/claude-code/issues

### Your Setup
- Skills: `~/.claude/skills/`
- Global Config: `~/.claude/CLAUDE.md`
- Scripts: `~/.claude/scripts/`
- Repos: `C:\Repositories for Git\`

---

## Next Steps After Setup

1. ✅ Complete authentication (Step 2 above)
2. ✅ Set GitHub token (Step 3 above)
3. ✅ Pair iPhone app (Step 4 above)
4. ✅ Test basic workflow (Step 6 above)
5. 📖 Read "Common Workflows" section
6. 🧪 Test with a small repo first
7. 🚀 Start coding from anywhere!

---

**Last Updated:** 2026-02-16
**Happy-Coder Version:** 0.13.0
**Claude Code Version:** 2.1.44
