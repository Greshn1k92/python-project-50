SEPARATOR = " "
ADD = '+ '
DEL = '- '
NONE = '  '


def format_value(value, spaces_count=4):
    if isinstance(value, dict):
        indent = spaces_count + 4
        end_indent = spaces_count
        lines = []
        for key, val in value.items():
            lines.append(f"{' ' * indent}{key}: {format_value(val, indent)}")
        return "{\n" + "\n".join(lines) + f"\n{' ' * end_indent}}}"
    elif value is None:
        return "null"
    elif isinstance(value, bool):
        return str(value).lower()
    elif value == "":
        return ""
    return str(value)


def make_stylish_diff(diff, spaces_count=4):
    if not diff:
        return "{}"
    lines = []
    indent = spaces_count
    for item in diff:
        key = item['name']
        action = item['action']
        if action == 'nested':
            children = make_stylish_diff(item['children'], spaces_count + 4)
            lines.append(f"{' ' * indent}{key}: {children}")
        elif action == 'added':
            value = format_value(item['value'], spaces_count)
            lines.append(f"{' ' * indent}+ {key}: {value}")
        elif action == 'deleted':
            value = format_value(item['value'], spaces_count)
            lines.append(f"{' ' * indent}- {key}: {value}")
        elif action == 'unchanged':
            value = format_value(item['value'], spaces_count)
            lines.append(f"{' ' * indent}  {key}: {value}")
        elif action == 'modified':
            old_value = format_value(item['old_value'], spaces_count)
            new_value = format_value(item['new_value'], spaces_count)
            lines.append(f"{' ' * indent}- {key}: {old_value}")
            lines.append(f"{' ' * indent}+ {key}: {new_value}")
    return "{\n" + "\n".join(lines) + f"\n{' ' * (spaces_count - 4)}}}"


def format_diff_stylish(data):
    return make_stylish_diff(data)