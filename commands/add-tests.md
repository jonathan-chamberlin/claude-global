---
description: Generate behavior tests for project components
---

Generate tests for the target path. Prefer real behavior tests over mocked unit tests — call actual APIs and verify real outputs unless the user explicitly requests mocks.

## Step 1: Detect Language and Framework

Before writing any tests, detect the project's language and test tooling:
- **Node.js/JS/TS:** Check for `package.json` (`"type": "module"`), Node version (≥18 has `node:test` built-in). Prefer `node:test` + `node:assert` to avoid adding dependencies. Use ES module imports.
- **Python:** Check for `pyproject.toml`, `pytest`. Use pytest with fixtures in `conftest.py`.
- **Other:** Detect from file extensions and existing test patterns.

Also check for `.env` files and credential setup — tests that hit real APIs need env vars loaded (e.g., `import 'dotenv/config'` for Node, `python-dotenv` for Python).

## Step 2: Identify Test Targets

Analyze the project structure and categorize each module:

1. **Pure functions** — Test with direct calls, specific inputs, exact expected outputs. Cover edge cases and boundary conditions.
2. **Configuration/data** — Validate structure, types, internal consistency (e.g., every key in map A also exists in map B).
3. **API clients** — Make real API calls. Verify response shapes, not specific values (data changes daily). Use generous timeouts (30s+).
4. **Pipelines/orchestrators** — End-to-end integration tests with real dependencies. Verify invariants (sorted output, threshold filtering) not specific results.
5. **Stateful modules** — Test the lifecycle (write, read back, verify persistence). Clean up state in before/after hooks.

## Step 3: Write Tests in Parallel

When testing multiple independent modules, use one subagent per module to write tests in parallel. Each agent gets:
- The source file to read
- The test style and framework to use
- Specific behaviors to test
- Timeout guidance for API calls

## Step 4: Run All Tests

Run every test file and report results. If any fail, fix them before reporting.

## Step 5: Coverage Report

After all tests pass, provide an honest summary of what was and wasn't tested:

```
| File | Tests | What's covered | What's NOT covered |
|------|-------|----------------|--------------------|
```

Explicitly call out:
- Functions that were tested via real calls vs. only import-checked
- Error paths that were exercised vs. skipped
- Internal helpers that couldn't be tested directly (not exported)
- Any API endpoints that require auth credentials not available

Do NOT present shallow import checks as "tests passing" — distinguish wiring tests from behavior tests.
