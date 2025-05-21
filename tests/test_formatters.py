from gendiff.formatters.json import format_diff_json as format_json
from gendiff.formatters.plain import format_diff as format_plain
from gendiff.formatters.stylish import format_diff_stylish


def test_format_json_special_values():
    diff = {
        'null_value': {
            'status': 'changed',
            'old_value': None,
            'new_value': 'not null'
        },
        'bool_value': {
            'status': 'changed',
            'old_value': False,
            'new_value': True
        },
        'number': {
            'status': 'changed',
            'old_value': 0,
            'new_value': 42
        }
    }
    result = format_json(diff)
    assert '"null_value"' in result
    assert '"bool_value"' in result
    assert '"number"' in result
    assert '"old_value": null' in result
    assert '"new_value": "not null"' in result
    assert '"old_value": false' in result
    assert '"new_value": true' in result


def test_format_json_empty():
    assert format_json({}) == '[]'


def test_format_stylish_empty():
    assert format_diff_stylish({}) == '{\n\n}'


def test_format_plain_empty():
    assert format_plain({}) == '' 