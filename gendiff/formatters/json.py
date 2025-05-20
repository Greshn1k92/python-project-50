import json


def _transform_to_list(diff_node):
    """Recursively transforms the diff dictionary node into a list format
    matching the expected JSON structure (using 'name' and correct 'action'
    values)."""
    output_list = []
    for key in sorted(diff_node.keys()):
        item = diff_node[key]
        status = item['status']
        
        # Map internal status to the expected 'action' string for JSON output
        if status == 'removed':
            action = 'deleted'
        elif status == 'changed':
            action = 'modified'
        else:
            action = status  # For 'added', 'unchanged', 'nested'

        entry = {
            'action': action,
            'name': key,
        }

        if status == 'added':
            entry['new_value'] = item['value']
        elif status == 'removed':  # internal status is 'removed'
            entry['old_value'] = item['value']
        elif status == 'unchanged':
            entry['value'] = item['value']
        elif status == 'changed':  # internal status is 'changed'
            # Match order from expected_result_json_format.txt: new_value then
            # old_value
            entry['new_value'] = item['new_value']
            entry['old_value'] = item['old_value']
        elif status == 'nested':
            entry['children'] = _transform_to_list(item['children'])
        
        output_list.append(entry)
    return output_list


def format_diff_json(diff_dict):
    """Formats the diff dictionary into a JSON string representing a list of
    changes."""
    if not isinstance(diff_dict, dict):
        return json.dumps([])
        
    list_representation = _transform_to_list(diff_dict)
    # Add sort_keys=False to prevent reordering of keys within dictionaries
    return json.dumps(list_representation, indent=4, sort_keys=False) 