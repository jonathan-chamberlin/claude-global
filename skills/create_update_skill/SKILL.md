---
name: create-update-skill
description: Documents the required formatting for creating or updating Claude Code skills so they are auto-discovered. Use when creating a new skill, updating an existing skill, or when a skill isn't showing up in the available skills list.
---

# create_update_skill

Use this skill when creating a new skill or updating an existing one to ensure it is properly formatted and auto-discovered by Claude Code.

## Required SKILL.md Format

Every SKILL.md file MUST start with YAML frontmatter. Without it, Claude Code will not discover the skill.

### Minimum Required Frontmatter

```yaml
---
name: my-skill-name
description: Short description of what the skill does. Use when [trigger conditions].
---
```

### Rules

- name: lowercase letters, numbers, and hyphens only. Max 64 characters. This becomes the /slash-command.
- description: must describe what the skill does AND include "Use when..." trigger phrases so Claude knows when to auto-invoke it.
- The `---` delimiters on their own lines are required. The frontmatter block must be the very first thing in the file.

### Optional Frontmatter Fields

```yaml
---
name: my-skill-name
description: What it does. Use when [triggers].
allowed-tools: Bash(specific-command:*), Read, Write
disable-model-invocation: true
user-invocable: false
argument-hint: [arg1] [arg2]
model: claude-opus
context: fork
agent: Explore
---
```

- allowed-tools: restrict which tools the skill can use
- disable-model-invocation: true means only the user can invoke via /slash-command (Claude won't auto-invoke)
- user-invocable: false means only Claude can auto-invoke (won't appear in slash menu)
- argument-hint: help text shown in the slash command menu
- model: override the model used when skill is active
- context: "fork" runs in a subagent
- agent: which subagent type (Explore, Bash, etc.)

## File Structure

```
.claude/skills/
  my_skill_name/
    SKILL.md          (required - must have YAML frontmatter)
    helper_script.py  (optional - supporting files)
    template.md       (optional - templates)
```

The folder name does NOT need to match the `name` field. Underscores in folder names are fine. Only the `name` field in frontmatter controls the /slash-command name.

## Common Mistake

This will NOT be discovered (missing frontmatter):

```markdown
# my-skill

Use this skill when...
```

This WILL be discovered (has frontmatter):

```markdown
---
name: my-skill
description: Does X. Use when the user asks for Y.
---

# my-skill

Use this skill when...
```

## Checklist When Creating or Updating a Skill

1. Does the file start with `---` on line 1?
2. Does it have a `name` field (lowercase, hyphens, no underscores)?
3. Does it have a `description` field with "Use when..." triggers?
4. Does it end the frontmatter with `---` on its own line?
5. Is the SKILL.md file inside a folder under `.claude/skills/`?
