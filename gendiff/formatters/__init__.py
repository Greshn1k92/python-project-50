from gendiff.formatters.json import format_diff_json as json_formatter
from gendiff.formatters.plain import format_diff as plain
from gendiff.formatters.stylish import format_diff_stylish as stylish

FORMATTERS = {
    'stylish': stylish,
    'plain': plain,
    'json': json_formatter,
}