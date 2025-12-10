"""Advent of Code 2025 Day 8 Solution

author: Dan Blanchard
"""

import argparse
import itertools
from math import sqrt, prod
from operator import itemgetter


class JunctionBox:
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z
        self.circuit = {self}
        self.connections = {self}

    def distance_from(self, other):
        return sqrt(
            ((self.x - other.x) ** 2)
            + ((self.y - other.y) ** 2)
            + ((self.z - other.z) ** 2)
        )

    def connect(self, other):
        # Update circuits
        self.circuit.update(other.circuit)
        for box in self.circuit:
            box.circuit = self.circuit
        # Update direct connections
        self.connections.add(other)
        other.connections.add(self)

    def __eq__(self, other: "JunctionBox") -> bool:
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))

    def __str__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"


def connect_closest_boxes(boxes, iterations: int, verbose):
    box_distances = {
        (box1, box2): box1.distance_from(box2)
        for box1, box2 in itertools.combinations(boxes, 2)
    }
    closest_boxes = sorted(box_distances.items(), key=itemgetter(1))
    for i, ((box1, box2), distance) in enumerate(closest_boxes):
        if iterations and i > iterations:
            break
        if verbose:
            print(f"Connected {box1} to {box2} with distance {distance}")
            if box1.circuit == box2.circuit:
                print("...but they were already in the same circuit")
        box1.connect(box2)
        if len(box1.circuit) == len(boxes):
            print(f"Final connection made between {box1} and {box2}")
            print(f"Product of X of those boxes = {box1.x * box2.x}")
            break


def find_circuits(boxes):
    circuits: list[set[JunctionBox]] = []
    seen_boxes = set()
    for box in boxes:
        if box in seen_boxes:
            continue
        circuits.append(box.circuit)
        seen_boxes.update(box.circuit)
    return circuits


def parse_line(line: str):
    return JunctionBox(*[int(i) for i in line.strip().split(",")])


def parse_input_file(input_file: str):
    boxes = list()
    with open(input_file, "r") as file:
        for line in file:
            boxes.append(parse_line(line))
    return boxes


def main(*, input_file: str, verbose: bool, n: int):
    boxes = parse_input_file(input_file)
    if verbose:
        for box in boxes:
            print(str(box))
    connect_closest_boxes(boxes, n, verbose)
    # if verbose:
    #     print(boxes)
    circuits = find_circuits(boxes)
    if verbose:
        for i, circuit in enumerate(circuits):
            print(f"Circuit {i}:")
            for box in circuit:
                print(f"  {box}")
    print(f"Num circuits: {len(circuits)}")
    circuit_sizes = [len(circuit) for circuit in circuits]
    print(f"Circuit sizes: {circuit_sizes}")
    largest_sizes = sorted(circuit_sizes, reverse=True)[:3]
    print(
        f"Largest three product: {' x '.join(str(x) for x in largest_sizes)} = {prod(largest_sizes)}"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Connect some junction boxes for day 8 of Advent of Code."
    )
    parser.add_argument("input_file", type=str, help="Path to the input file")
    parser.add_argument("-n", type=int, help="Number of pairs to try to connect")
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Print debug messages"
    )
    args = parser.parse_args()

    main(input_file=args.input_file, verbose=args.verbose, n=args.n)
