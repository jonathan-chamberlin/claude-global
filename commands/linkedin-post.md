---
description: Write a LinkedIn post with clarifying questions and tone review
---

Write a LinkedIn post following the exact guidelines below. The user will provide context and optionally reference files to read for additional context.

## Guidelines

Follow EVERY rule in these two documents. Violations are unacceptable.

### Structure Rules
${{C:\Users\Jonathan Chamberlin\.claude\commands\resources\linkedin_structure.md}}

### Tone Rules
${{C:\Users\Jonathan Chamberlin\.claude\commands\resources\linkedin_tone.md}}

## Workflow

### Step 1: Read Context Files
If the user referenced any files (paths after "Read files:"), read each one using the Read tool. These provide context for the post.

### Step 2: Clarifying Questions
Before writing anything, ask the user 3 multiple-choice clarifying questions using AskUserQuestion. Each question should have 3 options. Questions should cover:
1. Tone/voice (e.g. casual storytelling vs technical vs inspirational)
2. Focus/emphasis (e.g. personal experience vs product vs technical decisions)
3. Target audience (e.g. developers vs founders vs general)

### Step 3: Write Draft
Using the context, file contents, and user's answers, write a LinkedIn post draft. Follow every guideline above strictly.

When the post contains a sequence of items, steps, or observations (3+), use a bulleted list. Bullets improve scannability on LinkedIn. Keep each bullet to one line, no sub-bullets. The list should sit inside the narrative, not replace it (introduce it with a sentence, and continue after it).

### Step 4: Self-Review
Review your own draft against EVERY rule in both guideline documents. Output your critique with specific violations quoted, then output a revised post that fixes all violations. Format:

```
CRITIQUE:
- [rule violated]: "quoted offending text"
...

REVISED POST:
[full corrected post]
```

Suggest 4 screenshots that could be included. They can be real screenshots on this computer, in a repo, or pics the user could take, or pics the user might have already taken.

### Step 5: Present to User
Show the revised post with character count. Ask the user using AskUserQuestion:
- "Post as-is" (copy to clipboard)
- "Modify" (ask what to change, then revise and re-review)
- "Regenerate" (start fresh from Step 3)
- "Cancel"

If the user chooses Modify, apply their feedback, re-review against guidelines, and present again. Repeat until they're satisfied.

## Usage
```
/linkedin-post {context} Read files: {file paths}
```
