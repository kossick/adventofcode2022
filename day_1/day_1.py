import sys
import pathlib
import argparse
from typing import List

CURRENT_PATH = pathlib.Path.cwd()


def generate_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', default='test.txt')
    parser.add_argument('-n', '--number_of_top', type=int, default=1)
    return parser


def read_file(file: pathlib.Path) -> List[str]:
    if not file.exists():
        raise FileNotFoundError
    with file.open() as in_file:
        source_data = in_file.readlines()
    return [data.rstrip('\n') for data in source_data]


def assign_calories_to_elves(data: List[str]) -> List[int]:
    elves_calories = list()
    current_elf = 0
    for line in data:
        if line == '':
            elves_calories.append(current_elf)
            current_elf = 0
            continue
        current_elf += int(line)
    return elves_calories


def get_top_elves_calories(calories: List[int], top_elves: int) -> int:
    return sum(sorted(calories, reverse=True)[:top_elves])


def main() -> None:
    parser = generate_arg_parser()
    args = parser.parse_args()
    file_name = (
        args.filename
        if '.txt' in args.filename
        else f'{args.filename}.txt'
    )
    top_elves = args.number_of_top
    try:
        raw_data = read_file(CURRENT_PATH / file_name)
    except FileNotFoundError:
        print(
            f"Unable to find the file '{file_name}', "
            "check that it exists and that you spelt it correctly!"
        )
        sys.exit(1)
    elves_calories = assign_calories_to_elves(raw_data)
    top_elves_calories = get_top_elves_calories(elves_calories, top_elves)
    print(
        f"The top {top_elves} el{'f' if top_elves == 1 else 'ves'} "
        f"ha{'s' if top_elves == 1 else 've'} {top_elves_calories} calories"
    )


if __name__ == "__main__":
    main()
