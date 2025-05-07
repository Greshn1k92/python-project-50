import argparse

from gendiff.diff import generate_diff
from gendiff.parser import parse_json


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
    data1 = parse_json(args.first_file)
    data2 = parse_json(args.second_file)
    print(generate_diff(data1, data2))


if __name__ == "__main__":
    main() 