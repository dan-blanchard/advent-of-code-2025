"""Advent of Code 2025 Day 7 Solution

author: Dan Blanchard
"""

import argparse
from collections import defaultdict
from enum import StrEnum
from dataclasses import dataclass


class StateEnum(StrEnum):
    START = "S"
    EMPTY = "."
    SPLIT = "^"
    BEAM = "|"


@dataclass
class Location:
    state: StateEnum
    column: int


def parse_line(line: str):
    return [
        Location(state=StateEnum(state), column=i)
        for i, state in enumerate(line.strip())
    ]


def parse_input_file(input_file: str):
    rows = []
    with open(input_file, "r") as file:
        for line in file:
            rows.append(parse_line(line))
    return rows


def print_row(row):
    print("".join(location.state for location in row))


def print_rows(rows):
    for row in rows:
        print_row(row)


def shoot_beam(rows, verbose):
    start = next(
        (location.column for location in rows[0] if location.state == StateEnum.START),
        None,
    )
    if start is None:
        raise ValueError(f"Failed to find start in row 0: {rows[0]}")
    beams = {start: 1}
    split_count = 0
    for row_num, row in enumerate(rows):
        if row_num == 0:
            continue
        new_beams = defaultdict(int)
        for beam, path_count in beams.items():
            if row[beam].state == StateEnum.SPLIT:
                row[beam - 1].state = StateEnum.BEAM
                row[beam + 1].state = StateEnum.BEAM
                new_beams[beam - 1] += path_count
                new_beams[beam + 1] += path_count
                split_count += 1
            else:
                row[beam].state = StateEnum.BEAM
                new_beams[beam] += path_count
        if verbose:
            if beams != new_beams:
                print_row(row)
            else:
                print(
                    "".join(
                        [str(new_beams.get(i, row[i].state)) for i in range(len(row))]
                    )
                )

        beams = new_beams

    if verbose:
        print_rows(rows)
    return split_count, sum(beams.values())


def main(*, input_file: str, verbose: bool):
    rows = parse_input_file(input_file)
    if verbose:
        print_rows(rows)
        print()
    split_count, quantum_count = shoot_beam(rows, verbose)
    print(f"Split count: {split_count}")
    print(f"Quantum count: {quantum_count}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Split some tachyon beams for day 7 of Advent of Code."
    )
    parser.add_argument("input_file", type=str, help="Path to the input file")
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Print debug messages"
    )
    args = parser.parse_args()

    main(input_file=args.input_file, verbose=args.verbose)
