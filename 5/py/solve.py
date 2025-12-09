"""Advent of Code 2025 Day 5 Solution

author: Dan Blanchard
"""

import argparse


def parse_line(line: str):
    return list(line.strip())


def parse_input_file(input_file: str):
    fresh_ranges = []
    available_ingredients = set()
    with open(input_file, "r") as file:
        saw_blank = False
        for line in file:
            if not line.strip():
                saw_blank = True
                continue
            if saw_blank:
                available_ingredients.add(int(line.strip()))
            else:
                start, end = line.strip().split("-")
                fresh_ranges.append((int(start), int(end)))
    return fresh_ranges, available_ingredients


def find_fresh_ingredients(fresh_ranges, available_ingredients):
    fresh_ingredients = set()
    for ingredient in available_ingredients:
        for start, end in fresh_ranges:
            if start <= ingredient <= end:
                fresh_ingredients.add(ingredient)
                break
    return fresh_ingredients


def collapse_fresh_ranges(fresh_ranges):
    collapsed_ranges = []
    collapsed_start = None
    collapsed_end = None
    for start, end in sorted(fresh_ranges):
        if collapsed_start is None:
            collapsed_start = start
        if collapsed_end is None:
            collapsed_end = end
        # If start of range is within existing range, end should be
        # greater of the two
        if collapsed_start <= start <= collapsed_end:
            collapsed_end = max(end, collapsed_end)
        # Otherwise, we are at the start of a new range
        else:
            collapsed_ranges.append((collapsed_start, collapsed_end))
            collapsed_start = start
            collapsed_end = end
    if collapsed_start and collapsed_end:
        collapsed_ranges.append((collapsed_start, collapsed_end))
    return collapsed_ranges


def main(*, input_file: str, verbose: bool):
    fresh_ranges, available_ingredients = parse_input_file(input_file)
    fresh_ingredients = find_fresh_ingredients(fresh_ranges, available_ingredients)
    if verbose:
        print(f"Fresh ingredients: {list(sorted(fresh_ingredients))}")
    print(f"Num fresh ingredients: {len(fresh_ingredients)}")

    collapsed_fresh_ranges = collapse_fresh_ranges(fresh_ranges)
    if verbose:
        print("Collapsed fresh ranges:")
        for start, end in collapsed_fresh_ranges:
            print(f"{start}-{end}")
    possible_fresh_ingredients = sum(
        ((end - start) + 1) for start, end in collapsed_fresh_ranges
    )
    print(f"Num possible fresh ingredients: {possible_fresh_ingredients}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Find the accessible spots for day 5 of Advent of Code."
    )
    parser.add_argument("input_file", type=str, help="Path to the input file")
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Print debug messages"
    )
    args = parser.parse_args()

    main(input_file=args.input_file, verbose=args.verbose)
