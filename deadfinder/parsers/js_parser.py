from tree_sitter import Language, Parser
import tree_sitter_javascript as tsjs
import tree_sitter_typescript as tsts
from pathlib import Path


JS_LANGUAGE = Language(tsjs.language())
TS_LANGUAGE = Language(tsts.language_typescript())
TSX_LANGUAGE = Language(tsts.language_tsx())


def parse_js_ts(file_path: str) -> dict:
    ext = Path(file_path).suffix.lower()
    if ext == ".ts":
        lang = TS_LANGUAGE
    elif ext == ".tsx":
        lang = TSX_LANGUAGE
    else:
        lang = JS_LANGUAGE

    parser = Parser(lang)
    source = Path(file_path).read_bytes()
    tree = parser.parse(source)
    root = tree.root_node

    definitions = {"functions": [], "classes": [], "imports": [], "variables": []}
    usages = set()

    definition_offsets = set()

    def walk(node):
        t = node.type

        if t in ("function_declaration", "function"):
            name_node = node.child_by_field_name("name")
            if name_node:
                definition_offsets.add(name_node.start_byte)
                definitions["functions"].append({
                    "name": name_node.text.decode(),
                    "line": name_node.start_point[0] + 1,
                    "file": file_path,
                })

        elif t == "class_declaration":
            name_node = node.child_by_field_name("name")
            if name_node:
                definition_offsets.add(name_node.start_byte)
                definitions["classes"].append({
                    "name": name_node.text.decode(),
                    "line": name_node.start_point[0] + 1,
                    "file": file_path,
                })

        elif t in ("lexical_declaration", "variable_declaration"):
            for child in node.children:
                if child.type == "variable_declarator":
                    name_node = child.child_by_field_name("name")
                    value_node = child.child_by_field_name("value")
                    if name_node:
                        definition_offsets.add(name_node.start_byte)
                        if value_node and value_node.type in ("arrow_function", "function"):
                            definitions["functions"].append({
                                "name": name_node.text.decode(),
                                "line": name_node.start_point[0] + 1,
                                "file": file_path,
                            })
                        else:
                            definitions["variables"].append({
                                "name": name_node.text.decode(),
                                "line": name_node.start_point[0] + 1,
                                "file": file_path,
                            })

        elif t == "import_statement":
            for child in node.children:
                if child.type == "import_clause":
                    for ic in child.children:
                        if ic.type == "identifier":
                            definition_offsets.add(ic.start_byte)
                            definitions["imports"].append({
                                "name": ic.text.decode(),
                                "line": ic.start_point[0] + 1,
                                "file": file_path,
                            })
                        elif ic.type == "named_imports":
                            for spec in ic.children:
                                if spec.type == "import_specifier":
                                    alias = spec.child_by_field_name("alias")
                                    name = spec.child_by_field_name("name")
                                    target = alias or name
                                    if target:
                                        definition_offsets.add(target.start_byte)
                                        definitions["imports"].append({
                                            "name": target.text.decode(),
                                            "line": target.start_point[0] + 1,
                                            "file": file_path,
                                        })

        elif t == "identifier":
            if node.start_byte not in definition_offsets:
                usages.add(node.text.decode())

        for child in node.children:
            walk(child)

    walk(root)
    return {"definitions": definitions, "usages": usages}
