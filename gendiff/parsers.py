import json
from typing import Any, Dict

import yaml


def parse_file(file_path: str) -> Dict[str, Any]:
    try:
        with open(file_path) as f:
            if file_path.endswith('.json'):
                try:
                    return json.load(f)
                except json.JSONDecodeError as e:
                    raise ValueError(f"Invalid JSON file {file_path}: {str(e)}")
            elif file_path.endswith(('.yml', '.yaml')):
                try:
                    return yaml.safe_load(f)
                except yaml.YAMLError as e:
                    raise ValueError(f"Invalid YAML file {file_path}: {str(e)}")
            else:
                raise ValueError(f"Unsupported file format: {file_path}")
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except PermissionError:
        raise PermissionError(f"Permission denied: {file_path}") 