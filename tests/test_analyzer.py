import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deadfinder.analyzer import analyze


def test_python_dead_code():
    results = analyze(["tests/fixtures/sample.py"])
    dead = results["dead"]
    dead_names = (
        [i["name"] for i in dead["functions"]]
        + [i["name"] for i in dead["classes"]]
        + [i["name"] for i in dead["imports"]]
        + [i["name"] for i in dead["variables"]]
    )
    assert "dead_function" in dead_names, "should detect unused function"
    assert "DeadClass" in dead_names, "should detect unused class"
    assert "json" in dead_names, "should detect unused import"
    assert "used_function" not in dead_names, "should not flag used function"
    assert "UsedClass" not in dead_names, "should not flag used class"
    print("✓ Python dead code detection passed")


def test_js_dead_code():
    results = analyze(["tests/fixtures/sample.js"])
    dead = results["dead"]
    dead_names = (
        [i["name"] for i in dead["functions"]]
        + [i["name"] for i in dead["classes"]]
        + [i["name"] for i in dead["imports"]]
        + [i["name"] for i in dead["variables"]]
    )
    assert "deadFunction" in dead_names, "should detect unused JS function"
    assert "DeadClass" in dead_names, "should detect unused JS class"
    assert "usedFunction" not in dead_names, "should not flag used JS function"
    print("✓ JS dead code detection passed")


if __name__ == "__main__":
    os.chdir(os.path.join(os.path.dirname(__file__), ".."))
    test_python_dead_code()
    test_js_dead_code()
    print("\nAll tests passed.")
