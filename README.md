# Вычислитель отличий

[![Actions Status](https://github.com/Greshn1k92/python-project-50/workflows/Python%20CI/badge.svg)](https://github.com/Greshn1k92/python-project-50/actions)
<!--
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Greshn1k92_python-project-50&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=Greshn1k92_python-project-50)
-->
[![Test Coverage](https://sonarcloud.io/api/project_badges/measure?project=Greshn1k92_python-project-50&metric=coverage)](https://sonarcloud.io/summary/new_code?id=Greshn1k92_python-project-50)

## Description
Generate diff between two configuration files.

[![asciicast](https://asciinema.org/a/S0l8nqXjB6Lttjosv1ZWaUfVE.svg)](https://asciinema.org/a/S0l8nqXjB6Lttjosv1ZWaUfVE)
[![asciicast](https://asciinema.org/a/ACrGk9Vm5Hjnfb4x2Emr1pXcb.svg)](https://asciinema.org/a/ACrGk9Vm5Hjnfb4x2Emr1pXcb)
[![asciicast](https://asciinema.org/a/1CxCPJdhKmnG5uyXqTxPbSaWB.svg)](https://asciinema.org/a/1CxCPJdhKmnG5uyXqTxPbSaWB)

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