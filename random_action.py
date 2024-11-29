from game import Game
import numpy as np
import random
import concurrent.futures

SEED = 1234
random.seed(SEED)
np.random.seed(SEED)

def play_game(game: Game):
    while not game.game_over():
        action = random.choice(game.available_actions())
        game.do_action(action)
    return game.score(), game.max_tile()

if __name__ == '__main__':
    with concurrent.futures.ProcessPoolExecutor() as executor:
        games = [Game(9, 3, 2) for _ in range(500)]
        results = list(executor.map(play_game, games))

    for result in results:
        print(f"{result[0]} {result[1]}")
    print(f"Mean score: {np.mean([result[0] for result in results])}")