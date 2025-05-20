REPLACER = ' '
SPACE_COUNT = 4


def format_value(node, depth: int) -> str:
    """Format a value for stylish output based on the user's working example."""
    big_indent = REPLACER * SPACE_COUNT * (depth + 1)
    indent = REPLACER * SPACE_COUNT * depth
    
    if not isinstance(node, dict):
        if isinstance(node, bool):
            return 'true' if node else 'false'
        elif node is None:
            return 'null'
        else:
            return str(node)
    
    if not node: # Handle empty dicts that might be passed
        return "{}"

    result = []
    for key, value in sorted(node.items()): # Sort for consistent order
        result.append(f'{big_indent}{key}: {format_value(value, depth + 1)}')
    
    return '{\n' + '\n'.join(result) + '\n' + indent + '}'


def make_stylish_diff(diff_dict: dict, depth=0):
    """Generate a stylish representation of the diff, based on the user's working example."""
    big_indent = REPLACER * SPACE_COUNT * (depth + 1)
    sign_indent = REPLACER * (SPACE_COUNT * (depth + 1) - 2)
    diff_block_closing_brace_indent = REPLACER * SPACE_COUNT * depth 
    
    result = []
    for key in sorted(diff_dict.keys()):
        item = diff_dict[key]
        action = item['status']
        
        if action == "unchanged":
            result.append(f'{big_indent}{key}: {format_value(item["value"], depth + 1)}')
        elif action == "changed":
            result.append(f'{sign_indent}- {key}: {format_value(item["old_value"], depth + 1)}')
            result.append(f'{sign_indent}+ {key}: {format_value(item["new_value"], depth + 1)}')
        elif action == "removed":
            result.append(f'{sign_indent}- {key}: {format_value(item["value"], depth + 1)}')
        elif action == "added":
            result.append(f'{sign_indent}+ {key}: {format_value(item["value"], depth + 1)}')
        elif action == 'nested':
            result.append(f'{big_indent}{key}: {make_stylish_diff(item["children"], depth + 1)}')
    
    return '{\n' + '\n'.join(result) + '\n' + diff_block_closing_brace_indent + '}'


def format_diff_stylish(data):
    """Main function to format diff in stylish format."""
    return make_stylish_diff(data, 0)


# Keep original (potentially unused by stylish tests) functions format_diff and format
# These were part of the original file structure but their logic might differ.
def format_diff(diff_list, depth=0): # Assuming diff_list is a list of dicts
    old_school_indent = REPLACER * SPACE_COUNT * depth 
    old_school_result = []
    for item_dict in diff_list: 
        key = item_dict.get('key', item_dict.get('name')) 
        status = item_dict.get('status', item_dict.get('action'))
        
        if status == 'nested':
            old_school_result.append(f"{old_school_indent}{REPLACER*SPACE_COUNT}{key}: {{")
            old_school_result.append(format_diff(item_dict.get('children', []), depth + 1))
            old_school_result.append(f"{old_school_indent}{REPLACER*SPACE_COUNT}}}")
        elif status == 'added':
            old_school_result.append(f"{old_school_indent}{REPLACER*(SPACE_COUNT-2)}+ {key}: {format_value(item_dict['value'], depth +1)}") 
        elif status == 'removed':
            old_school_result.append(f"{old_school_indent}{REPLACER*(SPACE_COUNT-2)}- {key}: {format_value(item_dict['value'], depth +1)}")
        elif status == 'changed':
            old_school_result.append(
                f"{old_school_indent}{REPLACER*(SPACE_COUNT-2)}- {key}: {format_value(item_dict['old_value'], depth +1)}"
            )
            old_school_result.append(
                f"{old_school_indent}{REPLACER*(SPACE_COUNT-2)}+ {key}: {format_value(item_dict['new_value'], depth +1)}"
            )
        elif status == 'unchanged':
            old_school_result.append(f"{old_school_indent}{REPLACER*SPACE_COUNT}{key}: {format_value(item_dict['value'], depth +1)}")
    return '\n'.join(old_school_result)

def format(diff_list):
    return '{\n' + format_diff(diff_list) + '\n}'