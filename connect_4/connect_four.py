import numpy as np
from colorama import Fore, Style

NUM_COLUMNS = 7
COLUMN_HEIGHT = 6
FOUR = 4


class Connect4:
    def __init__(self, state=None):
        if state is not None:
            self.state = state
        else:
            self.state = state = np.zeros((NUM_COLUMNS, COLUMN_HEIGHT), dtype=np.byte)
        self.moves_history = list()
        self.player = 1 if np.sum(state != 0) % 2 == 0 else -1

    def valid_moves(self):
        """Returns columns where a disc may be played"""
        return set(
            [n for n in range(NUM_COLUMNS) if self.state[n, COLUMN_HEIGHT - 1] == 0]
        )

    def play(self, column):
        """Updates `state` as `player` drops a disc in `column`"""
        (index,) = next((i for i, v in np.ndenumerate(self.state[column]) if v == 0))
        self.state[column, index] = self.player
        self.player = -self.player
        self.moves_history.append(column)
        return

    def take_back(self):
        """Updates `state` removing top disc from last move made"""
        column = self.move_history.pop()
        (index,) = [i for i, v in np.ndenumerate(self.state[column]) if v != 0][-1]
        self.state[column, index] = 0
        return

    def four_in_a_row(self, player):
        """Checks if `player` has a 4-piece line"""
        return (
            any(
                all(self.state[c, r] == player)
                for c in range(NUM_COLUMNS)
                for r in (
                    list(range(n, n + FOUR)) for n in range(COLUMN_HEIGHT - FOUR + 1)
                )
            )
            or any(
                all(self.state[c, r] == player)
                for r in range(COLUMN_HEIGHT)
                for c in (
                    list(range(n, n + FOUR)) for n in range(NUM_COLUMNS - FOUR + 1)
                )
            )
            or any(
                np.all(self.state[diag] == player)
                for diag in (
                    (range(ro, ro + FOUR), range(co, co + FOUR))
                    for ro in range(0, NUM_COLUMNS - FOUR + 1)
                    for co in range(0, COLUMN_HEIGHT - FOUR + 1)
                )
            )
            or any(
                np.all(self.state[diag] == player)
                for diag in (
                    (range(ro, ro + FOUR), range(co + FOUR - 1, co - 1, -1))
                    for ro in range(0, NUM_COLUMNS - FOUR + 1)
                    for co in range(0, COLUMN_HEIGHT - FOUR + 1)
                )
            )
        )

    def best_move(self, moves):
        for m in moves:
            outcome = self.with_move(m)
            if outcome.winner():
                return m
        return None

    def with_move(self, move):
        """Return a new game instance where `move` has been played by the current
        player"""
        new_game = Connect4(np.copy(self.state))
        new_game.play(move)
        return new_game

    def copy(self):
        return Connect4(np.copy(self.state))

    def winner(self):
        return self.four_in_a_row(self.player)

    def __str__(self):
        return (
            str(np.flip(self.state.T, 0))
            .replace("[", " ")
            .replace("]", "")
            .replace("0", "_")
            .replace("-1", Fore.YELLOW + " O" + Style.RESET_ALL)
            .replace("1", Fore.RED + "X" + Style.RESET_ALL)
        )
