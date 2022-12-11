from copy import deepcopy
import re
import sys
import pathlib
import argparse
from typing import List, Tuple

CURRENT_PATH = pathlib.Path.cwd()


def generate_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', default='test.txt')
    parser.add_argument('-m', '--multi_pickup', type=bool, default=False)
    return parser


def read_file(file: pathlib.Path) -> List[str]:
    if not file.exists():
        raise FileNotFoundError
    with file.open() as in_file:
        source_data = in_file.readlines()
    return [data.rstrip('\n') for data in source_data]


def split_input(data: List[str]) -> Tuple[List[List[str]], List[str]]:
    split_index = 0
    for index, line in enumerate(data):
        if line == '':
            split_index = index
            break
    return (
        [list(line) for line in data[:split_index - 1]],
        data[split_index + 1:]
    )


def convert_to_lists(crates: List[List[str]]) -> List[List[str]]:
    crate_labels = [line[1::4] for line in crates][::-1]
    crate_stacks = [list() for _ in range(len(crate_labels[0]))]
    for line in crate_labels:
        for index, crate in enumerate(line):
            if crate == ' ':
                continue
            crate_stacks[index].append(crate)
    return crate_stacks


def extract_values(instructions: List[str]) -> List[Tuple[int, int, int]]:
    instruction_values = list()
    for line in instructions:
        instruction_search = re.findall('\w+ (\d+)', line)
        instruction_values.append(
            tuple(int(value) for value in instruction_search)
        )
    return instruction_values


def convert_input(
    data: List[str]
) -> Tuple[List[List[str]], List[Tuple[int, int, int]]]:
    raw_crates, raw_instructions = split_input(data)
    crate_stacks = convert_to_lists(raw_crates)
    instructions = extract_values(raw_instructions)
    return (crate_stacks, instructions)


def apply_instructions(
    piles: List[List[str]],
    instructions: List[Tuple[int, int, int]],
    allow_multi_pickup: bool
) -> List[List[str]]:
    updated = deepcopy(piles)
    for line in instructions:
        num_moves, source, target = line
        if allow_multi_pickup:
            moving = updated[source - 1][-1 * num_moves:]
            updated[source - 1] = updated[source - 1][:-1 * num_moves]
            updated[target - 1].extend(moving)
        else:
            for _ in range(num_moves):
                moving = updated[source - 1].pop()
                updated[target - 1].append(moving)
    return updated


def main() -> None:
    parser = generate_arg_parser()
    args = parser.parse_args()
    file_name = (
        args.filename
        if '.txt' in args.filename
        else f'{args.filename}.txt'
    )
    multiple_pickup = args.multi_pickup
    try:
        raw_data = read_file(CURRENT_PATH / file_name)
    except FileNotFoundError:
        print(
            f"Unable to find the file '{file_name}', "
            "check that it exists and that you spelt it correctly!"
        )
        sys.exit(1)
    piles, instructions = convert_input(raw_data)
    updated_piles = apply_instructions(piles, instructions, multiple_pickup)
    print(
        f"The top crates are {''.join([line[-1] for line in updated_piles])}"
    )


if __name__ == "__main__":
    main()
