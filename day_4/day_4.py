import sys
import pathlib
import argparse
from typing import List, Tuple

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


def get_indices(line: str) -> List[Tuple[int, int]]:
    elves = line.split(',')
    first_low, first_high = [
        int(values) for values in elves[0].split('-')
    ]
    second_low, second_high = [
        int(values) for values in elves[1].split('-')
    ]
    return [
        (first_low, first_high),
        (second_low, second_high)
    ]


def find_fully_contained_pairs(data: List[str]) -> List[str]:
    fully_contained = list()
    for line in data:
        (first_low, first_high), (second_low, second_high) = get_indices(line)
        included = (
            (first_low <= second_low and first_high >= second_high)
            or (first_low >= second_low and first_high <= second_high)
        )
        if included:
            fully_contained.append(line)
    return fully_contained


def find_any_overlap(data: List[str]) -> List[str]:
    overlapping = list()
    for line in data:
        (first_low, first_high), (second_low, second_high) = get_indices(line)
        first_elf = set(range(first_low, first_high + 1))
        second_elf = set(range(second_low, second_high + 1))
        if len(first_elf.intersection(second_elf)) > 0:
            overlapping.append(line)
    return overlapping


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
    # Part 1
    # fully_contained_pairs = find_fully_contained_pairs(raw_data)
    # print(f"There are {len(fully_contained_pairs)} fully contained pairs")
    # Part 2
    overlapping = find_any_overlap(raw_data)
    print(f"There are {len(overlapping)} overlapping pairs")


if __name__ == "__main__":
    main()
