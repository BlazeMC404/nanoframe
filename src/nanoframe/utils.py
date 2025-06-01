# nanoframe/utils.py

from typing import List, Any, Union, Optional, Callable
from statistics import mean as stat_mean


def infer_dtype(values: List[Any]) -> str:
    """
    Infer the most common data type of a list of values.
    """
    non_nulls = [v for v in values if v is not None]
    if not non_nulls:
        return "unknown"

    types = set(type(v) for v in non_nulls)

    if types.issubset({int}):
        return "int"
    elif types.issubset({int, float}):
        return "float"
    elif types.issubset({str}):
        return "str"
    elif types.issubset({bool}):
        return "bool"
    else:
        return "object"


def is_numeric_dtype(dtype: str) -> bool:
    return dtype in {"int", "float"}


def cast_column(values: List[Any], target_type: Callable) -> List[Any]:
    """
    Attempt to cast a list of values to a target type.
    """
    try:
        return [target_type(v) if v is not None else None for v in values]
    except Exception:
        raise ValueError(f"Failed to cast values to {target_type}")


def align_columns(dicts: List[dict]) -> dict:
    """
    Convert list of dicts (rows) into column-aligned dictionary of lists.
    Missing keys are filled with None.
    """
    if not dicts:
        return {}

    all_keys = set()
    for row in dicts:
        all_keys.update(row.keys())

    aligned = {key: [] for key in all_keys}
    for row in dicts:
        for key in all_keys:
            aligned[key].append(row.get(key, None))

    return aligned


def format_table(columns: dict, max_rows: int = 10, padding: int = 2) -> str:
    """
    Format a small table (dict of columns) as a string.
    """
    headers = list(columns.keys())
    col_widths = {col: max(len(col), max((len(str(v)) for v in columns[col][:max_rows]), default=0))
                  for col in headers}
    col_widths = {col: w + padding for col, w in col_widths.items()}

    def fmt_row(row):
        return "".join(str(row[col]).ljust(col_widths[col]) for col in headers)

    lines = []

    # Header
    lines.append("".join(col.ljust(col_widths[col]) for col in headers))
    lines.append("-" * sum(col_widths.values()))

    # Rows
    row_count = len(next(iter(columns.values())))
    for i in range(min(row_count, max_rows)):
        row = {col: columns[col][i] for col in headers}
        lines.append(fmt_row(row))

    if row_count > max_rows:
        lines.append(f"... ({row_count - max_rows} more rows)")

    return "\n".join(lines)


def is_null(value: Any) -> bool:
    return value is None


def not_null(value: Any) -> bool:
    return value is not None


def safe_mean(values: List[Any]) -> Optional[float]:
    """
    Compute mean ignoring None/nulls.
    """
    numeric = [v for v in values if isinstance(v, (int, float)) and v is not None]
    return stat_mean(numeric) if numeric else None


def safe_min(values: List[Any]) -> Optional[Any]:
    try:
        return min(v for v in values if v is not None)
    except ValueError:
        return None


def safe_max(values: List[Any]) -> Optional[Any]:
    try:
        return max(v for v in values if v is not None)
    except ValueError:
        return None