---
name: new-branch
description: Create a new git branch and a worktree for it. Use when user wants to create a new branch, start a new feature branch, or make a branch for experimental changes.
allowed-tools: Bash
---

# New Branch: Create a New Git Branch with Worktree

Create a new git branch, then create a worktree for it so you can work on it in a separate folder/VS Code window.

## When to Use This Skill

- User asks to "create a new branch"
- User wants to "make a new branch"
- User says "start a new feature branch"
- User wants to "branch off" for new work

## Create Branch Workflow

Execute these exact steps in order:

### Step 1: Navigate to the git repository

Navigate to the root of the git repository. Use `git rev-parse --show-toplevel` to find it if needed.

### Step 2: Check current branches

```bash
git branch -a
```

See what branches exist and which one you're currently on.

### Step 3: Create the new branch

```bash
git branch <branch-name>
```

Replace `<branch-name>` with the desired name. This creates the branch but does NOT switch to it.

### Step 4: Create a worktree for the new branch

```bash
git worktree add ../<repo-name>-<branch-name> <branch-name>
```

This creates a new folder `<repo-name>-<branch-name>` with the new branch checked out.

**Example:** If repo is `my-project` and branch is `experiment-rewards`:
```bash
git branch experiment-rewards
git worktree add ../my-project-experiment-rewards experiment-rewards
```

### Step 5: Tell the user how to open the worktree

After the worktree is created, tell the user the full path to the new worktree folder so they can open it in their IDE.

### Step 6: Push the new branch to origin (optional)

From the worktree folder:
```bash
git push -u origin <branch-name>
```

The `-u` flag sets up tracking so future `git push` and `git pull` work automatically.

## Result

| Folder | Branch |
|--------|--------|
| `<repo>` | original branch (e.g., `main`) |
| `<repo>-<branch-name>` | new branch |

Both folders share the same git history. Commits made in either are visible to both.

## Branch Naming Conventions

| Prefix | Use For | Example |
|--------|---------|---------|
| `feature-` | New features | `feature-new-reward-function` |
| `bugfix-` | Bug fixes | `bugfix-landing-detection` |
| `experiment-` | Experimental changes | `experiment-hyperparameters` |
| `refactor-` | Code refactoring | `refactor-training-loop` |

## Removing a Worktree

When you're done with the worktree:
```bash
cd /path/to/main/repo
git worktree remove ../<repo-name>-<branch-name>
```

## Important Notes

- Always verify you're in the correct directory (main repo) before running git commands
- Branch names should be lowercase with hyphens (no spaces)
- The new branch will be based on your current branch at the time of creation
- You cannot have the same branch checked out in two worktrees simultaneously
