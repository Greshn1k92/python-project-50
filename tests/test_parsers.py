import pytest

from gendiff.parsers import get_file_format, parse_data, parse_file, read_file


@pytest.mark.parametrize('file_path,expected', [
    ('file.json', 'json'),
    ('file.yaml', 'yaml'),
    ('file.yml', 'yml')
])
def test_get_file_format(file_path, expected):
    assert get_file_format(file_path) == expected


def test_read_file():
    content = read_file('tests/test_data/file1.json')
    assert isinstance(content, str)
    assert len(content) > 0

    with pytest.raises(FileNotFoundError):
        read_file('nonexistent.json')


@pytest.mark.parametrize('data,format,expected', [
    ('{"key": "value"}', 'json', {"key": "value"}),
    ('key: value', 'yaml', {"key": "value"}),
    ('key: value', 'yml', {"key": "value"})
])
def test_parse_data_valid(data, format, expected):
    assert parse_data(data, format) == expected


@pytest.mark.parametrize('data,format,error_msg', [
    ('{"key": "value"', 'json', 'Invalid JSON'),
    ('key: value\n  nested:', 'yaml', 'Invalid YAML'),
    ('some data', 'txt', 'Unsupported file format')
])
def test_parse_data_invalid(data, format, error_msg):
    with pytest.raises(ValueError) as exc_info:
        parse_data(data, format)
    assert error_msg in str(exc_info.value)


def test_parse_file():
    file_paths = [
        'tests/test_data/file1.json',
        'tests/test_data/file1.yaml'
    ]
    for file_path in file_paths:
        result = parse_file(file_path)
        assert isinstance(result, dict)
        assert len(result) > 0

    with pytest.raises(FileNotFoundError):
        parse_file('nonexistent.json') 