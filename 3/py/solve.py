"""Advent of Code 2025 Day 3 Solution

author: Dan Blanchard
"""

import argparse
from collections import defaultdict


def parse_line(line: str):
    return [int(x) for x in line.strip()]


def find_largest_n_digit_num(joltages: list[int], n: int) -> int:
    # Pick first n digits as a starting point of comparison
    digit_list = []

    # Store where each digit is located
    digit_locations = defaultdict(list)
    for i, digit in enumerate(joltages):
        digit_locations[digit].append(i)

    digit_index = -1
    for digit_pos in range(n):
        min_index = digit_index + 1
        max_index = len(joltages) - (n - digit_pos)
        greatest_digit = 0
        for digit, locations in digit_locations.items():
            for location in locations:
                if location > max_index:
                    break
                if location >= min_index and digit > greatest_digit:
                    greatest_digit = digit
                    digit_index = location
                    break
        digit_list.append(greatest_digit)

    if len(digit_list) != n:
        raise RuntimeError(
            f"Calculated invalid digit list of length {len(digit_list)} when desired {n}"
        )

    return int("".join(str(digit) for digit in digit_list))


def main(*, input_file: str, verbose: bool, n: int):
    total = 0
    with open(input_file, "r") as file:
        lines = file.readlines()
        for line in lines:
            joltages = parse_line(line)
            largest_num = find_largest_n_digit_num(joltages, n)
            total += largest_num
            if verbose:
                print(f"{line.strip()}: largest is {largest_num}; total is {total}")

    print(f"Total joltage: {total}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Calculate the total joltage for day 3 of Advent of Code."
    )
    parser.add_argument("input_file", type=str, help="Path to the input file")
    parser.add_argument("-n", default=2, type=int, help="Length of number of to find")
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Print debug messages"
    )
    args = parser.parse_args()

    main(input_file=args.input_file, verbose=args.verbose, n=args.n)
