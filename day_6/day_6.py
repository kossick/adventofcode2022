import sys
import pathlib
import argparse
from typing import List

CURRENT_PATH = pathlib.Path.cwd()


def generate_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', default='test.txt')
    parser.add_argument('-l', '--marker_length', type=int, default=4)
    return parser


def read_file(file: pathlib.Path) -> List[str]:
    if not file.exists():
        raise FileNotFoundError
    with file.open() as in_file:
        source_data = in_file.readlines()
    return [data.rstrip('\n') for data in source_data]


def contains_different_characters(submessage: List[str]) -> bool:
    return len(set(submessage)) == len(submessage)


def find_message_start(data: List[str], length: int) -> int | None:
    for index, _ in enumerate(data):
        if contains_different_characters(data[index: index + length]):
            return index + length


def main() -> None:
    parser = generate_arg_parser()
    args = parser.parse_args()
    file_name = (
        args.filename
        if '.txt' in args.filename
        else f'{args.filename}.txt'
    )
    marker_length = args.marker_length
    try:
        raw_data = read_file(CURRENT_PATH / file_name)
    except FileNotFoundError:
        print(
            f"Unable to find the file '{file_name}', "
            "check that it exists and that you spelt it correctly!"
        )
        sys.exit(1)
    for line in raw_data:
        message_start = find_message_start(list(line), marker_length)
        print(f"The message starts after character {message_start}")


if __name__ == "__main__":
    main()
