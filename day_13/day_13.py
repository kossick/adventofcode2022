from ast import literal_eval
from functools import cmp_to_key
from math import prod
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


def split_into_pairs(data: List[str]) -> List[Tuple[str, str]]:
    pairs = list()
    pair = tuple()
    for line in data:
        if line == '':
            pairs.append(pair)
            pair = tuple()
            continue
        pair += (line,)
    pairs.append(pair)
    return pairs


def convert_strings(pairs: List[Tuple[str, str]]) -> List[Tuple[List, List]]:
    messages = list()
    for pair in pairs:
        message_pair = tuple()
        for string in pair:
            message_pair += (literal_eval(string),)
        messages.append(message_pair)
    return messages


def is_in_correct_order(
    left: List[int | list],
    right: List[int | list]
) -> int:
    left = [left] if isinstance(left, int) else left
    right = [right] if isinstance(right, int) else right
    for left_elem, right_elem in zip(left, right):
        if isinstance(left_elem, list) or isinstance(right_elem, list):
            result = is_in_correct_order(left_elem, right_elem)
        else:
            result = right_elem - left_elem
        if result != 0:
            return result
    return len(right) - len(left)


def find_correctly_ordered(packets: List[Tuple[List, List]]) -> List[int]:
    return [
        index for index, pair in enumerate(packets, 1)
        if is_in_correct_order(*pair) > 0
    ]


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
    string_pairs = split_into_pairs(raw_data)
    message_pairs = convert_strings(string_pairs)
    correctly_ordered_pairs = find_correctly_ordered(message_pairs)
    print(
        "The sum of the indices in the correct order "
        f"is {sum(correctly_ordered_pairs)}"
    )
    # Part 2
    packets = [
        literal_eval(line) for line in raw_data if line != ''
    ] + [[[2]], [[6]]]
    sorted_packets = sorted(
        packets,
        key=cmp_to_key(is_in_correct_order),
        reverse=True
    )
    decoder_indices = [
        n for n, packet in enumerate(sorted_packets, 1)
        if packet in ([[2]], [[6]])
    ]
    print(
        f"The decoder key is {prod(decoder_indices)}"
    )


if __name__ == "__main__":
    main()
