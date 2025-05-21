import pytest

from gendiff.diff import generate_diff


def read_file(path):
    with open(path) as f:
        return f.read()


@pytest.mark.parametrize('file_path1, file_path2, expected_result', [
    ('tests/test_data/file1.json',
     'tests/test_data/file2.json',
     'tests/test_data/expected_result_json.txt'),
    ('tests/test_data/file1.yaml',
     'tests/test_data/file2.yaml',
     'tests/test_data/expected_result_yaml.txt')])
def test_generate_diff(file_path1, file_path2, expected_result):
    diff = generate_diff(file_path1, file_path2)
    expected = read_file(expected_result).strip()
    assert diff.strip() == expected


@pytest.mark.parametrize('file_path1, file_path2, expected_result', [
    ('tests/test_data/file1.json',
     'tests/test_data/file2.json',
     'tests/test_data/expected_result_plain.txt'),
    ('tests/test_data/file1.yaml',
     'tests/test_data/file2.yaml',
     'tests/test_data/expected_result_plain.txt')])
def test_generate_diff_plain(file_path1, file_path2, expected_result):
    diff = generate_diff(file_path1, file_path2, format_name="plain")
    expected = read_file(expected_result).strip()
    assert diff.strip() == expected


@pytest.mark.parametrize('file_path1, file_path2, expected_result', [
    ('tests/test_data/file1.json',
     'tests/test_data/file2.json',
     'tests/test_data/expected_result_json_format.txt'),
    ('tests/test_data/file1.yaml',
     'tests/test_data/file2.yaml',
     'tests/test_data/expected_result_json_format.txt')])
def test_generate_diff_json(file_path1, file_path2, expected_result):
    diff = generate_diff(file_path1, file_path2, format_name="json")
    expected = read_file(expected_result).strip()
    assert diff.strip() == expected






