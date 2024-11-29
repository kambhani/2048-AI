from game import Game
import numpy as np
import random
import concurrent.futures

SEED = 1234
random.seed(SEED)
np.random.seed(SEED)

def play_game(index: int):
    game = Game(9, 3, 2)
    while not game.game_over():
        action = random.choice(game.available_actions())
        game.do_action(action)
    return game.score(), game.max_tile()


if __name__ == '__main__':
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = list(executor.map(play_game, np.arange(200)))

    for result in results:
        print(f"{result[0]} {result[1]}")
    print(f"Mean score: {np.mean([result[0] for result in results])}")
