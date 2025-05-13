from typing import Any, List

from gendiff.diff_tree import DiffNode


def format_value(value, depth):
    if value is None:
        return 'null'
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        indent = '    ' * (depth + 1)
        lines = [f"{indent}{k}: {format_value(v, depth + 1)}" for k, v in value.items()]
        closing = '    ' * depth
        return f"{{\n{chr(10).join(lines)}\n{closing}}}"
    return str(value)


def format_node(node, depth=1):
    indent = '    ' * (depth - 1)
    if node.type == 'nested':
        children = ''.join([format_node(child, depth + 1) for child in node.children])
        return f"{indent}{node.key}: {{\n{children}{indent}}}\n"
    elif node.type == 'added':
        return f"{indent}+ {node.key}: {format_value(node.value, depth)}\n"
    elif node.type == 'removed':
        return f"{indent}- {node.key}: {format_value(node.value, depth)}\n"
    elif node.type == 'unchanged':
        return f"{indent}{node.key}: {format_value(node.value, depth)}\n"
    elif node.type == 'changed':
        return (
            f"{indent}- {node.key}: {format_value(node.old_value, depth)}\n"
            f"{indent}+ {node.key}: {format_value(node.new_value, depth)}\n"
        )


def format_diff(diff):
    if not diff:
        return '{}'
    result = '{\n'
    for node in diff:
        result += format_node(node, 1)
    result += '}'
    return result 