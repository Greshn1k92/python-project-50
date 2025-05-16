import json
import os
import tempfile

import pytest
import yaml

from gendiff.diff import generate_diff
from gendiff.parser import parse_json, parse_yaml


def create_test_file(data):
    temp = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
    with open(temp.name, 'w') as f:
        json.dump(data, f)
    return temp.name


def create_test_yaml_file(data):
    temp = tempfile.NamedTemporaryFile(delete=False, suffix='.yml')
    with open(temp.name, 'w') as f:
        yaml.dump(data, f)
    return temp.name


@pytest.mark.parametrize('file1, file2, expected_result', [
    ('tests/test_data/file1.json', 'tests/test_data/file2.json', '''{
    - follow: false
      host: hexlet.io
    - proxy: 123.234.53.22
    - timeout: 50
    + timeout: 20
    + verbose: true
}'''),
    ('tests/test_data/file1.yml', 'tests/test_data/file2.yml', '''{
    - follow: false
      host: hexlet.io
    - proxy: 123.234.53.22
    - timeout: 50
    + timeout: 20
    + verbose: true
}''')
])
def test_generate_diff_with_real_files(file1, file2, expected_result):
    file1_data = (
        parse_json(file1) if file1.endswith('.json')
        else parse_yaml(file1)
    )
    file2_data = (
        parse_json(file2) if file2.endswith('.json')
        else parse_yaml(file2)
    )
    result = generate_diff(file1_data, file2_data)
    assert result == expected_result


def test_generate_diff_with_temp_files():
    file1_data = {
        "host": "hexlet.io",
        "timeout": 100,
        "proxy": "123.234.53.22"
    }
    file2_data = {
        "host": "hexlet.io",
        "timeout": 200,
        "verbose": True
    }
    file1 = create_test_file(file1_data)
    file2 = create_test_file(file2_data)
    try:
        data1 = parse_json(file1)
        data2 = parse_json(file2)
        expected = '''{
      host: hexlet.io
    - proxy: 123.234.53.22
    - timeout: 100
    + timeout: 200
    + verbose: true
}'''
        assert generate_diff(data1, data2) == expected
    finally:
        os.unlink(file1)
        os.unlink(file2)


@pytest.mark.parametrize('file1_data, file2_data, expected_result', [
    ({}, {}, '{}'),
    (
        {"host": "hexlet.io", "timeout": 100},
        {"host": "hexlet.io", "timeout": 100},
        '''{
      host: hexlet.io
      timeout: 100
}'''
    )
])
def test_generate_diff_with_special_cases(
    file1_data, file2_data, expected_result
):
    result = generate_diff(file1_data, file2_data)
    assert result == expected_result


@pytest.mark.parametrize('file1, file2, expected_result', [
    (
        'tests/test_data/file1_nested.json',
        'tests/test_data/file2_nested.json',
        '''{
    common: {
      + follow: false
        setting1: Value 1
      - setting2: 200
      - setting3: true
      + setting3: null
      + setting4: blah blah
      + setting5: {
            key5: value5
        }
        setting6: {
            key: value
          + ops: vops
            doge: {
              - wow: 
              + wow: so much
            }
        }
    }
    group1: {
      - baz: bas
      + baz: bars
        foo: bar
      - nest: {
            key: value
        }
      + nest: str
    }
  - group2: {
        abc: 12345
        deep: {
            id: 45
        }
    }
  + group3: {
        deep: {
            id: {
                number: 45
            }
        }
        fee: 100500
    }
}'''
    ),
    (
        'tests/test_data/file1_nested.yml',
        'tests/test_data/file2_nested.yml',
        '''{
    common: {
      + follow: false
        setting1: Value 1
      - setting2: 200
      - setting3: true
      + setting3: null
      + setting4: blah blah
      + setting5: {
            key5: value5
        }
        setting6: {
            key: value
          + ops: vops
            doge: {
              - wow: 
              + wow: so much
            }
        }
    }
    group1: {
      - baz: bas
      + baz: bars
        foo: bar
      - nest: {
            key: value
        }
      + nest: str
    }
  - group2: {
        abc: 12345
        deep: {
            id: 45
        }
    }
  + group3: {
        deep: {
            id: {
                number: 45
            }
        }
        fee: 100500
    }
}'''
    )
])
def test_generate_diff_with_nested_files(file1, file2, expected_result):
    file1_data = (
        parse_json(file1) if file1.endswith('.json')
        else parse_yaml(file1)
    )
    file2_data = (
        parse_json(file2) if file2.endswith('.json')
        else parse_yaml(file2)
    )
    result = generate_diff(file1_data, file2_data)
    assert result == expected_result


def test_generate_diff_with_explicit_format():
    file1_data = {
        "host": "hexlet.io",
        "timeout": 100
    }
    file2_data = {
        "host": "hexlet.io",
        "timeout": 200
    }
    expected = '''{
      host: hexlet.io
    - timeout: 100
    + timeout: 200
}'''
    result = generate_diff(file1_data, file2_data, format_name='stylish')
    assert result == expected


def test_generate_diff_with_special_values():
    file1_data = {
        "common": {
            "empty": "",
            "null_value": None,
            "bool_value": True
        }
    }
    file2_data = {
        "common": {
            "empty": "not empty",
            "null_value": "not null",
            "bool_value": False
        }
    }
    expected = '''{
    common: {
      - empty: 
      + empty: not empty
      - null_value: null
      + null_value: not null
      - bool_value: true
      + bool_value: false
    }
}'''
    result = generate_diff(file1_data, file2_data)
    assert result == expected 