import sys
import pathlib
import argparse
from typing import Protocol, List, Tuple
from dataclasses import dataclass
from enum import Enum, IntEnum

CURRENT_PATH = pathlib.Path.cwd()


class Move(Protocol):
    name: str
    beats: str
    loses_to: str
    value: int


@dataclass
class Rock:
    name: str = 'rock'
    beats: str = 'scissors'
    loses_to: str = 'paper'
    value: int = 1


@dataclass
class Paper:
    name: str = 'paper'
    beats: str = 'rock'
    loses_to: str = 'scissors'
    value: int = 2


@dataclass
class Scissors:
    name: str = 'scissors'
    beats: str = 'paper'
    loses_to: str = 'rock'
    value: int = 3


class MoveChoice(Enum):
    ROCK = Rock
    PAPER = Paper
    SCISSORS = Scissors


class Result(IntEnum):
    LOSE = 0
    DRAW = 3
    WIN = 6


class PlayerOne(Enum):
    A = Rock
    B = Paper
    C = Scissors


class PlayerTwo(Enum):
    X = Result.LOSE
    Y = Result.DRAW
    Z = Result.WIN


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


def retrieve_move_list_from(file: pathlib.Path) -> List[Tuple[Move, Result]]:
    source_data = read_file(file)
    split_moves = [tuple(line.split(' ')) for line in source_data]
    return [
        (
            PlayerOne[p1_move].value,
            PlayerTwo[p2_move].value
        ) for p1_move, p2_move in split_moves
    ]


def decide_moves(
    move_list: List[Tuple[Move, Result]]
) -> List[Tuple[Move, Move]]:
    optimal_moves = list()
    for move in move_list:
        p1_move, outcome = move
        if outcome == Result.WIN:
            optimal_moves.append(
                (p1_move, MoveChoice[p1_move.loses_to.upper()].value)
            )
        elif outcome == Result.LOSE:
            optimal_moves.append(
                (p1_move, MoveChoice[p1_move.beats.upper()].value)
            )
        else:
            optimal_moves.append(
                (p1_move, p1_move)
            )
    return optimal_moves


def move_result(player_one: Move, player_two: Move) -> Result:
    if player_one.name == player_two.beats:
        return Result.WIN
    if player_one.name == player_two.loses_to:
        return Result.LOSE
    return Result.DRAW


def score_play(player_one: Move, player_two: Move) -> int:
    move_score = player_two.value
    move_score += move_result(player_one, player_two).value
    return move_score


def tally_score(move_list: List[Tuple[Move, Move]]) -> int:
    total_score = 0
    for play in move_list:
        total_score += score_play(*play)
    return total_score


def main() -> None:
    parser = generate_arg_parser()
    args = parser.parse_args()
    file_name = (
        args.filename
        if '.txt' in args.filename
        else f'{args.filename}.txt'
    )
    try:
        move_list = retrieve_move_list_from(CURRENT_PATH / file_name)
    except FileNotFoundError:
        print(
            f"Unable to find the file '{file_name}', "
            "check that it exists and that you spelt it correctly!"
        )
        sys.exit(1)
    optimal_moves = decide_moves(move_list)
    total_score = tally_score(optimal_moves)
    print(f"The final score is {total_score}")


if __name__ == "__main__":
    main()
