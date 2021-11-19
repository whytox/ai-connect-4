import numpy as np
from itertools import permutations


TICTACTOE_MAP = np.array([[1, 6, 5], [8, 4, 0], [3, 2, 7]])

board = (set(), set())


def won(moves):
    return any(sum(l) == 12 for l in permutations(moves, 3))


def eval_terminal(x, o):
    if won(x):
        return 1
    if won(o):
        return -1
    return 0


def minmax(board):
    val = eval_terminal(*board)
    possible = list(set(range(9)) - board[0] - board[1])
    if val != 0 or not possible:
        return None, val
    evaluations = list()
    for ply in possible:
        _, val = minmax((board[1], board[0] | {ply}))
        evaluations.append((ply, -val))
    return max(evaluations, key=lambda k: k[1])
