SEPARATOR = " "
ADD = '+ '
DEL = '- '
NONE = '  '


def format_value(value, spaces_count):
    if isinstance(value, dict):
        indent = SEPARATOR * (spaces_count + 4)
        closing_indent = SEPARATOR * spaces_count
        lines = []
        for key, val in value.items():
            lines.append(
                f"{indent}{key}: {format_value(val, spaces_count + 4)}"
            )
        return "{\n" + "\n".join(lines) + f"\n{closing_indent}" + "}"
    elif value is None:
        return "null"
    elif isinstance(value, bool):
        return str(value).lower()
    return str(value)


def make_stylish_diff(diff, spaces_count=4):
    if not diff:
        return '{}'
    indent = SEPARATOR * spaces_count
    lines = []
    for node in diff:
        key = node.key
        type_ = node.type
        value = getattr(node, 'value', None)
        old_value = getattr(node, 'old_value', None)
        new_value = getattr(node, 'new_value', None)

        if type_ == "unchanged":
            lines.append(
                f"{indent}{NONE}{key}: {format_value(value, spaces_count)}"
            )
        elif type_ == "changed":
            lines.append(
                f"{indent}{DEL}{key}: {format_value(old_value, spaces_count)}"
            )
            lines.append(
                f"{indent}{ADD}{key}: {format_value(new_value, spaces_count)}"
            )
        elif type_ == "removed":
            lines.append(
                f"{indent}{DEL}{key}: {format_value(value, spaces_count)}"
            )
        elif type_ == "added":
            lines.append(
                f"{indent}{ADD}{key}: {format_value(value, spaces_count)}"
            )
        elif type_ == "nested":
            children = make_stylish_diff(node.children, spaces_count + 4)
            lines.append(f"{indent}{NONE}{key}: {children}")
    formatted_string = '\n'.join(lines)
    end_indent = SEPARATOR * (spaces_count - 4)
    return f"{{\n{formatted_string}\n{end_indent}}}"


def format_diff(diff):
    return make_stylish_diff(diff)