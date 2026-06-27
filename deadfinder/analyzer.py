from pathlib import Path
from .parsers import parse_python, parse_js_ts

SUPPORTED = {
    ".py": parse_python,
    ".js": parse_js_ts,
    ".ts": parse_js_ts,
    ".tsx": parse_js_ts,
    ".jsx": parse_js_ts,
}

# Names that are almost always used implicitly — skip them
BUILTIN_SKIP = {
    "__init__", "__main__", "__all__", "__name__", "__file__",
    "__repr__", "__str__", "__len__", "__eq__", "__hash__",
    "__enter__", "__exit__", "__call__", "__new__", "__del__",
    "main", "setup", "teardown",
}


def analyze(paths: list[str], exclude: list[str] = None) -> dict:
    exclude = set(exclude or [])
    all_defs = {"functions": [], "classes": [], "imports": [], "variables": []}
    all_usages = set()

    files = _collect_files(paths, exclude)

    for f in files:
        ext = Path(f).suffix.lower()
        parser = SUPPORTED.get(ext)
        if not parser:
            continue
        try:
            result = parser(f)
            for key in all_defs:
                all_defs[key].extend(result["definitions"][key])
            all_usages.update(result["usages"])
        except Exception as e:
            print(f"[warn] could not parse {f}: {e}")

    dead = {}
    for category, items in all_defs.items():
        dead[category] = [
            item for item in items
            if item["name"] not in all_usages
            and item["name"] not in BUILTIN_SKIP
            and not item["name"].startswith("_")
        ]

    return {"dead": dead, "total_files": len(files)}


def _collect_files(paths: list[str], exclude: set) -> list[str]:
    files = []
    for p in paths:
        path = Path(p)
        if path.is_file():
            if path.suffix.lower() in SUPPORTED:
                files.append(str(path))
        elif path.is_dir():
            for f in path.rglob("*"):
                if f.suffix.lower() in SUPPORTED:
                    if not any(ex in f.parts for ex in exclude):
                        files.append(str(f))
    return files
