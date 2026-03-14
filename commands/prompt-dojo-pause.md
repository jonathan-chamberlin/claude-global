Save the current prompt dojo session state so it can be resumed in a new conversation.

1. Write a resume prompt to the current plan file. The resume prompt should:
   - State which phase was completed and which phase is in progress
   - For each completed phase, summarize what gaps were found and how they were resolved
   - For the in-progress phase, list exactly what questions were asked, what answers were given, and what open items remain
   - Include enough detail that a new Claude Code instance running /prompt-dojo could pick up exactly where we left off without re-asking resolved questions
   - Be formatted as a single code block the user can copy-paste after a new /prompt-dojo session responds with "What do you want to build?"

2. After writing the file, output the full file path in a copyable code block like this:

```
C:\Users\Jonathan Chamberlin\.claude\plans\<plan-file-name>.md
```

So the user can easily find and copy the resume prompt.
