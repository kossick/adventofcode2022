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


def parse_line(line: str) -> Tuple[str, int]:
    line_split = line.split(' ')
    value = 0
    if len(line_split) > 1:
        value = int(line_split[1])
    command = line_split[0]
    return (command, value)


def update_signals(
    cpu_cycle: int,
    register_value: int,
    signal_strengths: List[int]
) -> List[int]:
    if (cpu_cycle - 20) % 40 == 0:
        signal_strengths.append(cpu_cycle * register_value)
    return signal_strengths


def update_crt(
    crt: list[str],
    cycle: int,
    sprite_centre: int
) -> List[str]:
    crt.append(
        '#'
        if (cycle - 1) % 40 in range(sprite_centre - 1, sprite_centre + 2)
        else '.'
    )
    return crt


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
    cpu_cycle = 1
    register_value = 1
    # Part 1
    # signal_strengths = list()
    # Part 2
    crt_display = list()
    for line in raw_data:
        command, value = parse_line(line)
        if command == 'addx':
            for _ in range(2):
                # Part 1
                # signal_strengths = update_signals(
                #     cpu_cycle,
                #     register_value,
                #     signal_strengths
                #     )
                # Part 2
                crt_display = update_crt(
                    crt_display,
                    cpu_cycle,
                    register_value
                )
                cpu_cycle += 1
            register_value += value
        else:
            # Part 1
            # signal_strengths = update_signals(
            #         cpu_cycle,
            #         register_value,
            #         signal_strengths
            #         )
            # Part 2
            crt_display = update_crt(
                crt_display,
                cpu_cycle,
                register_value
            )
            cpu_cycle += 1
    # Part 1
    # print(f"Total sum of signal strengths is {sum(signal_strengths)}")
    # Part 2
    rendered_image = [
        ''.join(crt_display[n * 40: (n + 1) * 40]) for n in range(6)
    ]
    print(*rendered_image, sep='\n')


if __name__ == "__main__":
    main()
