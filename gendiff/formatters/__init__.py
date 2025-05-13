from gendiff.formatters.plain import format_diff as plain
from gendiff.formatters.stylish import format_diff as stylish

FORMATTERS = {
    'stylish': stylish,
    'plain': plain,
} 