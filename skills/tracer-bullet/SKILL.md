---
name: tracer-bullet
description: Build the simplest end-to-end version of a system before investing in any single component. Use when starting a new project, feature, or pipeline and you want to prove the full path works before optimizing. Also use when user mentions "tracer bullet", "end-to-end skeleton", or "simplest version first".
---

# Tracer Bullet

Build the simplest possible end-to-end version of a system before investing in any single component. The goal is to prove the full path works — data in, result out — with the dumbest possible implementation at each step.

## When to Use

- Starting a new project or feature with multiple components (data loading, processing, model, API, UI)
- Unsure whether the pieces will connect properly
- Tempted to perfect one component before building the others

## Process

### Phase 1: Define the Path

Identify every component the system needs, end to end. Write them as a linear chain:

```
[Data Source] → [Loading] → [Processing] → [Model/Logic] → [Output/API] → [Consumer]
```

Ask the user: "What's the full path from input to output?" Don't assume — different projects have different chains.

### Phase 2: Write tracer.md

Create `tracer.md` in the project root with this structure:

```markdown
# Tracer Bullet Plan

## End-to-End Path
[Component 1] → [Component 2] → ... → [Final Output]

## Simplest Implementation Per Component
| Component | Tracer Version | Real Version (later) |
|-----------|---------------|---------------------|
| Data loading | Hardcoded 10 rows | Full dataset with streaming |
| Processing | No-op passthrough | Feature engineering pipeline |
| Model | Return most popular / random | Trained neural net |
| API | Print to console | FastAPI endpoint |

## Open Questions
- [ ] Question 1
- [ ] Question 2

## Success Criteria
The tracer works when: [describe what "end to end works" means concretely]
```

### Phase 3: Build It

Implement each component in the tracer column — nothing more. Rules:

- **No optimization.** Hardcode values, use naive algorithms, skip edge cases.
- **No abstraction.** Put it all in one file if possible. Refactor later.
- **No perfectionism.** The model can return a constant. The API can be a print statement. The data loader can read 10 rows.
- **Wire everything together.** The whole point is that data flows from start to finish.

### Phase 4: Run It

Execute the full path. Either it works end-to-end or it doesn't. If it doesn't, fix the connection that broke — don't improve any component.

### Phase 5: Mark What's Real

Update `tracer.md`: check off which components are now ready to be replaced with real implementations. The user decides what to upgrade first.

## Anti-Patterns

| Anti-Pattern | Why It Fails | Do Instead |
|---|---|---|
| Perfect the data loader before building anything else | You don't know if the rest of the pipeline even works | Hardcode 10 rows, move on |
| Build abstractions for future flexibility | You don't know what flexibility you'll need yet | Inline everything, refactor after tracer works |
| Skip a component ("we'll add the API later") | That's the component most likely to break the chain | Stub it, even if it's a print statement |
| Spend time on error handling | Errors in a tracer are useful signals, not problems to suppress | Let it crash, fix the real issue |
