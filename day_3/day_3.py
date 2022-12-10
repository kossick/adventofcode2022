from string import ascii_letters
import sys
import pathlib
import argparse
from typing import List

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


def find_duplicates_in(data: List[str]) -> List[str]:
    duplicates = list()
    for line in data:
        items = list(line)
        mid_point = len(items) // 2
        shared = set(items[:mid_point]).intersection(set(items[mid_point:]))
        duplicates.append(list(shared)[0])
    return duplicates


def get_badges_from(data: List[str]) -> List[str]:
    badges = list()
    number_of_groups = len(data) // 3
    for index in range(number_of_groups):
        badge = set(data[3 * index]).intersection(
            set(data[3 * index + 1]),
            set(data[3 * index + 2])
        )
        badges.append(list(badge)[0])
    return badges


def calculate_priorities_of(letters: list[str]) -> list[int]:
    return [ascii_letters.index(letter) + 1 for letter in letters]


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

    # For part 1
    # duplicate_letters = find_duplicates_in(raw_data)
    # duplicate_priorities = calculate_priorities_of(duplicate_letters)
    # print(
    #     "The duplicated letters have total priority "
    #     f"{sum(duplicate_priorities)}"
    # )

    # For part 2
    badges = get_badges_from(raw_data)
    badge_priorities = calculate_priorities_of(badges)
    print(f"The badges have a total priority of {sum(badge_priorities)}")


if __name__ == "__main__":
    main()
