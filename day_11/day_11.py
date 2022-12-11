from __future__ import annotations
from dataclasses import dataclass
import re
import sys
import pathlib
import argparse
from typing import Callable, Dict, List

CURRENT_PATH = pathlib.Path.cwd()
RELAXATION_FACTOR = 1  # Used to swap between parts


@dataclass
class Monkey:
    identifier: int
    items: List[int]
    operation: Callable[[int], int]
    test_value: int
    throw_true: int
    throw_false: int


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


def parse_monkey(monkey_data: List[str]) -> Monkey:
    for line in monkey_data:
        id_search = re.search('Monkey (\d):', line)
        if id_search:
            id = int(id_search.group(1))
        item_search = re.search('Starting items: (\d+)', line)
        if item_search:
            items = [int(item) for item in re.findall('\d+', line)]
        operation_search = re.search(
            'Operation: new = ((\d|\w)+ [+*] (\d|\w)+)', line
        )
        if operation_search:
            operation_string = operation_search.group(1)
            operation = lambda old: eval(operation_string)
        test_search = re.search('Test: .+ (\d+)', line)
        if test_search:
            divisor = int(test_search.group(1))
        true_search = re.search('If true: .+ (\d+)', line)
        if true_search:
            true_id = int(true_search.group(1))
        false_search = re.search('If false: .+ (\d+)', line)
        if false_search:
            false_id = int(false_search.group(1))
    return Monkey(
        id,
        items,
        operation,
        divisor,
        true_id,
        false_id
    )


def add_monkeys(data: List[str]) -> List[Monkey]:
    monkey_data = list()
    monkey_list = list()
    for line in data:
        if line == "":
            monkey_list.append(parse_monkey(monkey_data))
            monkey_data = list()
            continue
        monkey_data.append(line)
    monkey_list.append(parse_monkey(monkey_data))
    return monkey_list


def get_lowest_common_denominator(monkeys: List[Monkey]) -> int:
    lcd = 1
    for monkey in monkeys:
        lcd *= monkey.test_value
    return lcd


def inspect(item: int, operation: Callable[[int], int], modulo: int) -> int:
    return (operation(item) // RELAXATION_FACTOR) % modulo


def throw(item: int, thrower: Monkey, recipient: Monkey) -> None:
    thrower.items = thrower.items[1:]
    recipient.items.append(item)


def calculate_most_inspection_product(inspection: Dict[int, int]) -> int:
    to_sort = list(inspection.values())
    to_sort.sort(reverse=True)
    return to_sort[0] * to_sort[1]


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
    monkeys = add_monkeys(raw_data)
    lcd = get_lowest_common_denominator(monkeys)
    inspection_count = {monkey.identifier: 0 for monkey in monkeys}
    for _ in range(10_000):
        for monkey in monkeys:
            count = inspection_count[monkey.identifier]
            for item in monkey.items:
                item = inspect(item, monkey.operation, lcd)
                throw_index = (
                    monkey.throw_true
                    if item % monkey.test_value == 0
                    else monkey.throw_false
                )
                throw(
                    item,
                    monkey,
                    monkeys[throw_index]
                )
                count += 1
            inspection_count.update({monkey.identifier: count})
    print(
        "The product of the two most inspecting monkeys is "
        f"{calculate_most_inspection_product(inspection_count)}"
    )


if __name__ == "__main__":
    main()
