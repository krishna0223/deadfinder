import argparse
import sys
from .analyzer import analyze
from .reporter import report_text, report_json


def main():
    parser = argparse.ArgumentParser(
        prog="deadfinder",
        description="Find dead code in Python, JavaScript, and TypeScript projects.",
    )
    parser.add_argument(
        "paths",
        nargs="+",
        help="Files or directories to scan",
    )
    parser.add_argument(
        "--exclude",
        nargs="*",
        default=["node_modules", ".venv", "venv", "__pycache__", "dist", "build", ".git"],
        metavar="DIR",
        help="Directory names to exclude (default: node_modules, .venv, dist, build)",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output",
    )
    parser.add_argument(
        "--only",
        nargs="*",
        choices=["functions", "classes", "imports", "variables"],
        help="Only report specific categories",
    )

    args = parser.parse_args()
    results = analyze(args.paths, exclude=args.exclude)

    if args.only:
        for key in list(results["dead"].keys()):
            if key not in args.only:
                results["dead"][key] = []

    if args.format == "json":
        print(report_json(results))
    else:
        report_text(results, no_color=args.no_color)

    total_dead = sum(len(v) for v in results["dead"].values())
    sys.exit(1 if total_dead > 0 else 0)


if __name__ == "__main__":
    main()
