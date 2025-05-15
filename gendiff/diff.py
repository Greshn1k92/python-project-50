from typing import Any, Dict

from gendiff.diff_tree import build_diff
from gendiff.formatters import FORMATTERS


def generate_diff(
    data1: Dict[str, Any],
    data2: Dict[str, Any],
    format_name: str = 'stylish'
) -> str:
    diff = build_diff(data1, data2)
    
    if format_name not in FORMATTERS:
        raise ValueError(f"Unknown format: {format_name}")
    
    return FORMATTERS[format_name](diff)