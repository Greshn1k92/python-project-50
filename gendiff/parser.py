import json

import yaml


def parse_json(file_path):
    return json.load(open(file_path))


def parse_yaml(file_path):
    return yaml.safe_load(open(file_path)) 