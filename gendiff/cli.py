"""CLI interface for gendiff."""

import argparse


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate diff",
    )
    parser.add_argument("first_file", help="path to first file")
    parser.add_argument("second_file", help="path to second file")
    parser.add_argument(
        "-f",
        "--format",
        help="set format of output",
        default="stylish",
    )
    return parser.parse_args()


def main():
    """Run the main CLI logic."""
    args = parse_args()
    print(f"Comparing {args.first_file} and {args.second_file}")
    print(f"Format: {args.format}")


if __name__ == "__main__":
    main() 