from __future__ import annotations
import argparse
from dataclasses import dataclass
import pathlib
import re
import sys
from time import perf_counter
from typing import List, Self, Set

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





        # border = self.beaconless_border()
        # on_line = sorted([point for point in border if point.y == row], key=lambda p: p.x)
        # if len(on_line) == 1 and on_line == self.nearest_beacon:
        #     return []
        # if len(on_line) == 2:
        #     left, right = on_line
        #     if left == self.nearest_beacon:
        #         # Shift right
        #         on_line[0] = Point(left.x + 1, row)
        #     elif right == self.nearest_beacon:
        #         # Shift left
        #         on_line[1] = Point(right.x - 1, row)

        # return on_line

    # def without_beacons(self: Self) -> Set[Point]:
    #     """Find all points around a sensor with a distance less than or equal to the distance of the nearest beacon

    #     Makes sure to not include the location of the beacon as well"""
    #     beaconless = set()
    #     beacon_distance = self.distance_from(self.nearest_beacon)
    #     for x in range(beacon_distance + 1):
    #         for y in range(beacon_distance + 1 - x):
    #             neighbours = (
    #                 Point(self.x + x, self.y + y),
    #                 Point(self.x + x, self.y - y),
    #                 Point(self.x - x, self.y + y),
    #                 Point(self.x - x, self.y - y),
    #             )
    #             for point in neighbours:
    #                 if point != self and point != self.nearest_beacon:
    #                     beaconless.add(point)
    #     return beaconless


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
    intersect_row = [
        sensor for sensor in coordinates
        if abs(Y_VAL - sensor.y) < sensor.distance_from(sensor.nearest_beacon)
    ]
    print(f"{len(intersect_row)} intersect row {Y_VAL}")
    beaconless_on_line = set()
    for id, sensor in enumerate(intersect_row, 1):
        print(f"calculating sensor {id}")
        beaconless_on_line = beaconless_on_line.union(sensor.beaconless_on_line(Y_VAL))
    print(f"{len(beaconless_on_line)} beaconless points.")
    

    # beaconless = set()
    # for sensor in coordinates:
    #     beaconless = beaconless.union(sensor.beaconless_border())
    # print(len(beaconless))
    # exclude_sensors = [point for point in beaconless if point not in coordinates]
    # print(len(exclude_sensors))
    # print([point for point in exclude_sensors if point.y == 10])


    # print(f"{sensor}, distance: {sensor.distance_from(sensor.nearest_beacon)}")
    # print(sensor.beaconless_border())
    # beaconless: Set[Point] = set()
    # print(f"analysed 0/{len(coordinates)}", end='')
    # for id, sensor in enumerate(coordinates, 1):
    #     beaconless = beaconless.union(sensor.without_beacons())
    #     print(f"\banalysed {id}/{len(coordinates)}", end='')
    # exclude_sensors = [point for point in beaconless if point not in coordinates]
    # fixed_y = [point for point in exclude_sensors if point.y == Y_VAL]
    # print(f"Number of beaconless points in row y={Y_VAL} is {len(fixed_y)}")


if __name__ == "__main__":
    start_time = perf_counter()
    main()
    print(f"Time taken: {(perf_counter() - start_time):.2f}s")
