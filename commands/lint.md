---
description: Format and lint the codebase
---

Run code quality tools on the current project.

## Detection

First detect the project type:
- If `package.json` exists → Node.js project, use ESLint + Prettier
- If `pyproject.toml` or `*.py` files exist → Python project, use black + ruff + mypy
- If both exist → run both tool sets

## Node.js Tools

1. **ESLint** — Lint JavaScript (errors, unused vars, equality)
2. **Prettier** — Auto-format code

### Node.js Commands

```bash
# Lint
npx eslint .

# Auto-fix lint
npx eslint . --fix

# Format
npx prettier --write .

# Check formatting (no changes)
npx prettier --check .
```

## Python Tools

1. **black** - Auto-format Python code (PEP 8 compliant)
2. **ruff** - Fast linter (replaces flake8/pylint)
3. **mypy** - Static type checking

## Steps

1. Check if tools are installed (`pip list | grep -E "black|ruff|mypy"`)
2. Install missing tools if needed
3. Ensure `pyproject.toml` has tool configuration
4. Run each tool and report issues
5. Optionally auto-fix (black, ruff --fix)

## Commands

```bash
# Check formatting (no changes)
black --check .

# Auto-format
black .

# Lint with ruff
ruff check .

# Auto-fix lint issues
ruff check . --fix

# Type checking
mypy . --ignore-missing-imports
```

## pyproject.toml Configuration

If not present, add this configuration:

```toml
[tool.black]
line-length = 100
target-version = ['py310']

[tool.ruff]
line-length = 100
select = ["E", "F", "W", "I", "N", "UP", "B", "C4"]
ignore = ["E501"]  # Line too long (handled by black)

[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_ignores = true
ignore_missing_imports = true
```

## Expected Issues

Common issues in RL codebases:
- Type annotations missing for numpy arrays/tensors
- Line length (configurable)
- Import ordering
- Unused variables (often intentional in RL)

## Auto-Fix Mode

When user requests auto-fix:
1. Run `black .` to format
2. Run `ruff check . --fix` to fix lint issues
3. Report remaining issues that need manual attention
