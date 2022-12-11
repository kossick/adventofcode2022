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


def is_visible(
    tree: int,
    column_id: int,
    row_id: int,
    trees: List[List[int]]
) -> bool:
    upper_column = [row[column_id] for row in trees[row_id - 1:: -1]]
    lower_column = [row[column_id] for row in trees[row_id + 1:]]
    return any([
        all(tree > other for other in trees[row_id][column_id - 1:: -1]),
        all(tree > other for other in trees[row_id][column_id + 1:]),
        all(tree > other for other in upper_column),
        all(tree > other for other in lower_column)
    ])


def find_all_visible_trees(trees: List[List[int]]) -> int:
    count = 4 * (len(trees[0]) - 1)  # account for trees on perimeter
    inner_trees = [[tree for tree in line[1: -1]] for line in trees[1: -1]]
    for row_id, row in enumerate(inner_trees):
        for column_id, tree in enumerate(row):
            if is_visible(tree, column_id + 1, row_id + 1, trees):
                count += 1
    return count


def calculate_scenic_score(
    tree: int,
    row_id: int,
    column_id: int,
    trees: List[List[int]]
) -> int:
    scenic_score = 1
    upper_column = [row[column_id] for row in trees[row_id - 1::-1]]
    lower_column = [row[column_id] for row in trees[row_id + 1:]]
    left_row = trees[row_id][column_id - 1:: -1]
    right_row = trees[row_id][column_id + 1:]
    for iterable in (upper_column, lower_column, left_row, right_row):
        visible = list()
        for other in iterable:
            visible.append(other)
            if tree <= other:
                break
        scenic_score *= len(visible)
    return scenic_score


def get_scenic_scores(trees: List[List[int]]) -> List[int]:
    # All trees on perimeter have a scenic score of 0 so ignore them
    inner_trees = [[tree for tree in line[1: -1]] for line in trees[1: -1]]
    scenic_scores = list()
    for row_id, row in enumerate(inner_trees):
        for column_id, tree in enumerate(row):
            scenic_scores.append(
                calculate_scenic_score(tree, row_id + 1, column_id + 1, trees)
            )
    return scenic_scores


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
    trees = [
        [int(tree) for tree in list(line)] for line in raw_data
    ]
    # Part 1
    number_visible_trees = find_all_visible_trees(trees)
    print(f"There are {number_visible_trees} trees visible from the outside")
    # Part 2
    scenic_scores = get_scenic_scores(trees)
    print(f"The largest scenic score is {max(scenic_scores)}")


if __name__ == "__main__":
    main()
