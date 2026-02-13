---
name: repo-map
description: Generate a concise codebase map showing file tree, exports, and key patterns. Use when starting work on an unfamiliar repo, when context was compacted, or when asked to "map" or "overview" the codebase.
---

Generate a repository map for the current project. This gives a quick overview without reading every file.

## Steps

1. Run `git ls-files` to get all tracked files (respects .gitignore)
2. Group files by directory into a tree structure
3. For each source file (.js, .ts, .py, .ahk):
   - Use Grep to extract export/function signatures (not implementations)
   - Note file size (line count) as a complexity indicator
4. For config files (package.json, pyproject.toml, eslint.config.js):
   - Extract key dependencies and settings
5. Present the map in the format below

## Output Format

```
## Repository Map: <repo-name>
Generated: <date>

### Structure
skills/
  notion/
    client.js (50 lines) — exports: notion, DATABASE_ID, validateEnv, logAction, parseDate
    create.js (45 lines) — exports: createTask
    ...

### Dependencies
@notionhq/client, googleapis, nodemailer, dotenv

### Key Patterns
- [2-3 patterns observed in the code]
```

## Language-Aware Extraction

- **.js/.ts**: Look for `export function`, `export const`, `export default`, `export async function`
- **.py**: Look for `def `, `class `, top-level assignments
- **.ahk**: Look for hotkey definitions (`::`, `#`), function definitions

## Notes

- Generate fresh each time — do not save to disk (avoids staleness)
- Skip binary files, images, PDFs, CSVs, lock files
- For large repos (100+ source files), summarize directories instead of listing every file
- Prioritize source code over config/metadata
