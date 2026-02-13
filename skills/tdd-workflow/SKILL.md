---
name: tdd-workflow
description: Test-driven development workflow. Use when the user asks to "write tests first", "TDD", or when implementing a new feature where behavior should be defined before coding.
---

Follow the red-green-refactor cycle for test-driven development.

## Workflow

1. **Understand** — Read the feature requirement or bug report
2. **Identify** — Determine which module/function will implement it
3. **Write tests FIRST** — Create test file with descriptive test names covering:
   - Happy path (expected behavior)
   - Edge cases (empty input, null, boundary values)
   - Error cases (invalid input, missing required fields)
4. **Run tests** — They should all FAIL (red phase). If any pass, the tests aren't testing new behavior.
5. **Implement** — Write the minimum code to make tests pass (green phase)
6. **Run tests again** — They should all PASS
7. **Refactor** — Clean up while keeping tests green

## Language Detection

- If `package.json` exists → use `node:test` + `node:assert/strict` (zero dependencies)
- If `pyproject.toml` or `*.py` files exist → use `pytest`

## Node.js Test Pattern (gold standard — from kalshi tests)

```javascript
import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { functionToTest } from '../module.js';

describe('functionToTest', () => {
  it('returns expected output for valid input', () => {
    const result = functionToTest('valid input');
    assert.strictEqual(result, 'expected output');
  });

  it('throws on invalid input', () => {
    assert.throws(() => functionToTest(null), /error message/);
  });
});
```

## Python Test Pattern

```python
import pytest
from module import function_to_test

def test_valid_input():
    assert function_to_test("valid") == "expected"

def test_invalid_input():
    with pytest.raises(ValueError):
        function_to_test(None)
```

## Test File Locations

- Node.js: `skills/<name>/tests/<module>.test.js`
- Python: `tests/test_<module>.py`

## Running Tests

- Node.js: `node --test <test-file>`
- Python: `pytest <test-file> -v`

## Rules

- Test ONLY pure functions and validation logic in seed tests — do not mock APIs
- Follow existing test patterns in the repo (check kalshi tests as the gold standard)
- Each test should have a descriptive name explaining the expected behavior
- Always run tests after writing them to confirm they pass
