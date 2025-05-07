"""Test module for gendiff package."""

import json
import os
import tempfile
from gendiff.diff import generate_diff
from gendiff.parser import parse_json


def create_test_file(data):
    """Create temporary JSON file with given data."""
    temp = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
    with open(temp.name, 'w') as f:
        json.dump(data, f)
    return temp.name


def test_generate_diff_with_real_files():
    """Test generate_diff function with existing JSON files."""
    file1_data = parse_json('file1.json')
    file2_data = parse_json('file2.json')
    
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
    """Test generate_diff function with temporary JSON files."""
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
    """Test generate_diff function with empty JSON files."""
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
    """Test generate_diff function with identical JSON files."""
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