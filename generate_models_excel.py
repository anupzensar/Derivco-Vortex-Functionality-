"""Generate an Excel workbook summarizing Pydantic model fields.

Specification (updated):
    - Only include columns: Class | Field Name | Type
    - Strip Optional/Union None wrappers from the displayed type (e.g. Optional[str] -> str, str | None -> str)
    - One worksheet per source file containing its Pydantic models.

Run: python generate_models_excel.py
Creates: models_summary.xlsx in project root.
"""
from __future__ import annotations
import ast
from pathlib import Path
from typing import List, Optional
from openpyxl import Workbook

PROJECT_ROOT = Path(__file__).parent
MODELS_DIR = PROJECT_ROOT / "models"
OUTPUT_FILE = PROJECT_ROOT / "models_summary.xlsx"

class ModelField:
    def __init__(self, name: str, type_repr: str, alias: Optional[str], required: bool):
        self.name = name
        self.type_repr = type_repr
        self.alias = alias
        self.required = required  # retained for possible future use, not exported

class ParsedModel:
    def __init__(self, file: Path, class_name: str):
        self.file = file
        self.class_name = class_name
        self.fields: List[ModelField] = []

    def add_field(self, field: ModelField):
        self.fields.append(field)


def is_base_model_in_bases(class_def: ast.ClassDef) -> bool:
    for base in class_def.bases:
        # match BaseModel or pydantic.BaseModel style
        if isinstance(base, ast.Name) and base.id == "BaseModel":
            return True
        if isinstance(base, ast.Attribute) and base.attr == "BaseModel":
            return True
    return False


def annotation_to_str(annotation: Optional[ast.AST]) -> str:
    if annotation is None:
        return "<none>"
    try:
        return ast.unparse(annotation)
    except Exception:
        # Fallback manual reconstruction
        if isinstance(annotation, ast.Name):
            return annotation.id
        return annotation.__class__.__name__


def normalize_type(type_str: str) -> str:
    """Remove Optional/None wrappers from a type representation.

    Examples:
      Optional[str] -> str
      Union[int, None] -> int
      str | None -> str
      Optional[List[str]] -> List[str]
    """
    if type_str == "<none>":
        return type_str
    # Remove whitespace for easier pattern matching then restore format
    raw = type_str
    # Handle typing.Optional[...] pattern
    if raw.startswith("Optional[") and raw.endswith("]"):
        inner = raw[len("Optional["):-1]
        return inner
    # Handle Union[..., None]
    if raw.startswith("Union[") and raw.endswith("]"):
        inner = raw[len("Union["):-1]
        parts = [p.strip() for p in inner.split(",")]
        non_none = [p for p in parts if p not in ("None", "NoneType")]
        if len(non_none) == 1:
            return non_none[0]
        return ", ".join(non_none)
    # Handle PEP604 union syntax T | None or None | T
    if "|" in raw:
        parts = [p.strip() for p in raw.split("|")]
        non_none = [p for p in parts if p not in ("None", "NoneType")]
        if len(non_none) == 1:
            return non_none[0]
        return " | ".join(non_none)
    return raw


def extract_alias(value: ast.AST) -> Optional[str]:
    # Look for Field(..., alias="...")
    if isinstance(value, ast.Call):
        func_name = None
        if isinstance(value.func, ast.Name):
            func_name = value.func.id
        elif isinstance(value.func, ast.Attribute):
            func_name = value.func.attr
        if func_name == "Field":
            for kw in value.keywords:
                if kw.arg == "alias":
                    if isinstance(kw.value, ast.Constant) and isinstance(kw.value.value, str):
                        return kw.value.value
    return None


def is_required(annotation_str: str, default_value: Optional[ast.AST]) -> bool:
    # Simple heuristic: Optional[...] or Union[..., None] => not required; default None => not required
    lower = annotation_str.lower()
    if "optional" in lower:
        return False
    if "none" in lower and ("union" in lower or "|" in annotation_str):
        return False
    if isinstance(default_value, ast.Constant) and default_value.value is None:
        return False
    # Field(None, ...) default call where first arg is None
    if isinstance(default_value, ast.Call) and default_value.args:
        first = default_value.args[0]
        if isinstance(first, ast.Constant) and first.value is None:
            return False
    return True


def parse_models_in_file(path: Path) -> List[ParsedModel]:
    models: List[ParsedModel] = []
    source = path.read_text(encoding="utf-8")
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        print(f"Skipping {path.name}: syntax error {e}")
        return models

    for node in tree.body:
        if isinstance(node, ast.ClassDef) and is_base_model_in_bases(node):
            parsed = ParsedModel(path, node.name)
            # Walk assignments inside class body
            for stmt in node.body:
                if isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name):
                    field_name = stmt.target.id
                    type_repr = annotation_to_str(stmt.annotation)
                    default_value = stmt.value
                    alias = extract_alias(default_value) if default_value else None
                    required = is_required(type_repr, default_value)
                    parsed.add_field(ModelField(field_name, normalize_type(type_repr), alias, required))
                elif isinstance(stmt, ast.Assign) and len(stmt.targets) == 1 and isinstance(stmt.targets[0], ast.Name):
                    # Non-annotated assignment - treat type as '<inferred>'
                    field_name = stmt.targets[0].id
                    alias = extract_alias(stmt.value)
                    parsed.add_field(ModelField(field_name, normalize_type('<inferred>'), alias, False))
            models.append(parsed)
    return models


def collect_all_models() -> List[ParsedModel]:
    all_models: List[ParsedModel] = []
    for py_file in MODELS_DIR.glob("*.py"):
        if py_file.name.startswith("__"):
            continue
        all_models.extend(parse_models_in_file(py_file))
    return all_models


def write_excel(models: List[ParsedModel]):
    wb = Workbook()
    # Remove default sheet
    default = wb.active
    wb.remove(default)

    # Group by file
    by_file = {}
    for m in models:
        by_file.setdefault(m.file.name, []).append(m)

    for file_name, class_list in sorted(by_file.items()):
        ws = wb.create_sheet(title=file_name[:31])  # Excel sheet name limit
        ws.append(["Class", "Field Name", "Type"])
        for parsed in class_list:
            for field in parsed.fields:
                ws.append([
                    parsed.class_name,
                    field.name,
                    field.type_repr,
                ])
        # Auto width (simple heuristic)
        for col in ws.columns:
            max_len = 0
            col_letter = col[0].column_letter
            for cell in col:
                if cell.value is None:
                    continue
                max_len = max(max_len, len(str(cell.value)))
            ws.column_dimensions[col_letter].width = min(max_len + 2, 50)

    wb.save(OUTPUT_FILE)
    print(f"Model summary written to {OUTPUT_FILE}")


def main():
    models = collect_all_models()
    if not models:
        print("No Pydantic models found.")
        return
    write_excel(models)

if __name__ == "__main__":
    main()
