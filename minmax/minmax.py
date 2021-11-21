from collections import Counter
import random


class MinMax:
    MAX_VAL = float("inf")
    MIN_VAL = -float("inf")

    def __init__(self, game, max_depth=4, mc_samples=100):
        self.game = game
        self.player = game.player
        self.max_depth = max_depth
        self.mc_samples = mc_samples

    def search(self, game=None, alpha=MIN_VAL, beta=MAX_VAL, depth=None):

        if game is None:
            game = self.game
        if depth is None:
            depth = self.max_depth
        elif depth == 0:
            return None, self.mc_eval(game)

        valid_moves = game.valid_moves()
        # we need to manually search mandatory moves otherwise
        # depending on the order we could have a wrong result

        winning_move = game.best_move(valid_moves)
        if winning_move is not None:
            return (winning_move, game.player)

        mandatory_move = game.best_move(valid_moves, -game.player)
        if mandatory_move is not None:
            return mandatory_move, -game.player
        val = self.MIN_VAL
        move = None
        for m in valid_moves:
            _, child_val = self.search(game.with_move(m), -beta, -alpha, depth - 1)
            val = max(val, -child_val)
            alpha = max(alpha, val)
            if alpha >= beta:
                move = m
                break
        return move, val

    def mc_eval(self, game):
        outcomes = [self.simulate(game) for _ in range(self.mc_samples)]
        stat = Counter(outcomes)
        return (stat[1] - stat[-1]) / len(stat) * game.player

    def simulate(self, game):
        valid = game.valid_moves()
        while valid:
            m = random.choice(valid)
            game.play(m)
            winner = game.winner()
            if winner is not None:
                return winner
            valid = game.valid_moves()
        return 0
