"""Advent of Code 2025 Day 1 Solution

author: Dan Blanchard
"""

import argparse


def parse_line(line: str) -> tuple[str, int]:
    line = line.strip()
    direction = line[0]
    value = int(line[1:])
    return direction, value


def main(*, input_file: str, verbose: bool):
    position = 50
    exact_zero_count = 0
    passed_zero_count = 0
    if verbose:
        print(f"  - The dial starts by pointing at {position}")
    with open(input_file, "r") as file:
        lines = file.readlines()
        for line in lines:
            direction, value = parse_line(line)
            # If we are turning right, we increase, left, we decrease
            mult = 1 if direction == "R" else -1
            start_pos = position
            position += mult * value
            # Count approximately how many times we passed through
            # position 0, but needs correction for edge cases to handle
            # the distinctions between leaving, landing, and passing zero
            passes = abs(position // 100)
            # Apply modulo to get final position in [0, 99]
            position = position % 100
            # Apply corrections for asymmetry in how floor division treats
            # positive vs negative multiples of 100
            if passes > 0:
                # Subtract 1 in these cases where the formula overcounts:
                #
                # 1. ENDED at zero going RIGHT
                #    Example: R48 from 52 → raw=100 → pos=0
                #    Formula gives 1, but we LANDED on 0 (should be exact, not pass)
                #
                # 2. STARTED at zero and ENDED at zero
                #    Example: L100 from 0 → raw=-100 → pos=0
                #    Formula gives 1, but only visit is the landing (exact, not pass)
                #
                # 3. STARTED at zero and went LEFT
                #    Example: L30 from 0 → raw=-30 → pos=70
                #    Formula gives 1, but we started at 0, didn't pass through it
                #
                # The ONE case where we DON'T subtract when we END at zero:
                # - ENDED at zero by going LEFT from non-zero
                #   Example: L325 from 25 → raw=-300 → pos=0
                #   We visit 0 four times: at 0, -100, -200, -300 (all ≡ 0 mod 100)
                #   Should be: passes=3 (first three), exact=1 (final landing)
                #   Formula gives: abs(-300 // 100) = 3 ✓
                #   The formula naturally counts only intermediate visits, excluding
                #   the final landing, so no correction needed!
                if (position == 0 and (mult == 1 or start_pos == 0)) or (
                    start_pos == 0 and mult == -1
                ):
                    passes -= 1
            if position == 0:
                exact_zero_count += 1
            passed_zero_count += passes
            if verbose:
                print(
                    f"  - The dial is rotated {direction}{value} to point at {position}",
                    end="",
                )
                if passes:
                    print(
                        f"; during this rotation, it points at 0 {'once' if passes == 1 else f'{passes} times'}",
                        end="",
                    )
                print()

    print(f"Password (exact): {exact_zero_count}")
    print(f"Password (exact + passed): {exact_zero_count + passed_zero_count}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Open the safe for day 1 of Advent of Code."
    )
    parser.add_argument("input_file", type=str, help="Path to the input file")
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Print debug messages"
    )
    args = parser.parse_args()

    main(input_file=args.input_file, verbose=args.verbose)
