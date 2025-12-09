"""Advent of Code 2025 Day 4 Solution

author: Dan Blanchard
"""

import argparse


def parse_line(line: str):
    return list(line.strip())


def parse_input_file(input_file: str):
    grid = []
    with open(input_file, "r") as file:
        lines = file.readlines()
        for line in lines:
            grid.append(parse_line(line))
    return grid


def count_adjacent_rolls(grid: list[list[str]], row: int, col: int) -> int:
    count = 0
    for row_delta in (-1, 0, 1):
        row_idx = row + row_delta
        if row_idx >= len(grid):
            break
        if row_idx < 0:
            continue
        current_row = grid[row_idx]
        for col_delta in (-1, 0, 1):
            col_idx = col + col_delta
            if col_idx >= len(current_row):
                break
            if col_delta == row_delta == 0 or col_idx < 0:
                continue
            if current_row[col_idx] == "@":
                count += 1
    return count


def find_accessible_spots(grid: list[list[str]]) -> set[tuple[int, int]]:
    adjacent_counts = get_adjacent_counts(grid)
    accessible_spots = set()
    for row_idx, grid_row in enumerate(grid):
        for col_idx, spot in enumerate(grid_row):
            if spot == "@" and adjacent_counts[row_idx][col_idx] < 4:
                accessible_spots.add((row_idx, col_idx))
    return accessible_spots


def print_accessible_spots(accessible_spots, grid):
    for row_idx, grid_row in enumerate(grid):
        for col_idx, spot in enumerate(grid_row):
            print("x" if (row_idx, col_idx) in accessible_spots else spot, end="")
        print()


def remove_accessible_rolls(accessible_spots, grid):
    for row_idx, col_idx in accessible_spots:
        grid[row_idx][col_idx] = "."


def get_adjacent_counts(grid: list[list[str]]) -> list[list[int]]:
    adjacent_counts = []
    for row in range(len(grid)):
        adjacent_counts.append(
            [count_adjacent_rolls(grid, row, i) for i in range(len(grid[row]))]
        )
    return adjacent_counts


def main(*, input_file: str, verbose: bool):
    grid = parse_input_file(input_file)
    accessible_spots = find_accessible_spots(grid)
    if verbose:
        print_accessible_spots(accessible_spots, grid)
    print(f"Num accessible spots: {len(accessible_spots)}")

    total_removed = len(accessible_spots)
    while accessible_spots:
        remove_accessible_rolls(accessible_spots, grid)
        accessible_spots = find_accessible_spots(grid)
        total_removed += len(accessible_spots)

    print(f"Total removed: {total_removed}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Find the accessible spots for day 4 of Advent of Code."
    )
    parser.add_argument("input_file", type=str, help="Path to the input file")
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Print debug messages"
    )
    args = parser.parse_args()

    main(input_file=args.input_file, verbose=args.verbose)
