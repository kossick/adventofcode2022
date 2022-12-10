import sys
import pathlib
import argparse
from typing import Any, Dict, List

CURRENT_PATH = pathlib.Path.cwd()
DIR_LIMIT = 100_000


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


def get_command_indices(raw_data: List[str]) -> List[int]:
    return [
        index for index, line in enumerate(raw_data) if '$' in line
    ]


def generate_sub_tree(raw_data: List[str], starting_index: int) -> List[str]:
    sub_tree = list()
    for line in raw_data[starting_index + 1:]:
        if '$' in line:
            break
        sub_tree.append(line)
    return sub_tree


def update_directory(directory_stack: List[str], address: str) -> List[str]:
    if address == '..':
        directory_stack.pop()
    else:
        directory_stack.append(address)
    return directory_stack


def find_directory_contents(raw_data: List[str]) -> Dict[str, List[str]]:
    relative_file_tree = dict()
    directory_stack = ['/']
    command_indices = get_command_indices(raw_data)
    for index in command_indices:
        command = raw_data[index]
        if 'cd' in command:
            directory_stack = update_directory(
                directory_stack,
                command.split('cd ')[-1]
            )
        else:
            relative_file_tree[directory_stack[-1]] = generate_sub_tree(
                raw_data,
                index
            )
    return relative_file_tree


def calculate_directory_size(
    directory: str,
    directory_contents: Dict[str, List[str]]
) -> int:
    file_sizes = list()
    for element in directory_contents[directory]:
        if 'dir' in element:
            directory_name = element.split('dir ')[-1]
            file_sizes.append(calculate_directory_size(
                directory_name,
                directory_contents
            ))
        else:
            file_sizes.append(int(element.split(' ')[0]))
    return sum(file_sizes)


def find_directory_sizes(raw_data: List[str]) -> Dict[str, int]:
    directory_sizes = dict()
    directory_contents = find_directory_contents(raw_data)
    for directory in directory_contents.keys():
        directory_sizes[directory] = calculate_directory_size(
            directory,
            directory_contents
        )

    return directory_sizes


def find_directories_smaller_than(
    limit: int,
    directories: List[int]
) -> List[int]:
    return [dir for dir in directories if dir < limit]


def populate_directory(
    folder: List[str],
    directories: Dict[str, List[str]]
) -> List[Any]:
    folder_contents = list()
    for element in folder:
        if 'dir' in element:
            folder_name = element.split('dir ')[-1]
            folder_contents.append(
                populate_directory(directories[folder_name], directories)
            )
        else:
            folder_contents.append(element)
    return folder_contents


def generate_file_tree(raw_data: List[str]) -> List[Any]:
    directories = find_directory_contents(raw_data)
    return populate_directory(directories['/'], directories)


def convert_to_bytes(folder: List[str | list]) -> List[int | list]:
    byte_folder = list()
    for element in folder:
        if isinstance(element, list):
            byte_folder.append(convert_to_bytes(element))
        else:
            byte_folder.append(int(element.split(' ')[0]))
    return byte_folder


def get_folder_sizes(folders: List[Any]) -> List[int]:
    folder_sizes = list()
    folder_total = 0
    for element in folders:
        if isinstance(element, list):
            folder_size = get_folder_sizes(element)
            folder_sizes.extend(folder_size)
            folder_total += sum(folder_size)
        else:
            folder_total += element
    folder_sizes.append(folder_total)
    return folder_sizes


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
    file_tree = generate_file_tree(raw_data)
    dir_bytes = convert_to_bytes(file_tree)
    print(dir_bytes)
    folder_sizes = get_folder_sizes(dir_bytes)
    print(sorted(folder_sizes))
    under_limit = find_directories_smaller_than(DIR_LIMIT, folder_sizes)
    print(
        "The total disk space of folders under "
        f"the limit is {sum(under_limit)}"
    )


if __name__ == "__main__":
    main()
