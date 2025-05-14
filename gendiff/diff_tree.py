from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class DiffNode:
    key: str
    type: str
    value: Any
    old_value: Optional[Any] = None
    new_value: Optional[Any] = None
    children: Optional[List['DiffNode']] = None


def build_diff(data1: Dict, data2: Dict) -> List[DiffNode]:
    result = []
    all_keys = sorted(set(data1.keys()) | set(data2.keys()))
    
    for key in all_keys:
        if key not in data1:
            result.append(DiffNode(key, 'added', data2[key]))
        elif key not in data2:
            result.append(DiffNode(key, 'removed', data1[key]))
        elif data1[key] == data2[key]:
            result.append(DiffNode(key, 'unchanged', data1[key]))
        elif isinstance(data1[key], dict) and isinstance(data2[key], dict):
            children = build_diff(data1[key], data2[key])
            result.append(DiffNode(key, 'nested', None, children=children))
        else:
            result.append(DiffNode(
                key, 'changed', None,
                old_value=data1[key],
                new_value=data2[key]
            ))
    
    return result 