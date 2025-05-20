def format_value(value):
    if isinstance(value, dict):
        return '[complex value]'
    if isinstance(value, str):
        return f"'{value}'"
    if value is None:
        return 'null'
    if isinstance(value, bool):
        return str(value).lower()
    return str(value)


def build_plain_lines(diff_dict, current_path_prefix=''):
    lines = []
    for key in sorted(diff_dict.keys()):
        item_data = diff_dict[key]
        full_path = (
            f"{current_path_prefix}.{key}" if current_path_prefix else key
        )

        status = item_data.get('status')

        if status == 'nested':
            lines.extend(build_plain_lines(item_data['children'], full_path))
        elif status == 'added':
            formatted_value = format_value(item_data['value'])
            lines.append(
                f"Property '{full_path}' was added with value: "
                f"{formatted_value}"
            )
        elif status == 'removed':
            lines.append(f"Property '{full_path}' was removed")
        elif status == 'changed':
            formatted_old_value = format_value(item_data['old_value'])
            formatted_new_value = format_value(item_data['new_value'])
            lines.append(
                f"Property '{full_path}' was updated. From "
                f"{formatted_old_value} to {formatted_new_value}"
            )
    return lines


def format_diff(diff_data):
    if not isinstance(diff_data, dict):
        return ""
        
    lines = build_plain_lines(diff_data)
    return '\n'.join(lines) 