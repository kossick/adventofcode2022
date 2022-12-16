from string import ascii_letters
import sys
import pathlib
import argparse
from typing import Dict, List, Tuple

CURRENT_PATH = pathlib.Path.cwd()


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


def get_start_end_coordinates(
    data: List[List[str]]
) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    start_point = (0, 0)
    end_point = (0, 0)
    for row_id, row in enumerate(data):
        for column_id, char in enumerate(row):
            if char == 'S':
                start_point = (column_id, row_id)
            if char == 'E':
                end_point = (column_id, row_id)
    return (start_point, end_point)


def convert_letter_to_int(character: str) -> int:
    if character == 'S':
        return 0
    elif character == 'E':
        return 25
    return list(ascii_letters).index(character)


def convert_to_heights(
    data: List[List[str]]
) -> Dict[Tuple[int, int], int]:
    return {
        (x, y): convert_letter_to_int(character)
        for y, line in enumerate(data)
        for x, character in enumerate(line)
    }


def get_valid_neighbours(
    point: Tuple[int, int],
    limits: Tuple[int, int],
    heights: Dict[Tuple[int, int], int]
) -> List[Tuple[int, int]]:
    x, y = point
    max_x, max_y = limits
    possible = (
        (x + 1, y),
        (x - 1, y),
        (x, y + 1),
        (x, y - 1)
    )
    return [
        direction for direction in possible
        if (0 <= direction[0] < max_x and 0 <= direction[1] < max_y)
        and heights[direction] - heights[point] < 2
    ]


def find_shortest_path(
    start: Tuple[int, int],
    end: Tuple[int, int],
    limits: Tuple[int, int],
    heights: Dict[Tuple[int, int], int]
) -> int:
    open: List[Tuple[int, Tuple[int, int]]] = [(0, start)]
    visited: List[Tuple[int, int]] = []
    # for _ in range(5):
    while len(open) > 0:
        step, point = open.pop(0)
        if point == end:
            return min([step for step, _ in open])
        if point in visited:
            continue
        visited.append(point)
        for neighbour in get_valid_neighbours(point, limits, heights):
            open.append((step + 1, neighbour))
    return 0


def find_shortest_total_path(
    end: Tuple[int, int],
    limits: Tuple[int, int],
    heights: Dict[Tuple[int, int], int]
) -> int:
    possible_starts = [
        point for point, height in heights.items()
        if height == 0
    ]
    path_lengths = list()
    print(f"Found {len(possible_starts)} possible starting points")
    for index, start in enumerate(possible_starts):
        print(f"Trying start {index + 1}", end='\r')
        path_lengths.append(
            find_shortest_path(
                start,
                end,
                limits,
                heights
            )
        )
    return min([length for length in path_lengths if length > 0])


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
    split_data = split_data = [list(line) for line in raw_data]
    max_x = len(split_data[0])
    max_y = len(split_data)
    start_point, end_point = get_start_end_coordinates(split_data)
    heights = convert_to_heights(split_data)
    # Part 1
    # shortest_path = find_shortest_path(
    #     start_point,
    #     end_point,
    #     (max_x, max_y),
    #     heights
    # )
    # print(f"The shortest path is {shortest_path} steps long")
    # Part 2
    shortest_path = find_shortest_total_path(
        end_point,
        (max_x, max_y),
        heights
    )
    print(f"The shortest possible path is {shortest_path}")


if __name__ == "__main__":
    main()
