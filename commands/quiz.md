Create a practice exam, grade it, and offer a retake targeting weak spots.

## Arguments
- The user will specify which class materials to read (files, folders, or notebooks)
- Optionally a number of questions (default: 6)

## Step 1: Create the exam

1. Read all source materials the user pointed to (analysis.py, notebooks, etc.)
2. Identify every key concept covered
3. Create `test.md` in the same folder as the source materials
4. Use 6 questions (or the number the user specified)
5. Every example must be completely unrelated to the source material — different domain, different variable names, different scenario. If the source uses dogs and weather, use movies and recipes. Never reuse examples from the source.
6. Format rules:
   - Title: `# Class XX Topic — Practice Exam`
   - Instruction line: `Write your answers in the code blocks. You cannot run the code, so write carefully.`
   - `---` separators between questions
   - Code questions use fenced code blocks with `# your answer` placeholder
   - Conceptual questions use plain fenced blocks with `# your answer`
   - Leave 3 blank lines inside each answer block for writing space
7. Mix question types: some "write the code", some "what's wrong with this code", some conceptual "explain the difference"
8. Questions should progress from basic recall to applied/synthesis

## CRITICAL: Do not reveal answers

After creating the file, say only: "Created test.md with N questions. Answer when ready."

**Do NOT list what the questions cover. Do NOT summarize the topics. Do NOT describe what each question tests.** Any of this gives away the answers. The user will read the file themselves.

## Step 2: Grade

When the user says "check", "grade", or "done":

1. Read the current state of the test file
2. Grade each question:
   - **Correct**: say "Correct." and move on
   - **Partially correct**: say what's right, then what's wrong. Be specific — name the exact syntax error, wrong method, or missing piece
   - **Wrong**: explain why and what the correct approach is
3. Give a score: **X / N**
4. After grading, if the user got anything wrong, ask: "Want to fix and re-check, or want a retake exam targeting the concepts you missed?"

## Step 3: Re-grading

When the user fixes answers and says "check again":
- Only comment on questions that changed or still have issues
- If everything is now correct, just say the new score
- After re-grading, again offer the retake if there are still gaps

## Step 4: Retake exam

If the user wants a retake:
1. Create `test2.md` (or `test3.md`, etc.) in the same folder
2. Only test concepts the user got wrong or partially wrong
3. Use completely different examples from both the source material AND the previous test(s)
4. Same format rules as Step 1
5. Same "do not reveal answers" rule
6. Say only: "Created testN.md with N questions targeting [X concept, Y concept]. Answer when ready."
   - For retakes only, naming the targeted concepts is OK since the user already knows what they got wrong
