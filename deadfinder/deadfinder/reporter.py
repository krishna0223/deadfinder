import json
from pathlib import Path


CATEGORY_LABELS = {
    "functions": "Unused Functions",
    "classes": "Unused Classes",
    "imports": "Unused Imports",
    "variables": "Unused Variables",
}

COLORS = {
    "red": "\033[91m",
    "yellow": "\033[93m",
    "cyan": "\033[96m",
    "green": "\033[92m",
    "bold": "\033[1m",
    "reset": "\033[0m",
}


def report_text(results: dict, no_color: bool = False):
    dead = results["dead"]
    total_files = results["total_files"]
    total_dead = sum(len(v) for v in dead.values())

    def c(text, color):
        if no_color:
            return text
        return f"{COLORS[color]}{text}{COLORS['reset']}"

    print(f"\n{c('deadfinder', 'bold')} — scanned {total_files} file(s)\n")

    if total_dead == 0:
        print(c("  No dead code found.", "green"))
        return

    for category, items in dead.items():
        if not items:
            continue
        print(c(f"  {CATEGORY_LABELS[category]} ({len(items)})", "bold"))
        for item in items:
            rel = _rel(item["file"])
            print(f"    {c(item['name'], 'red')}  {c(rel, 'cyan')}:{c(str(item['line']), 'yellow')}")
        print()

    print(c(f"  {total_dead} dead code item(s) found.", "bold"))


def report_json(results: dict) -> str:
    output = {
        "total_files_scanned": results["total_files"],
        "dead_code": {
            category: [
                {"name": i["name"], "file": _rel(i["file"]), "line": i["line"]}
                for i in items
            ]
            for category, items in results["dead"].items()
        },
        "summary": {k: len(v) for k, v in results["dead"].items()},
        "total": sum(len(v) for v in results["dead"].values()),
    }
    return json.dumps(output, indent=2)


def _rel(path: str) -> str:
    try:
        return str(Path(path).relative_to(Path.cwd()))
    except ValueError:
        return path
