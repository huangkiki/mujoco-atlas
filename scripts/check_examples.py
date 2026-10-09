"""Check syntax only: never import or execute tutorial code or compile MJCF."""

import ast
from pathlib import Path
import re
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    python_files = sorted((ROOT / "examples").rglob("*.py"))
    xml_files = sorted((ROOT / "examples").rglob("*.xml"))
    snippets = 0
    for path in python_files:
        ast.parse(path.read_text(), filename=str(path.relative_to(ROOT)))
    for path in sorted((ROOT / "docs").rglob("*.md")):
        for number, code in enumerate(
            re.findall(r"^```python\n(.*?)^```", path.read_text(), re.M | re.S), 1
        ):
            ast.parse(code, filename=f"{path.relative_to(ROOT)}:python-block-{number}")
            snippets += 1
    for path in xml_files:
        ET.parse(path)
    print(
        f"Syntax passed: {len(python_files)} Python files, "
        f"{snippets} Python snippets, {len(xml_files)} XML files. "
        "No imports, native execution or MJCF schema validation performed."
    )


if __name__ == "__main__":
    main()
