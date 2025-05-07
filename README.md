# Hexlet Code

## Description
Generate diff between two configuration files.

## Installation
```bash
pip install hexlet-code
```

## Usage
```python
from gendiff import generate_diff

diff = generate_diff('file1.json', 'file2.json')
print(diff)
```

## Example
```bash
$ gendiff file1.json file2.json
{
  - follow: false
    host: hexlet.io
  - proxy: 123.234.53.22
  - timeout: 50
  + timeout: 20
  + verbose: true
}
```

### Hexlet tests and linter status:
[![Actions Status](https://github.com/Greshn1k92/python-project-50/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Greshn1k92/python-project-50/actions)