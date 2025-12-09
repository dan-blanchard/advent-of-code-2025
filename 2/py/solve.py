"""Advent of Code 2025 Day 2 Solution

author: Dan Blanchard
"""

import argparse
import re


def parse_line(line: str):
    line = line.strip()
    for range in line.split(","):
        start, end = range.split("-")
        yield int(start), int(end)


def is_invalid_id(id: int):
    return bool(re.match(r"^(.+)\1$", str(id)))


def is_invalid_id2(id: int):
    return bool(re.match(r"^(.+)\1+$", str(id)))


def main(*, input_file: str, verbose: bool):
    invalid_sum = 0
    invalid_sum2 = 0
    with open(input_file, "r") as file:
        lines = file.readlines()
        for line in lines:
            for start, end in parse_line(line):
                for id in range(start, end + 1):
                    if is_invalid_id(id):
                        invalid_sum += id
                        if verbose:
                            print(f"Invalid ID (Part 1): {id}")
                    if is_invalid_id2(id):
                        invalid_sum2 += id
                        if verbose:
                            print(f"Invalid ID (Part 2): {id}")

    print(f"Invalid sum (Part 1): {invalid_sum}")
    print(f"Invalid sum (Part 2): {invalid_sum2}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Find the invalid IDs for day 2 of Advent of Code."
    )
    parser.add_argument("input_file", type=str, help="Path to the input file")
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Print debug messages"
    )
    args = parser.parse_args()

    main(input_file=args.input_file, verbose=args.verbose)
