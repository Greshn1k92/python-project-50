SEPARATOR = " "
ADD = '+ '
DEL = '- '
NONE = '  '

def format_value(value, spaces_count=2):
    if isinstance(value, bool):
        return str(value).lower()
    if value is None:
        return "null"
    if isinstance(value, dict):
        indent = SEPARATOR * (spaces_count + 4)
        result_lines = []
        for key, inner_value in value.items():
            formatted_value = format_value(inner_value, spaces_count + 4)
            result_lines.append(f"{indent}{NONE}{key}: {formatted_value}")
        formatted_string = '\n'.join(result_lines)
        end_indent = SEPARATOR * (spaces_count + 2)
        return f"{{\n{formatted_string}\n{end_indent}}}"
    return str(value)

def make_stylish_diff(diff, spaces_count=2):
    indent = SEPARATOR * spaces_count
    lines = []
    for item in diff:
        key = item['name']
        action = item['action']
        value = item.get('value')
        old_value = item.get('old_value')
        new_value = item.get('new_value')

        if action == "unchanged":
            lines.append(f"{indent}{NONE}{key}: {format_value(value, spaces_count)}")
        elif action == "modified":
            lines.append(f"{indent}{DEL}{key}: {format_value(old_value, spaces_count)}")
            lines.append(f"{indent}{ADD}{key}: {format_value(new_value, spaces_count)}")
        elif action == "deleted":
            lines.append(f"{indent}{DEL}{key}: {format_value(old_value, spaces_count)}")
        elif action == "added":
            lines.append(f"{indent}{ADD}{key}: {format_value(new_value, spaces_count)}")
        elif action == 'nested':
            children = make_stylish_diff(item.get("children"), spaces_count + 4)
            lines.append(f"{indent}{NONE}{key}: {children}")
    
    formatted_string = '\n'.join(lines)
    end_indent = SEPARATOR * (spaces_count - 2)
    return f"{{\n{formatted_string}\n{end_indent}}}" if lines else "{}"

def format_diff(diff):
    return make_stylish_diff(diff)