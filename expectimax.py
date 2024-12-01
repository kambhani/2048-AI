from game import Game
import numpy as np
import time
import math
import concurrent.futures

MAX_DEPTH = 5
spawns = [(1,1), (1,2), (2,1), (2,2)]
spawn_probs = [0.81, 0.09, 0.09, 0.01]

def evaluate(game: Game):
    weights = [0.5, 1, 10, 4, 1]
    heuristics = [game.score(), game.num_available_merges(), len(game.spawn_points()), game.max_tile(), game.smoothness()]
    return sum([weight * heuristic for weight, heuristic in list(zip(weights, heuristics))])

def expectimax(game: Game, depth: int, maximizing: bool):
    if depth == MAX_DEPTH or game.game_over():
        return evaluate(game)

    if maximizing:
        actions = game.available_actions()
        best_score = -float('inf')
        best_action = None
        for action in actions:
            game_copy = game.copy()
            game_copy.do_action(action, False)
            score = expectimax(game_copy, depth, False)
            if score > best_score:
                best_score = score
                best_action = action
        return best_action if depth == 0 else best_score 
    else:
        avg_score = 0
        spawn_points = game.spawn_points()
        num_spawn_points = min(len(spawn_points), 2)

        if num_spawn_points == 1:
          sp = spawn_points[np.random.choice(spawn_points.shape[0])]
          game_copy = game.copy()
          
          game_copy.set_tile_power((sp[0], sp[1]), 1)
          avg_score += 0.9 * expectimax(game_copy, depth + 1, True)
          
          game_copy.set_tile_power((sp[0], sp[1]), 2)
          avg_score += 0.1 * expectimax(game_copy, depth + 1, True)
          
          return avg_score

        random_indices = np.random.choice(spawn_points.shape[0], size=num_spawn_points, replace=False)
        selected_spawn_points = spawn_points[random_indices]
        for i in range(num_spawn_points):
            for j in range(i + 1, num_spawn_points):
                s1, s2 = selected_spawn_points[i], selected_spawn_points[j]
                for k, (s1_power, s2_power) in enumerate(spawns):
                    game_copy = game.copy()
                    game_copy.set_tile_power((s1[0], s1[1]), s1_power)                
                    game_copy.set_tile_power((s2[0], s2[1]), s2_power)
                    outcome_prob = (1 / math.comb(num_spawn_points, 2)) * spawn_probs[k]
                    avg_score += outcome_prob * expectimax(game_copy, depth + 1, True)                 
        return avg_score

def play_game(_: int):
    game = Game(6, 3, 2)
    start = time.time()
    while not game.game_over():
        next_action = expectimax(game, 0, True)
        game.do_action(next_action)
        print(f"scored {game.score()} with max tile of {game.max_tile()}")
    end = time.time()
    print(f"Finished game in {end-start:0.2f} seconds")
    return game.score(), game.max_tile()

if __name__ == '__main__':
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = list(executor.map(play_game, np.arange(1)))

    for result in results:
        print(f"{result[0]} {result[1]}")
    print(f"Mean score: {np.mean([result[0] for result in results])}")
    
    max_tiles = np.array([result[1] for result in results])
    unique_max_tiles, counts = np.unique(max_tiles, return_counts=True)
    print(f"Most common max tile: {unique_max_tiles[np.argmax(counts)]}")
