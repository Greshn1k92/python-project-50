from gendiff.formatters import FORMATTERS
from gendiff.parsers import parse_file


def make_diff(file1_data, file2_data):
    diff = dict()
    keys = sorted(file1_data.keys() | file2_data.keys())

    for key in keys:
        if key not in file1_data:
            diff[key] = {
                'status': 'added',
                'value': file2_data[key]
            }
        elif key not in file2_data:
            diff[key] = {
                'status': 'removed',
                'value': file1_data[key]
            }
        else:
            value1, value2 = file1_data[key], file2_data[key]
            if isinstance(value1, dict) and isinstance(value2, dict):
                nested = make_diff(value1, value2)
                diff[key] = {
                    'status': 'nested',
                    'children': nested
                }
            elif value1 == value2:
                diff[key] = {
                    'status': 'unchanged',
                    'value': value1
                }
            else:
                diff[key] = {
                    'status': 'changed',
                    'old_value': value1,
                    'new_value': value2
                }
    return diff


def generate_diff(file_path1, file_path2, format_name='stylish') -> str:
    file1_data = parse_file(file_path1)
    file2_data = parse_file(file_path2)
    
    diff_result = make_diff(file1_data, file2_data)
    
    if format_name not in FORMATTERS:
        raise ValueError(f"Unknown format: {format_name}")
    
    formatter_func = FORMATTERS[format_name]
    return formatter_func(diff_result)