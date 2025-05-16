import json
from typing import Any, Dict

import yaml


def parse_file(file_path: str) -> Dict[str, Any]:
    with open(file_path) as f:
        if file_path.endswith('.json'):
            return json.load(f)
        elif file_path.endswith(('.yml', '.yaml')):
            return yaml.safe_load(f)
        else:
            raise ValueError(f"Unsupported file format: {file_path}") 