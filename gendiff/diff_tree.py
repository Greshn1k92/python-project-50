from typing import Any, Dict, List


def build_diff(data1: Dict, data2: Dict) -> List[Dict]:
    result = []
    all_keys = sorted(set(data1.keys()) | set(data2.keys()))
    
    for key in all_keys:
        if key not in data1:
            result.append({
                'name': key,
                'action': 'added',
                'value': data2[key]
            })
        elif key not in data2:
            result.append({
                'name': key,
                'action': 'deleted',
                'value': data1[key]
            })
        elif data1[key] == data2[key]:
            result.append({
                'name': key,
                'action': 'unchanged',
                'value': data1[key]
            })
        elif isinstance(data1[key], dict) and isinstance(data2[key], dict):
            children = build_diff(data1[key], data2[key])
            result.append({
                'name': key,
                'action': 'nested',
                'children': children
            })
        else:
            result.append({
                'name': key,
                'action': 'modified',
                'old_value': data1[key],
                'new_value': data2[key]
            })
    
    return result 