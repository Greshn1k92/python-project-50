from gendiff.diff_tree import build_diff
from gendiff.formatters import FORMATTERS
from gendiff.parsers import parse_file


def generate_diff(
    file_path1: str,
    file_path2: str,
    format_name: str = 'stylish'
) -> str:
    data1 = parse_file(file_path1)
    data2 = parse_file(file_path2)
    diff = build_diff(data1, data2)
    
    if format_name not in FORMATTERS:
        raise ValueError(f"Unknown format: {format_name}")
    
    return FORMATTERS[format_name](diff)