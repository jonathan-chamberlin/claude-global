---
description: Review code structure and identify refactoring opportunities
---

Review all files in the target path to see where the code could be put closer to its ideal size and shape. Analyze the codebase for refactoring opportunities — both for human readability AND for AI agent readability (reducing hallucination and "fix one thing, break another" errors). Be specific and actionable.

## Metrics to Enforce
- Functions: ≤40 lines, ≤4 parameters, cyclomatic complexity ≤10
- Classes: ≤300 lines, single responsibility
- Modules: ≤500 lines, cohesive purpose

## Code Smells to Detect
- God classes / functions doing too much
- Feature envy (method uses another class's data excessively)
- Long parameter lists (→ parameter objects)
- Duplicate logic (→ extract shared utility)
- Primitive obsession (→ value objects)
- Shotgun surgery (one change = edits across many files)
- Deep nesting (≥3 levels → early returns or extraction)

## AI Readability Smells to Detect

These patterns cause AI coding agents to hallucinate, miss dependencies, or break things when editing code. Flag them alongside traditional code smells.

### Implicit dependencies (highest priority — #1 cause of "fix one thing, break another")
- **Globals and shared mutable state** — AI can't see cross-file side effects. Extract into explicit function parameters or injected config objects.
- **Barrel exports / re-exports** — `index.js` files that re-export from many modules hide where things actually live. AI agents miss transitive dependencies. Prefer direct imports.
- **Monkey-patching / prototype mutation** — AI treats the original definition as truth and misses runtime modifications.
- **Event-driven coupling without clear subscriber lists** — When file A emits events and files B, C, D listen, AI editing file A doesn't know B/C/D exist. Add a comment listing known subscribers, or co-locate event definitions with their handlers.

### Magic values
- **Magic numbers and strings** — Hardcoded `1000`, `"pending"`, `0.25` scattered through code. AI invents plausible but wrong values when editing nearby code. Extract to named constants (`MAX_BATCH_SIZE`, `STATUS_PENDING`, `ALARM_PERIOD_MINUTES`).
- **Duplicated literals** — The same string or number used in 3+ places without a constant. AI will update some occurrences but miss others.

### Missing type information (for typed languages)
- **Untyped function signatures** — AI hallucinates parameter types and return types when not specified. Add type annotations to all exported functions at minimum.
- **`any` / loose types** — Broad types remove constraints that help AI generate correct code. Use specific types.
- **Implicit return types** — Even if the language can infer them, explicit return types help AI understand intent without reading the full function body.

### Comment anti-patterns
- **Stale comments that contradict code** — AI trusts comments over code and generates wrong edits. Delete or update stale comments.
- **"What" comments on obvious code** — `// increment counter` above `counter++` wastes context window tokens. Delete these.
- **Missing "why" comments on non-obvious logic** — Edge cases, workarounds, business rules, and constraints need comments explaining WHY, not what. AI misses these and removes important guardrails.

### Coupling and file organization
- **Files over 500 lines** — Context window strain causes AI to lose track of code at the top when editing code at the bottom (lost-in-the-middle effect). Split into focused modules.
- **Functions over 50 lines** — AI generates larger deviations when errors occur in long functions, requiring extensive rewrites. Keep functions short.
- **Cross-cutting concerns mixed into business logic** — Logging, auth checks, validation mixed inline. AI editing business logic accidentally removes safety checks. Extract to middleware, decorators, or wrapper functions with clear names.
- **Deep inheritance hierarchies** — AI struggles to trace method resolution order. Prefer composition and explicit delegation.

### Testability
- **Untested public interfaces** — AI has no way to verify its edits didn't break behavior. Flag exported functions without corresponding tests. Tests are the single highest-leverage thing for AI accuracy.
- **Hard-to-test coupling** — Functions that require complex setup or mock many dependencies. Simplify interfaces so tests (and AI verification) are straightforward.

## Domain-Specific Concerns (apply when relevant)
- RL/ML: Agent/environment coupling, replay buffer leaks, policy/value separation
- API integrations: Config hardcoding vs. injectable parameters, god modules mixing config/auth/clients/utilities

## Output Format
For each opportunity:
```
### [Priority: HIGH/MED/LOW] <Summary>
- **File:** `path/to/file:L##-L##`
- **Smell:** <which code smell or AI readability smell>
- **Refactor:** <specific pattern to apply>
- **AI impact:** <how this reduces AI errors — e.g., "eliminates implicit dependency that causes missed updates" or "N/A if purely human readability">
- **Risk:** <breaking change? test impact?>
- **Effort:** <small/medium/large>
```

## Parallelization Plan

After listing all opportunities, propose a wave-based execution plan for implementing them with subagents:

1. **Identify file ownership:** Group refactoring tasks by which file they modify.
2. **Wave 1 (parallel):** Tasks that only touch one file each and don't change exported interfaces. One subagent per file, all run simultaneously.
3. **Wave 2+ (sequential or narrower parallel):** Cross-file changes (import path changes, interface changes, module splits). Order by dependency — do the change that touches the most files last.
4. For each wave, state which agents can run in parallel and why they won't conflict.

## Verification

After implementing each wave:
1. Read back every modified file to verify correctness.
2. Run existing test suites that cover the modified files. If tests pass, report results. If no behavioral tests exist for the modified files, explicitly state "no behavioral tests exist for [file]" — do not claim the code is tested based on import checks alone.
3. Report a before/after table (file, line count before, line count after, what changed).

List opportunities first. Do not modify code until I approve.
