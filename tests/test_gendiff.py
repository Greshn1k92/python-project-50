import pytest

from gendiff.diff import generate_diff
from gendiff.parsers import parse_file


def read_file(path):
    with open(path) as f:
        return f.read()


@pytest.mark.parametrize('file1, file2, expected', [
    (
        'tests/test_data/file1.json',
        'tests/test_data/file2.json',
        'tests/test_data/expected.txt'
    ),
    (
        'tests/test_data/file1.yml',
        'tests/test_data/file2.yml',
        'tests/test_data/expected.txt'
    ),
])
def test_generate_diff(file1, file2, expected):
    result = generate_diff(file1, file2)
    assert result.strip() == read_file(expected).strip()


@pytest.mark.parametrize('file1, file2, expected_result', [
    (
        'tests/test_data/file1.json',
        'tests/test_data/file2.json',
        read_file('tests/test_data/expected.txt')
    ),
    (
        'tests/test_data/file1.yml',
        'tests/test_data/file2.yml',
        read_file('tests/test_data/expected.txt')
    )
])
def test_generate_diff_with_real_files(file1, file2, expected_result):
    result = generate_diff(file1, file2)
    assert result.strip() == expected_result.strip()


@pytest.mark.parametrize('file1, file2, expected_result', [
    (
        'tests/test_data/file1_nested.json',
        'tests/test_data/file2_nested.json',
        read_file('tests/test_data/expected_nested.txt')
    ),
    (
        'tests/test_data/file1_nested.yml',
        'tests/test_data/file2_nested.yml',
        read_file('tests/test_data/expected_nested.txt')
    )
])
def test_generate_diff_nested(file1, file2, expected_result):
    result = generate_diff(file1, file2)
    assert result.strip() == expected_result.strip()


def test_parse_file_not_found():
    with pytest.raises(FileNotFoundError):
        parse_file('nonexistent.json')


def test_parse_file_invalid_json(tmp_path):
    invalid_json = tmp_path / "invalid.json"
    invalid_json.write_text("{invalid json")
    with pytest.raises(ValueError) as exc_info:
        parse_file(str(invalid_json))
    assert "Invalid JSON file" in str(exc_info.value)


def test_parse_file_invalid_yaml(tmp_path):
    invalid_yaml = tmp_path / "invalid.yml"
    invalid_yaml.write_text("invalid: yaml: content:")
    with pytest.raises(ValueError) as exc_info:
        parse_file(str(invalid_yaml))
    assert "Invalid YAML file" in str(exc_info.value)


def test_parse_file_unsupported_format(tmp_path):
    invalid_file = tmp_path / "invalid.txt"
    invalid_file.write_text("some content")
    with pytest.raises(ValueError) as exc_info:
        parse_file(str(invalid_file))
    assert "Unsupported file format" in str(exc_info.value)