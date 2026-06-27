# deadfinder

A CLI tool to find dead code in Python, JavaScript, and TypeScript projects.

Detects:
- Unused functions
- Unused classes
- Unused imports
- Unused variables

## Installation

```bash
pip install deadfinder
```

Or from source:

```bash
git clone https://github.com/yourusername/deadfinder
cd deadfinder
pip install -e .
```

## Usage

```bash
# Scan a directory
deadfinder ./src

# Scan multiple paths
deadfinder ./src ./lib

# JSON output (great for CI)
deadfinder ./src --format json

# Only check imports and functions
deadfinder ./src --only imports functions

# Exclude extra directories
deadfinder ./src --exclude node_modules dist coverage

# No color (for pipes/logs)
deadfinder ./src --no-color
```

## Example output

```
deadfinder — scanned 12 file(s)

  Unused Functions (2)
    deadFunction   src/utils.js:14
    legacyHelper   src/helpers.py:32

  Unused Imports (3)
    json           src/config.py:2
    join           src/routes.js:1
    lodash         src/index.ts:3

  5 dead code item(s) found.
```

## Exit codes

- `0` — no dead code found
- `1` — dead code detected (useful for CI gates)

## Supported languages

| Language   | Extensions          |
|------------|---------------------|
| Python     | `.py`               |
| JavaScript | `.js`, `.jsx`       |
| TypeScript | `.ts`, `.tsx`       |

## How it works

deadfinder uses [tree-sitter](https://tree-sitter.github.io/) to parse source files into ASTs, collects all symbol definitions (functions, classes, imports, variables), collects all identifier usages across the entire project, and reports anything defined but never referenced.

> Note: deadfinder uses cross-file usage analysis — a symbol used in any file won't be flagged. It does not currently handle dynamic references (e.g. `getattr`, `eval`, string-based lookups).

## License

MIT
