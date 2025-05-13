import json
import os
import tempfile
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


def test_generate_diff_with_real_files():
    file1_data = parse_json('tests/test_data/file1.json')
    file2_data = parse_json('tests/test_data/file2.json')
    expected = '''{
    - follow: false
      host: hexlet.io
    - proxy: 123.234.53.22
    - timeout: 50
    + timeout: 20
    + verbose: true
}'''
    result = generate_diff(file1_data, file2_data)
    assert result == expected


def test_generate_diff_with_real_yaml_files():
    file1_data = parse_yaml('tests/test_data/file1.yml')
    file2_data = parse_yaml('tests/test_data/file2.yml')
    expected = '''{
    - follow: false
      host: hexlet.io
    - proxy: 123.234.53.22
    - timeout: 50
    + timeout: 20
    + verbose: true
}'''
    result = generate_diff(file1_data, file2_data)
    assert result == expected


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


def test_generate_diff_with_empty_files():
    file1 = create_test_file({})
    file2 = create_test_file({})
    try:
        data1 = parse_json(file1)
        data2 = parse_json(file2)
        expected = '{}'
        assert generate_diff(data1, data2) == expected
    finally:
        os.unlink(file1)
        os.unlink(file2)


def test_generate_diff_with_same_files():
    data = {
        "host": "hexlet.io",
        "timeout": 100
    }
    file1 = create_test_file(data)
    file2 = create_test_file(data)
    try:
        data1 = parse_json(file1)
        data2 = parse_json(file2)
        expected = '''{
      host: hexlet.io
      timeout: 100
}'''
        assert generate_diff(data1, data2) == expected
    finally:
        os.unlink(file1)
        os.unlink(file2)


def test_generate_diff_with_yaml_files():
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
    file1 = create_test_yaml_file(file1_data)
    file2 = create_test_yaml_file(file2_data)
    try:
        data1 = parse_yaml(file1)
        data2 = parse_yaml(file2)
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


def test_generate_diff_with_mixed_files():
    json_data = {
        "host": "hexlet.io",
        "timeout": 100,
        "proxy": "123.234.53.22"
    }
    yaml_data = {
        "host": "hexlet.io",
        "timeout": 200,
        "verbose": True
    }
    json_file = create_test_file(json_data)
    yaml_file = create_test_yaml_file(yaml_data)
    try:
        data1 = parse_json(json_file)
        data2 = parse_yaml(yaml_file)
        expected = '''{
      host: hexlet.io
    - proxy: 123.234.53.22
    - timeout: 100
    + timeout: 200
    + verbose: true
}'''
        assert generate_diff(data1, data2) == expected
    finally:
        os.unlink(json_file)
        os.unlink(yaml_file) 