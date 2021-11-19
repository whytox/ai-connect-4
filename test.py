from connect_4 import Connect4
from mcts import MCTS
import numpy as np

test_cases = [
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
    )
]


def main():
    for case in test_cases:
        game = Connect4(case)
        computer = MCTS(game, iters=10, samples=20)
        comp_move = computer.search()
        print(f"Board:\n{game.state.T.T}")
        print(f"Computer move:\n{comp_move}")
        print(computer)
    return


if __name__ == "__main__":
    main()
