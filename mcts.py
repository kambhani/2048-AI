from game import Game
import numpy as np
import random
import concurrent.futures

SEED = 1234
random.seed(SEED)
np.random.seed(SEED)

def play_random_moves(game: Game):
    while not game.game_over():
        action = random.choice(game.available_actions())
        game.do_action(action)
    return game.score()

def play_game(index: int):
    game = Game(6, 3, 2)
    while not game.game_over():
        actions = game.available_actions()
        best_action = -1
        best_score = -1
        for action in actions:
            game_copy = game.copy()
            game_copy.do_action(action)
            scores = [play_random_moves(game_copy.copy()) for _ in range(30)]
            if np.mean(scores) > best_score:
                best_score = np.mean(scores)
                best_action = action
        game.do_action(best_action)

    return game.score(), game.max_tile()


if __name__ == '__main__':
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = list(executor.map(play_game, np.arange(200)))

    for result in results:
        print(f"{result[0]} {result[1]}")
    print(f"Mean score: {np.mean([result[0] for result in results])}")
