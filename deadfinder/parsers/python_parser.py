from tree_sitter import Language, Parser
import tree_sitter_python as tspython
from pathlib import Path


PY_LANGUAGE = Language(tspython.language())


def parse_python(file_path: str) -> dict:
    parser = Parser(PY_LANGUAGE)
    source = Path(file_path).read_bytes()
    tree = parser.parse(source)
    root = tree.root_node

    definitions = {"functions": [], "classes": [], "imports": [], "variables": []}
    usages = set()

    # Track byte offsets of name nodes that are definition sites, not usages
    definition_offsets = set()

    def walk(node, scope=None):
        t = node.type

        if t == "function_definition":
            name_node = node.child_by_field_name("name")
            if name_node:
                definition_offsets.add(name_node.start_byte)
                definitions["functions"].append({
                    "name": name_node.text.decode(),
                    "line": name_node.start_point[0] + 1,
                    "file": file_path,
                })

        elif t == "class_definition":
            name_node = node.child_by_field_name("name")
            if name_node:
                definition_offsets.add(name_node.start_byte)
                definitions["classes"].append({
                    "name": name_node.text.decode(),
                    "line": name_node.start_point[0] + 1,
                    "file": file_path,
                })

        elif t == "import_statement":
            for child in node.children:
                if child.type in ("dotted_name", "identifier"):
                    definition_offsets.add(child.start_byte)
                    definitions["imports"].append({
                        "name": child.text.decode().split(".")[-1],
                        "line": child.start_point[0] + 1,
                        "file": file_path,
                    })

        elif t == "import_from_statement":
            for child in node.children:
                if child.type == "aliased_import":
                    alias = child.child_by_field_name("alias")
                    if alias:
                        definition_offsets.add(alias.start_byte)
                        definitions["imports"].append({
                            "name": alias.text.decode(),
                            "line": alias.start_point[0] + 1,
                            "file": file_path,
                        })
                elif child.type == "identifier" and child.prev_sibling and child.prev_sibling.type in ("import", ","):
                    definition_offsets.add(child.start_byte)
                    definitions["imports"].append({
                        "name": child.text.decode(),
                        "line": child.start_point[0] + 1,
                        "file": file_path,
                    })

        elif t == "assignment":
            left = node.child_by_field_name("left")
            if left and left.type == "identifier":
                definition_offsets.add(left.start_byte)
                definitions["variables"].append({
                    "name": left.text.decode(),
                    "line": left.start_point[0] + 1,
                    "file": file_path,
                })

        elif t == "identifier":
            if node.start_byte not in definition_offsets:
                usages.add(node.text.decode())

        for child in node.children:
            walk(child, scope)

    walk(root)
    return {"definitions": definitions, "usages": usages}
