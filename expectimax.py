from game import Game
import numpy as np
import time
import math
import concurrent.futures

MAX_DEPTH = 1
spawns = [(1,1), (1,2), (2,1), (2,2)]
spawn_probs = [(0.9*0.9), (0.9*0.1), (0.9*0.1), (0.1*0.1)]

def evaluate(game: Game):
    score_weight = 0.5
    available_merges_weight = 1
    empty_tiles_weight = 10
    smoothness_weight = 4
    max_weight = 1
    return (score_weight * game.score()) + (available_merges_weight * game.num_available_merges() + (empty_tiles_weight *len(game.spawn_points())) + (max_weight * game.max_tile()) + (smoothness_weight * game.smoothness())) 

def expectimax(game: Game, depth: int, maximizing: bool):
    if depth == MAX_DEPTH or game.game_over():
        return evaluate(game)

    if maximizing:
        actions = game.available_actions()
        best_score = -float('inf')
        best_action = None
        for action in actions:
            #print(f"checking action {action}")
            game_copy = game.copy()
            game_copy.do_action(action)
            score = expectimax(game_copy, depth, False)
            if score > best_score:
                best_score = score
                best_action = action
        return best_action if depth == 0 else best_score 
    else:
        avg_score = 0
        spawn_points = game.spawn_points()
        num_spawn_points = len(spawn_points)
        
        if num_spawn_points == 0:
            return evaluate(game)

        if num_spawn_points == 1:
            sp = spawn_points[0]
            game_copy = game.copy()
            
            game_copy.set_tile_power((sp[0], sp[1]), 1)
            avg_score += expectimax(game_copy, depth + 1, True) / 2
            
            game_copy.set_tile_power((sp[0], sp[1]), 2)
            avg_score += expectimax(game_copy, depth + 1, True) / 2
            
            return avg_score

        num_pairs = num_spawn_points ** 2 - num_spawn_points
        num_outcomes = num_pairs * len(spawns)

        for i in range(num_spawn_points):
            for j in range(i + 1, num_spawn_points):
                s1, s2 = spawn_points[i], spawn_points[j]
                for k, (s1_power, s2_power) in enumerate(spawns):
                    game_copy = game.copy()
                    game_copy.set_tile_power((s1[0], s1[1]), s1_power)                
                    game_copy.set_tile_power((s2[0], s2[1]), s2_power)
                    outcome_prob = (1 / math.comb(num_spawn_points, 2)) * spawn_probs[k]
                    #avg_score += 1 / num_outcomes * expectimax(game_copy, depth + 1, True)
                    avg_score += outcome_prob * expectimax(game_copy, depth + 1, True)                 
        return avg_score


def play_game(index:int):
    game = Game(6, 3, 2)
    while not game.game_over():
        start = time.time()
        next_action = expectimax(game, 0, True)
        game.do_action(next_action)
        #print(next_action)
        end = time.time()
        #print(f"Chose action in {end-start:0.2f} seconds")
    return game.score(), game.max_tile()

if __name__ == '__main__':
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = list(executor.map(play_game, np.arange(200)))

    for result in results:
        print(f"{result[0]} {result[1]}")
    print(f"Mean score: {np.mean([result[0] for result in results])}")
    
    #start = time.time()
    #print(play_game(1))
    #end = time.time()
    #print(f"Game took {end-start:0.2f} seconds to complete")
