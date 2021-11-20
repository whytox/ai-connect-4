import random
import numpy as np
from tqdm import tqdm
from colorama import Fore, Style

C = 1


class TSNode:
    def __init__(self, game, parent=None, action=None):
        self.game = game
        self.state = game.state
        self.action = action
        self.not_expanded_actions = game.valid_moves()  # return a set
        self.expanded_childs = list()
        self.player = game.player
        self.samples_count = 0
        self.samples_reward = 0
        self.parent = parent
        self.best_move_p = 0.5

    def has_child(self):
        return bool(self.expanded_childs)

    def is_not_fully_expanded(self):
        """Return true if I have still actions to be expanded."""
        return bool(self.not_expanded_actions)

    def is_terminal(self):
        return not bool(self.game.valid_moves())

    def expand(self):
        """Expand the current node by randomly creating a new child node
        from the set of not create children."""
        rand_move = random.choice(list(self.not_expanded_actions))
        self.not_expanded_actions.remove(rand_move)
        # create a new game
        # not very efficient
        new_game = self.game.with_move(rand_move)
        # print(new_game.player)
        new_child = TSNode(new_game, parent=self, action=rand_move)
        self.expanded_childs.append(new_child)
        return new_child

    def best_child(self):
        """Return the current node best child using the Upper Confidence Bound."""
        N_v = self.samples_count
        exploration_factor = np.sqrt(
            2 * np.log(self.samples_count) / self.childs_samples()
        )
        exploitation_factor = self.childs_estimate()
        return self.expanded_childs[np.argmax(exploitation_factor + exploration_factor)]

    def childs_estimate(self):
        return np.array([c.estimate() for c in self.expanded_childs])

    def childs_samples(self):
        return np.array([c.samples_count for c in self.expanded_childs])

    def estimate(self):
        """Return the Monte Carlo estimation of the node"""
        return self.samples_reward / self.samples_count

    def simulate(self):
        simulation = self.game.copy()
        valid = simulation.valid_moves()
        while valid:
            move = random.choice(list(valid))
            if random.random() < self.best_move_p:
                best_move = simulation.best_move(valid)
                if best_move is not None:
                    move = best_move
            simulation.play(move)
            if simulation.winner():
                return simulation.player
            valid = simulation.valid_moves()
        return 0

    def monte_carlo(self, samples=100):
        tot_outcomes = 0
        for _ in range(samples):
            tot_outcomes += self.simulate()
        return tot_outcomes, samples

    def back_prop(self, tot_outcome, samples):
        """Update parent and current nodes with the result of the simulation"""
        self.samples_reward += tot_outcome
        self.samples_count += samples
        if self.parent is not None:
            self.parent.back_prop(-tot_outcome, samples)
        return

    def __str__(self):
        return self.game.state.__str__()

    def __repr__(self):
        # TODO: improve node representation with action information
        if self.player == 1:
            color = Fore.BLUE
        else:
            color = Fore.RED
        return (
            color
            + str(self.samples_reward)
            + "/"
            + str(self.samples_count)
            + Style.RESET_ALL
        )


class MCTS:
    def __init__(self, game, iters=1000, samples=300):
        self.root = TSNode(game)
        self.iters = iters
        self.samples = samples

    def search(self):
        for _ in tqdm(range(self.iters)):
            sel_node = self.select_node()
            tot_outcome, samples = sel_node.monte_carlo(self.samples)
            sel_node.back_prop(tot_outcome, samples)
        return self.root.best_child()

    def select_node(self):
        """Add DOC"""
        curr_node = self.root
        while not curr_node.is_terminal():
            if curr_node.is_not_fully_expanded():
                return curr_node.expand()
            curr_node = curr_node.best_child()
        return curr_node

    def __str__(self, node=None, prefix=""):
        if node is None:
            node = self.root
            print(node.__repr__())
        # TODO: return a string instead of printing
        for c in node.expanded_childs[:-1]:
            connector = "├──"
            son_prefix = prefix + "|  "
            print(prefix + connector + c.__repr__())
            self.__str__(c, prefix=son_prefix)

        for c in node.expanded_childs[-1:]:
            connector = "└──"
            son_prefix = prefix + "  "
            print(prefix + connector + c.__repr__())
            self.__str__(c, prefix=son_prefix)
        return
