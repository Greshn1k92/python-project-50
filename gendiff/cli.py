import argparse
import os

from gendiff.diff import generate_diff
from gendiff.parser import parse_json, parse_yaml


def get_file_parser(file_path):
    _, ext = os.path.splitext(file_path)
    if ext.lower() in ['.yaml', '.yml']:
        return parse_yaml
    return parse_json


def parse_args():
    parser = argparse.ArgumentParser(
        description="Compares two configuration files and shows a difference.",
    )
    parser.add_argument("first_file")
    parser.add_argument("second_file")
    parser.add_argument(
        "-f",
        "--format",
        help="set format of output",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    parse_first = get_file_parser(args.first_file)
    parse_second = get_file_parser(args.second_file)
    data1 = parse_first(args.first_file)
    data2 = parse_second(args.second_file)
    print(generate_diff(data1, data2))


if __name__ == "__main__":
    main() 