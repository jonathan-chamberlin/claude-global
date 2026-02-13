---
description: Review code structure and identify refactoring opportunities
---

Review all files in the target path to see where the code could be put closer to its ideal size and shape. Analyze the codebase for refactoring opportunities. Be specific and actionable.

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

## Domain-Specific Concerns (apply when relevant)
- RL/ML: Agent/environment coupling, replay buffer leaks, policy/value separation
- API integrations: Config hardcoding vs. injectable parameters, god modules mixing config/auth/clients/utilities

## Output Format
For each opportunity:
```
### [Priority: HIGH/MED/LOW] <Summary>
- **File:** `path/to/file:L##-L##`
- **Smell:** <which code smell>
- **Refactor:** <specific pattern to apply>
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
