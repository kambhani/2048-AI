from game import Game
# import numpy as np
# import concurrent.futures

MAX_DEPTH = 10
spawns = [(1,1), (1,2), (2,1), (2,2)]

def evaluate(game: Game):
    return game.score() + game.available_merges() + len(game.spawn_points())

def expectimax(game: Game, depth: int, maximizing: bool):
    if depth == MAX_DEPTH or game.game_over():
        return evaluate(game)

    if maximizing:
        actions = game.available_actions()
        best_score = -float('inf')
        best_action = None
        for action in actions:
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
        num_pairs = len(spawn_points) ** 2 - len(spawn_points)
        num_outcomes = num_pairs * len(spawns)

        for s1 in spawn_points:
            for s2 in spawn_points:
                if s1 == s2:
                    continue
                for s1_power, s2_power in spawns:
                    game_copy = game.copy()
                    game_copy.set_tile_power(s1, s1_power)                
                    game_copy.set_tile_power(s2, s2_power)
                    avg_score += 1 / num_outcomes * expectimax(game_copy, depth + 1, True)                
        return avg_score

def play_game(game: Game):
    while not game.game_over():
        next_action = expectimax(game, 0, True)
        game.do_action(next_action)
        print(next_action)
    return game.score(), game.max_tile()

if __name__ == '__main__':
    # with concurrent.futures.ProcessPoolExecutor() as executor:
    #     games = [Game(6, 3, 2) for _ in range(200)]
    #     results = list(executor.map(play_game, games))

    # for result in results:
    #     print(f"{result[0]} {result[1]}")
    # print(f"Mean score: {np.mean([result[0] for result in results])}")
    print(play_game(Game(6, 3, 2)))