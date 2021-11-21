from connect_4 import Connect4
from mcts import MCTS
import numpy as np

from minmax.minmax import MinMax

test_cases = [
    (
        np.array(
            [
                [1, 1, -1, 0, 0, 0],
                [-1, 1, -1, -1, 1, 0],
                [1, -1, -1, 1, -1, 1],
                [1, 1, 1, -1, 0, 0],
                [-1, -1, -1, 0, 0, 0],
                [1, 1, -1, -1, 0, 0],
                [-1, 1, 1, 0, 0, 0],
            ],
            dtype=np.int8,
        ),
        1,
    ),
    (
        np.array(
            [
                [-1, 1, -1, 0, 0, 0],
                [-1, 1, 0, 0, 0, 0],
                [1, -1, 1, -1, -1, 0],
                [1, -1, -1, 1, 0, 0],
                [-1, -1, 0, 0, 0, 0],
                [1, 1, 1, -1, 1, -1],
                [1, -1, 1, -1, 1, 1],
            ],
            dtype=np.int8,
        ),
        4,
    ),
]


def test_mcts():
    for case, expected_move in test_cases:
        game_case = Connect4(case)
        computer = MCTS(game_case, iters=10, samples=20)
        move = computer.search()
        print(
            f"For game:\n{game_case}\ncomputer move was {move} and {expected_move} was expected."
        )
    return


def test_minmax():

    for case, expected_move in test_cases:
        game_case = Connect4(case)
        computer = MinMax(game_case)
        move = computer.search()
        print(
            f"For game:\n{game_case}\ncomputer move was {move[0]} and {expected_move} was expected."
        )
    return


def main():
    test_mcts()
    test_minmax()


if __name__ == "__main__":
    main()
