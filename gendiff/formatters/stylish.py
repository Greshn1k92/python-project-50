SEPARATOR = " "
ADD = '+ '
DEL = '- '
NONE = '  '

def format_value(value, depth):
    if value is None:
        return "null"
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, dict):
        indent = SEPARATOR * ((depth + 1) * 4)
        lines = []
        for k, v in value.items():
            lines.append(f"{indent}{k}: {format_value(v, depth + 1)}")
        closing_indent = SEPARATOR * (depth * 4)
        return "{\n" + "\n".join(lines) + f"\n{closing_indent}" + "}"
    return str(value)

def make_stylish_diff(diff, depth=0):
    if not diff:
        return '{}'
    indent = SEPARATOR * (depth * 4 + 4)
    sign_indent = SEPARATOR * (depth * 4 + 4)
    lines = []
    for node in diff:
        key = node.key
        type_ = node.type
        value = node.value
        if type_ == "nested":
            children = make_stylish_diff(node.children, depth + 1)
            lines.append(f"{indent}{NONE}{key}: {children}")
        elif type_ == "unchanged":
            lines.append(f"{indent}{NONE}{key}: {format_value(value, depth)}")
        elif type_ == "changed":
            old_value = format_value(node.old_value, depth)
            new_value = format_value(node.new_value, depth)
            lines.append(f"{sign_indent}{DEL}{key}: {old_value}")
            lines.append(f"{sign_indent}{ADD}{key}: {new_value}")
        elif type_ == "removed":
            lines.append(f"{sign_indent}{DEL}{key}: {format_value(value, depth)}")
        elif type_ == "added":
            lines.append(f"{sign_indent}{ADD}{key}: {format_value(value, depth)}")
    closing_indent = SEPARATOR * (depth * 4)
    return "{\n" + "\n".join(lines) + f"\n{closing_indent}" + "}"

def format_diff(diff):
    return make_stylish_diff(diff)