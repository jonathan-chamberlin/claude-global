# Happy-Coder Quick Reference Card

## 🚀 Start Session
**Windows PowerShell:**
```powershell
happy                    # Start new session
happy --resume           # Resume previous session
happy --yolo            # Skip permission prompts
```

## 📱 iPhone Prompts

### Navigation
```
Change to C:\Repositories for Git\[repo-name]
List all files in current directory
Show me the contents of [filename]
```

### Code Changes
```
Create a new file called [filename] with [description]
Add a function to [filename] that does [task]
Fix the bug in [filename] at line [number]
Refactor [function-name] to use [pattern]
```

### Git Operations
```
/commit                                    # Commit all changes
Commit these changes with message: "[msg]"  # Custom commit message
Push changes to GitHub                      # Push to remote
Show git status                            # Check status
Show recent commits                        # View history
```

### Skills (Slash Commands)
```
/help                    # Show available commands
/commit                  # Commit changes
/pdf                     # Convert to PDF
/debug                   # Debug current code
/merge-to-main          # Merge to main branch
/new-branch             # Create new branch
```

### Information
```
List all available skills
What slash commands are available?
Explain what this code does
Show me the project structure
```

## ⚙️ Setup Commands

**First Time Setup:**
```powershell
# 1. Authenticate
happy auth login

# 2. Set GitHub token
[System.Environment]::SetEnvironmentVariable('GITHUB_TOKEN', 'your-token', 'User')

# 3. Start Happy-Coder
happy
```

**Daily Use:**
```powershell
# Just start Happy-Coder
happy

# Or resume previous session
happy --resume
```

## 🔧 Troubleshooting

| Issue | Command | Notes |
|-------|---------|-------|
| Not authenticated | `happy auth login --force` | Re-authenticate |
| Can't connect | `happy doctor` | Run diagnostics |
| Wrong terminal | Use PowerShell, not Git Bash | Exit and reopen |
| API key set | `$env:ANTHROPIC_API_KEY` should be empty | Remove if set |
| GitHub push fails | Check `$env:GITHUB_TOKEN` | Generate new token if needed |

## ⚠️ Critical Reminders

1. **Never set ANTHROPIC_API_KEY** - Uses expensive API credits instead of subscription
2. **Keep terminal open** - Happy-Coder needs to run while using phone
3. **Use PowerShell** - Git Bash doesn't support interactive prompts
4. **Push frequently** - Easier to revert small commits

## 📊 Cost Check

```powershell
# Verify subscription usage (should be empty):
$env:ANTHROPIC_API_KEY

# If you see a value, REMOVE IT:
[System.Environment]::SetEnvironmentVariable('ANTHROPIC_API_KEY', $null, 'User')

# Check usage at: https://console.anthropic.com/settings/usage
# Should show subscription usage, NOT API charges
```

## 🎯 Best Practices

**From iPhone:**
- Use voice dictation for long prompts
- Be specific (harder to review on phone)
- Commit often (smaller changes)
- Test with small repos first

**From Windows:**
- Keep Happy-Coder running in terminal
- Use daemon mode for background operation
- Run diagnostics if issues: `happy doctor`

## 📍 Important Paths

| Location | Path |
|----------|------|
| Skills | `C:\Users\Jonathan Chamberlin\.claude\skills\` |
| Global Config | `C:\Users\Jonathan Chamberlin\.claude\CLAUDE.md` |
| Scripts | `C:\Users\Jonathan Chamberlin\.claude\scripts\` |
| Repos | `C:\Repositories for Git\` |

## 🔗 Resources

- Full guide: `~/.claude/scripts/happy-coder-setup-guide.md`
- Happy-Coder docs: https://happy.engineering/
- Claude Code help: `/help` or https://github.com/anthropics/claude-code

---

**Print this and keep it handy for phone coding sessions!**
