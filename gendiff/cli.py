import argparse
import os

from gendiff.diff import generate_diff
from gendiff.parsers import parse_file


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("first_file")
    parser.add_argument("second_file")
    parser.add_argument(
        "-f",
        "--format",
        default="stylish",
        help="set format of output (default: stylish)",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    print(generate_diff(args.first_file, args.second_file, args.format))


if __name__ == "__main__":
    main() 