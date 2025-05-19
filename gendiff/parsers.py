import json
import os
from typing import Any, Dict

import yaml


def get_file_format(file_path: str) -> str:
    _, extension = os.path.splitext(file_path)
    return extension[1:]


def read_file(file_path: str) -> str:
    try:
        with open(file_path, encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except PermissionError:
        raise PermissionError(f"Permission denied: {file_path}")


def parse_data(data: str, format: str) -> Dict[str, Any]:
    try:
        if format == 'json':
            return json.loads(data)
        if format in ('yaml', 'yml'):
            return yaml.safe_load(data)
        raise ValueError(f'Unsupported file format: {format}')
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON file: {str(e)}")
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML file: {str(e)}")


def parse_file(file_path: str) -> Dict[str, Any]:
    data = read_file(file_path)
    format = get_file_format(file_path)
    return parse_data(data, format) 