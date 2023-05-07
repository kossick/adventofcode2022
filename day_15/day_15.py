"""
Part 2 works for the input data, but not the test data!

This would need a rewrite for that to work.
"""

from __future__ import annotations
import argparse
from dataclasses import dataclass
import pathlib
import re
import sys
from time import perf_counter
from typing import List, Self, Set, Tuple

CURRENT_PATH = pathlib.Path.cwd()
PARSE_STRING = (
    r"Sensor at x=(?P<sensor_x>-*\d+), y=(?P<sensor_y>-*\d+): "
    r"closest beacon is at x=(?P<beacon_x>-*\d+), y=(?P<beacon_y>-*\d+)"
)
Y_VAL = 2_000_000
# Y_VAL = 10


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __repr__(self: Self) -> str:
        return f"({self.x}, {self.y})"

    def __eq__(self: Self, point: Point):
        return self.x == point.x and self.y == point.y

    def distance_from(self: Self, point: Point):
        """Calculate the Manhatten distance between two points"""
        return abs(self.x - point.x) + abs(self.y - point.y)


@dataclass(frozen=True)
class Sensor(Point):
    nearest_beacon: Point

    def beaconless_border(self: Self) -> Set[Point]:
        """Find the perimeter of the region without beacons for the sensor, excluding the beacon itself"""
        beacon_distance = self.distance_from(self.nearest_beacon)
        border = {
            Point(self.x + beacon_distance, self.y),
            Point(self.x - beacon_distance, self.y),
            Point(self.x, self.y + beacon_distance),
            Point(self.x, self.y - beacon_distance)
        }
        for x in range(1, beacon_distance):
            border = border.union({
                Point(self.x + x, self.y + (beacon_distance - x)),
                Point(self.x - x, self.y + (beacon_distance - x)),
                Point(self.x + x, self.y - (beacon_distance - x)),
                Point(self.x - x, self.y - (beacon_distance - x))
            })
        border.remove(self.nearest_beacon)
        return border

    def beaconless_on_line(self: Self, row: int) -> Set[Point]:
        """Find the perimeter of the region without beacons for the sensor on a given line,

        The beacon is excluded if on the line and the border is shifted accordingly, i.e. to the right if the beacon
        was on the left of the border.    
        """
        height = abs(self.y - row)
        width = self.distance_from(self.nearest_beacon) - height
        return {
            Point(self.x + x, row)
            for x in range(-width, width + 1)
            if Point(self.x + x, row) != self.nearest_beacon
        }

    def border_y_intercepts(self: Self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """
        Return y intercept values for the curves defining the sensor's borderless region.

        The first tuple contains the upper and lower value of the negative gradient curves,
        whilst the second contains the upper and lower value of the positive curves
        """
        beacon_distance = self.distance_from(self.nearest_beacon)
        return (
            (
                self.y + self.x - beacon_distance,
                self.y + self.x + beacon_distance
            ),
            (
                self.y - self.x - beacon_distance,
                self.y - self.x + beacon_distance
            )
        )


def generate_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', default='test.txt')
    return parser


def read_file(file: pathlib.Path) -> List[str]:
    if not file.exists():
        raise FileNotFoundError
    with file.open() as in_file:
        source_data = in_file.readlines()
    return [data.rstrip('\n') for data in source_data]


def parse_coordinates(raw: List[str]) -> List[Sensor]:
    coordinates = list()
    for line in raw:
        m = re.match(PARSE_STRING, line)
        coordinates.append(
            Sensor(
                x=int(m.group('sensor_x')),
                y=int(m.group('sensor_y')),
                nearest_beacon=Point(int(m.group('beacon_x')), int(m.group('beacon_y')))
            )
        )
    return coordinates


def find_missing_gap(intercepts: List[int]) -> int | None:
    """Find gap coordinate based on y-intercept values of curves.

    Following William Yeng's method (https://github.com/womogenes/AoC-2022-Solutions/blob/main/day_15/day_15_p2.py
    and https://www.youtube.com/watch?v=w7m48_uCvWI), we find the point where the distace between two y intercepts
    (corresponding to beaconless border lines) are exactly two apart.
    Returns the min of the two plus one (the actual gap value).
    """
    for id_a, a in enumerate(intercepts):
        for id_b, b in enumerate(intercepts[id_a+1:], start=id_a):
            # print(f"Comparing {a} and {b}, (ids: {id_a}, {id_b} [{id_a // 2}, {id_b // 2}])")
            if id_a // 2 == id_b // 2:
                # print(f"Skipping {a} and {b} (ids: {id_a}, {id_b})")
                continue  # Skip two curves from the same border
            if abs(a - b) == 2:
                return min(a, b) + 1
    return None


def find_gap_coordinates(pos: int, neg: int) -> Tuple[int, int]:
    """Find the intercept coordinates based on given gradients

    Using formulas `y - x = pos = (y_s - x_s)` and `y + x = neg = (y_s + x_s)`
    we can find `x_s = (neg - pos) / 2` and `y_s = (neg + pos) / 2`
    """
    return (
        (neg - pos) // 2,
        (neg + pos) // 2
    )


def calculate_tuning_frequency(x: int, y: int) -> int:
    return (4_000_000 * x) + y


def main() -> None:
    parser = generate_arg_parser()
    args = parser.parse_args()
    file_name = (
        args.filename
        if '.txt' in args.filename
        else f'{args.filename}.txt'
    )
    try:
        raw_data = read_file(CURRENT_PATH / file_name)
    except FileNotFoundError:
        print(
            f"Unable to find the file '{file_name}', "
            "check that it exists and that you spelt it correctly!"
        )
        sys.exit(1)
    coordinates = parse_coordinates(raw_data)
    # Part 1
    # intersect_row = [
    #     sensor for sensor in coordinates
    #     if abs(Y_VAL - sensor.y) < sensor.distance_from(sensor.nearest_beacon)
    # ]
    # print(f"{len(intersect_row)} intersect row {Y_VAL}")
    # beaconless_on_line = set()
    # for id, sensor in enumerate(intersect_row, 1):
    #     print(f"calculating sensor {id}")
    #     beaconless_on_line = beaconless_on_line.union(sensor.beaconless_on_line(Y_VAL))
    # print(f"{len(beaconless_on_line)} beaconless points.")

    # Part 2
    positive_lines = list()
    negative_lines = list()
    for sensor in coordinates:
        neg, pos = sensor.border_y_intercepts()
        negative_lines.extend(neg)
        positive_lines.extend(pos)
    pos = find_missing_gap(positive_lines)
    neg = find_missing_gap(negative_lines)
    if pos is not None and neg is not None:
        missing = find_gap_coordinates(pos, neg)
        print(f"Tuning frequency: {calculate_tuning_frequency(*missing)}")


if __name__ == "__main__":
    start_time = perf_counter()
    main()
    print(f"Time taken: {(perf_counter() - start_time):.2f}s")
