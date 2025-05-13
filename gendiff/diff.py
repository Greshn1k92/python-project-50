from typing import Any, Dict
from gendiff.diff_tree import build_diff
from gendiff.formatters import FORMATTERS

def generate_diff(data1: Dict, data2: Dict, format_name: str = 'stylish') -> str:
    diff = build_diff(data1, data2)
    formatter = FORMATTERS.get(format_name)
    if not formatter:
        raise ValueError(f"Unknown format: {format_name}")
    return formatter(diff) 