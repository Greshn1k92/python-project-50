def format_value(value):
    if isinstance(value, dict):
        return '[complex value]'
    if isinstance(value, str):
        return f"'{value}'"
    if value is None:
        return 'null'
    return str(value).lower() if isinstance(value, bool) else str(value)


def format_node(node, path=''):
    current_path = f"{path}.{node.key}" if path else node.key
    
    if node.type == 'nested':
        return ''.join([format_node(child, current_path) for child in node.children])
    elif node.type == 'added':
        return f"Property '{current_path}' was added with value: {format_value(node.value)}\n"
    elif node.type == 'removed':
        return f"Property '{current_path}' was removed\n"
    elif node.type == 'changed':
        return (
            f"Property '{current_path}' was updated. "
            f"From {format_value(node.old_value)} to {format_value(node.new_value)}\n"
        )
    return ''


def format_diff(diff):
    if not diff:
        return ''
    result = ''.join([format_node(node) for node in diff])
    return result.rstrip() 