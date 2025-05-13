def format_value(value, depth):
    if value is None:
        return 'null'
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, dict):
        if not value:
            return '{}'
        indent = ' ' * (depth * 4 + 6)
        closing_indent = ' ' * (depth * 4 + 4)
        lines = [f"{indent}{k}: {format_value(v, depth + 1)}" for k, v in value.items()]
        return '{\n' + '\n'.join(lines) + f'\n{closing_indent}' + '}'
    return str(value)


def format_node(node, depth):
    key = node.key
    type_ = node.type
    value = node.value
    key_indent = ' ' * (depth * 4 + 4)
    sign_indent = ' ' * (depth * 4 + 2)

    if type_ == 'nested':
        children = [format_node(child, depth + 1) for child in node.children]
        return f"{key_indent}{key}: {{\n" + '\n'.join(children) + f"\n{key_indent}}}"
    elif type_ == 'added':
        return f"{sign_indent}+ {key}: {format_value(value, depth)}"
    elif type_ == 'removed':
        return f"{sign_indent}- {key}: {format_value(value, depth)}"
    elif type_ == 'unchanged':
        return f"{key_indent}{key}: {format_value(value, depth)}"
    elif type_ == 'changed':
        old_value, new_value = node.old_value, node.new_value
        return (f"{sign_indent}- {key}: {format_value(old_value, depth)}\n"
                f"{sign_indent}+ {key}: {format_value(new_value, depth)}")


def format_diff(diff):
    if not diff:
        return '{}'
    lines = [format_node(node, 0) for node in diff]
    return '{\n' + '\n'.join(lines) + '\n}'