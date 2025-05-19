import pytest

from gendiff.diff import generate_diff


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