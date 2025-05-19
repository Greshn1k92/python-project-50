SEPARATOR = "    "
ADD = '+ '
DEL = '- '
NONE = '  '


def format_value(value, spaces_count=4):
    if value is None:
        return "null"
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, dict):
        indent = SEPARATOR * (spaces_count + 4)
        result_lines = []
        for key, inner_value in value.items():
            formatted_value = format_value(inner_value, spaces_count + 4)
            result_lines.append(f"{indent}{NONE}{key}: {formatted_value}")
        formatted_string = '\n'.join(result_lines)
        end_indent = SEPARATOR * (spaces_count + 2)
        return f"{{\n{formatted_string}\n{end_indent}}}"
    if isinstance(value, str):
        return value
    return str(value)


def format_diff(diff, depth=0):
    indent = '    ' * depth
    result = []
    
    for item in diff:
        key = item['key']
        status = item['status']
        
        if status == 'nested':
            result.append(f"{indent}    {key}: {{")
            result.append(format_diff(item['children'], depth + 1))
            result.append(f"{indent}    }}")
        elif status == 'added':
            result.append(f"{indent}  + {key}: {format_value(item['value'])}")
        elif status == 'removed':
            result.append(f"{indent}  - {key}: {format_value(item['value'])}")
        elif status == 'changed':
            result.append(
                f"{indent}  - {key}: {format_value(item['old_value'])}"
            )
            result.append(
                f"{indent}  + {key}: {format_value(item['new_value'])}"
            )
        elif status == 'unchanged':
            result.append(f"{indent}    {key}: {format_value(item['value'])}")
    
    return '\n'.join(result)


def format(diff):
    return '{\n' + format_diff(diff) + '\n}'


def make_stylish_diff(diff, spaces_count=4):
    indent = SEPARATOR * spaces_count
    lines = []
    for item in diff:
        key = item['name']
        action = item['action']
        
        if action == "unchanged":
            value = format_value(item['value'], spaces_count)
            lines.append(f"{indent}{NONE}{key}: {value}")
        elif action == "modified":
            old_value = format_value(item['old_value'], spaces_count)
            new_value = format_value(item['new_value'], spaces_count)
            lines.append(f"{indent}{DEL}{key}: {old_value}")
            lines.append(f"{indent}{ADD}{key}: {new_value}")
        elif action == "deleted":
            old_value = format_value(item['value'], spaces_count)
            lines.append(f"{indent}{DEL}{key}: {old_value}")
        elif action == "added":
            new_value = format_value(item['value'], spaces_count)
            lines.append(f"{indent}{ADD}{key}: {new_value}")
        elif action == 'nested':
            lines.append(f"{indent}{NONE}{key}: {{")
            children = make_stylish_diff(item['children'], spaces_count + 4)
            lines.append(children)
            lines.append(f"{indent}{NONE}}}")
    
    formatted_string = '\n'.join(lines)
    return formatted_string


def format_diff_stylish(data):
    return '{\n' + make_stylish_diff(data) + '\n}'