"""Advent of Code 2025 Day 6 Solution

author: Dan Blanchard
"""

import argparse
from functools import reduce
import operator

SYMBOL_TO_OPERATOR = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
}


def parse_line(line: str):
    return list(line.strip().split())


def parse_input_file(input_file: str):
    problems = []
    with open(input_file, "r") as file:
        for line in file:
            entries = parse_line(line)
            if not problems:
                problems = [list() for _ in range(len(entries))]
            for i, entry in enumerate(entries):
                problems[i].append(entry)
    return problems


def parse_input_file_columnwise(input_file: str):
    problems = []
    with open(input_file, "r") as file:
        # Find longest line so that we know max column
        max_length = max(len(line.rstrip("\n")) for line in file)
        file.seek(0)

        # Rotate file
        rotated_lines = [""] * max_length
        for line in file:
            line = line.rstrip("\n")
            length_diff = max_length - len(line)
            if length_diff:
                line += " " * length_diff
            for i, char in enumerate(reversed(line)):
                rotated_lines[i] += char

        # Parse rotated lines
        problem = []
        for line in rotated_lines:
            line = line.strip()
            if not line:
                continue
            if line[-1].isnumeric():
                problem.append(line)
            else:
                problem.append(line[:-1])
                problem.append(line[-1])
                problems.append(problem)
                problem = []

    return problems


def solve_problems(problems, verbose):
    answers = []
    for problem in problems:
        operator = problem[-1]
        operands = [int(x) for x in problem[:-1]]
        answer = reduce(SYMBOL_TO_OPERATOR[operator], operands)
        if verbose:
            print(f"{f' {operator} '.join(problem[:-1])} = {answer}")
        answers.append(answer)
    return answers


def main(*, input_file: str, verbose: bool, col_numbers: bool):
    problems = (
        parse_input_file(input_file)
        if not col_numbers
        else parse_input_file_columnwise(input_file)
    )
    answers = solve_problems(problems, verbose)
    print(f"Grand total: {sum(answers)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Do the cephalapod math for day 6 of Advent of Code."
    )
    parser.add_argument("input_file", type=str, help="Path to the input file")
    parser.add_argument(
        "-c",
        "--col_numbers",
        action="store_true",
        help="Read the numbers in right-to-left columns instead of horizontally (for part 2)",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Print debug messages"
    )
    args = parser.parse_args()

    main(input_file=args.input_file, verbose=args.verbose, col_numbers=args.col_numbers)
