from connect_4 import Connect4
from mcts import MCTS
from minmax import MinMax


def demo():
    ai = input_ai()
    game = ai.game
    turn = 0
    print("The computer is so kind to let you begin...")
    while not game.is_finished():
        print(game)
        if turn % 2 == 0:
            move = input_move(game.valid_moves())
            print(f"YOU drop a disk on column {move}")
        else:
            move = ai.search()
            print(f"AI drop a disk on column {move}")
        game.play(move)
        turn += 1
    print(game)
    if game.winner(player=-game.player):
        print(f"The winner is {'YOU' if -game.player == 1 else 'AI'}")
    else:
        print("It is a DRAW")


def input_ai():
    print("1. MinMax\n2. Monte Carlo Tree Search")
    ai = int(input("Select an AI: "))
    while ai not in (1, 2):
        ai = int(input("Input must either be 1 or 2: "))
    game = Connect4()

    if ai == 1:
        return MinMax(game)
    else:
        return MCTS(game, iters=10, samples=100)


def input_move(moves):

    user_move = int(input(f"Insert a a number in the set {moves}: "))
    while user_move not in moves:
        user_move = int(input(f"Invalid, input must one of {moves}: "))
    return user_move


if __name__ == "__main__":
    demo()
