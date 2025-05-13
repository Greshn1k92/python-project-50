from gendiff.formatters.stylish import format_diff as stylish
from gendiff.formatters.plain import format_diff as plain

FORMATTERS = {
    'stylish': stylish,
    'plain': plain,
} 