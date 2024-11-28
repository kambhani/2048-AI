from game import Game
import numpy as np
import random

SEED = 1234
random.seed(SEED)
np.random.seed(SEED)
scores = []

def play_game(game: Game):
    while not game.game_over():
        action = random.choice(game.available_actions())
        game.do_action(action)
    game.print_state()
    print("score is: {} max tile is: {}".format(game.score(), game.max_tile()))
    return game.score()

if __name__ == '__main__':
    for i in range(10):
        game = Game(9, 3, 2, None, 0)
        scores.append(play_game(game))
    print("the mean of the score is {}".format(np.mean(scores)))