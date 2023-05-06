from collections import deque
from dataclasses import dataclass
import re
import sys
import pathlib
import argparse
from typing import List, Tuple, Deque


CURRENT_PATH = pathlib.Path.cwd()
DROP_START = (500, 0)


@dataclass
class Layout:
    layout: List[Deque[str]]
    x_min: int
    x_max: int
    y_max: int


def generate_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', default='test.txt')
    parser.add_argument('-v', '--visualise', action=argparse.BooleanOptionalAction)
    return parser


def read_file(file: pathlib.Path) -> List[str]:
    if not file.exists():
        raise FileNotFoundError
    with file.open() as in_file:
        source_data = in_file.readlines()
    return [data.rstrip('\n') for data in source_data]


def retrieve_coordinates(data: List[str]) -> List[List[Tuple[int, int]]]:
    coordinates = list()
    for line in data:
        rock_path = list()
        for point in re.findall('(\d+,\d+)', line):
            rock_path.append(
                tuple([int(coordinate) for coordinate in point.split(',')])
            )
        coordinates.append(rock_path)
    return coordinates


def generate_rock_path(
    coordinates: List[Tuple[int, int]]
) -> List[Tuple[int, int]]:
    rock_path = list()
    for index, point in enumerate(coordinates[1:], 1):
        current_x, current_y = point
        previous_x, previous_y = coordinates[index - 1]
        x_diff = current_x - previous_x
        y_diff = current_y - previous_y
        if x_diff != 0:
            for inc in range(abs(x_diff)):
                updated_x = (
                    previous_x + inc if x_diff > 0 else previous_x - inc
                )
                rock_path.append((updated_x, previous_y))
        if y_diff != 0:
            for inc in range(abs(y_diff)):
                updated_y = (
                    previous_y + inc if y_diff > 0 else previous_y - inc
                )
                rock_path.append((previous_x, updated_y))
    rock_path.append(coordinates[-1])
    return rock_path


def build_initial_layout(paths: List[List[Tuple[int, int]]]) -> Layout:
    flattened = list()
    for path in paths:
        flattened.extend([point for point in path])
    flattened_x = [point[0] for point in flattened]
    flattened_y = [point[1] for point in flattened]
    flattened_x.sort(reverse=True)
    flattened_y.sort(reverse=True)
    x_max = flattened_x[0]
    x_min = flattened_x[-1]
    # y_max = flattened_y[0]  # Part 1
    y_max = flattened_y[0] + 2  # Part 2
    image = list()
    # for y in range(y_max + 1):  # Part 1
    for y in range(y_max):  # Part 2
        line = deque()
        for x in range(x_min, x_max + 1):
            line.append('#' if (x, y) in flattened else '.')
        image.append(line)
    # Part 2
    ground = deque()
    for _ in range(x_min, x_max + 1):
        ground.append('#')
    image.append(ground)
    return Layout(image, x_min, x_max, y_max)


def draw_layout(layout: Layout) -> None:
    print(*[''.join(line) for line in layout.layout], sep='\n')


def is_open(layout: Layout, position: Tuple[int, int]) -> bool:
    x, y = position
    return layout.layout[y][x - layout.x_min] not in ['#', 'o']


def extend_left(layout: Layout) -> Layout:
    layout.x_min -= 1
    for line_id, line in enumerate(layout.layout):
        line.appendleft('.' if line_id != layout.y_max else '#')
    return layout


def extend_right(layout: Layout) -> Layout:
    layout.x_max += 1
    for line_id, line in enumerate(layout.layout):
        line.append('.' if line_id != layout.y_max else '#')
    return layout


def drop_sand(layout: Layout) -> Tuple[Layout, bool]:
    if not is_open(layout, DROP_START):
        return layout, False
    sand_position = DROP_START
    floor = layout.y_max
    while True:
        x, y = sand_position
        y += 1
        if y > floor:
            return layout, False
        if is_open(layout, (x, y)):
            sand_position = (x, y)
            continue
        x -= 1
        if x < layout.x_min:
            # return layout, False  # Part 1
            layout = extend_left(layout)  # Part 2
        if is_open(layout, (x, y)):
            sand_position = (x, y)
            continue
        x += 2
        if x > layout.x_max:
            # return layout, False  # Part 1
            layout = extend_right(layout)  # Part 2
        if is_open(layout, (x, y)):
            sand_position = (x, y)
            continue
        layout.layout[sand_position[1]][sand_position[0] - layout.x_min] = 'o'
        break
    return layout, True


def main() -> None:
    parser = generate_arg_parser()
    args = parser.parse_args()
    file_name = (
        args.filename
        if '.txt' in args.filename
        else f'{args.filename}.txt'
    )
    display = args.visualise
    try:
        raw_data = read_file(CURRENT_PATH / file_name)
    except FileNotFoundError:
        print(
            f"Unable to find the file '{file_name}', "
            "check that it exists and that you spelt it correctly!"
        )
        sys.exit(1)
    coordinates = retrieve_coordinates(raw_data)
    rock_paths = [generate_rock_path(path) for path in coordinates]
    initial_layout = build_initial_layout(rock_paths)
    number_dropped = 0
    while True:
        initial_layout, keep_dropping = drop_sand(initial_layout)
        if not keep_dropping:
            break
        number_dropped += 1
    if display:
        draw_layout(initial_layout)
    print(f"Total grains of sand dropped: {number_dropped}")


if __name__ == "__main__":
    main()
