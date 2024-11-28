# This code is heavily based off of https://github.com/Shilun-Allan-Li/2048-reinforcement_learning/blob/master/game.py

import numpy as np

ACTION_NAMES = ["left", "up", "right", "down"]
ACTION_LEFT = 0
ACTION_UP = 1
ACTION_RIGHT = 2
ACTION_DOWN = 3

class Game:
    def __init__(self, n=4, t=2, r=1, state=None, initial_score=0):
        """Init the Game object.
        Args:
            n (int, optional): Size of the board. Defaults to 4.
            t (int, optional): Powers of the tiles. Defaults to 2.
            r (int, optional): Number of random tiles to place after each move. Defaults to 1.
            state: Shape (n, n) numpy array to initialize the state with. If None,
                the state will be initialized with two random tiles (as done
                in the original game).
            initial_score: Score to initialize the Game with.
        """

        self._n = n
        self._t = t
        self._r = r
        if state is None:
            self._state = np.zeros((n, n), dtype=int)
            self.add_random_tile()
            self.add_random_tile()
        else:
            self._state = state
        self._score = initial_score

    def copy(self):
        """Return a copy of self."""
        return Game(self._n, self._t, self._r, np.copy(self._state), self._score)

    def game_over(self):
        """Whether the game is over."""
        return len(self.available_actions()) == 0


    def available_actions(self):
        """Computes the set of actions that are available."""
        return [action for action in range(4) if self.is_action_available(action)]

    def is_action_available(self, action):
        """Determines whether action is available.
        That is, executing it would change the state.
        """

        temp_state = np.rot90(self._state, action)
        return self._is_action_available_left(temp_state)

    def _is_action_available_left(self, state):
        """Determines whether action 'Left' is available."""

        # True if any field is 0 (empty) on the left of a tile or if t tiles can
        # be merged.
        for row in range(self._n):
            has_empty = False
            count = 1
            for col in range(self._n):
                has_empty |= state[row, col] == 0

                # If the current tile is non-zero and there's an empty tile to its left
                if state[row, col] != 0 and has_empty:
                    return True

                # Check if the current tile is the same as the previous tile
                if col > 0 and state[row, col] == state[row, col - 1]:
                    count += 1  # Increment the count of consecutive tiles
                    if count == self._t:  # Check if the count has reached t
                        return True
                else:
                    count = 1  # Reset count if the sequence breaks

        return False

    def do_action(self, action):
        """Execute action, add a new tile, update the score & return the reward."""

        if not self.is_action_available(action):
            return 0
        temp_state = np.rot90(self._state, action)
        reward = self._do_action_left(temp_state)
        self._state = np.rot90(temp_state, -action)
        self._score += reward

        for _ in range(self._r):
            self.add_random_tile()

        return reward

    def _do_action_left(self, state):
        """Executes action 'Left'."""

        reward = 0

        for row in range(self._n):
            # Temporary storage for the row after processing
            new_row = np.zeros(self._n, dtype=int)
            current_index = 0
            sequence_count = 0
            current_value = 0

            for col in range(self._n):
                if state[row, col] == 0:
                    continue

                if state[row, col] == current_value:
                    sequence_count += 1
                    if sequence_count == self._t:
                        # Merge the tiles into a single tile
                        new_row[current_index] = current_value + 1
                        reward += self._t ** (current_value + 1)
                        current_value = 0
                        sequence_count = 0
                        current_index += 1
                else:
                    # Place the previous sequence if it didn't merge
                    for _ in range(sequence_count):
                        new_row[current_index] = current_value
                        current_index += 1

                    # Start a new sequence
                    current_value = state[row, col]
                    sequence_count = 1

            # Place the last sequence if it didn't merge
            for _ in range(sequence_count):
                new_row[current_index] = current_value
                current_index += 1

            # Update the row in the state
            state[row, :] = new_row

        return reward

    def add_random_tile(self):
        """Adds a random tile to the grid, if it is possible"""

        x_pos, y_pos = np.where(self._state == 0)
        if len(x_pos) == 0:
            return

        empty_index = np.random.choice(len(x_pos))
        value = np.random.choice([1, 2], p=[0.9, 0.1])

        self._state[x_pos[empty_index], y_pos[empty_index]] = value

    def print_state(self):
        """Prints the current state."""

        def tile_string(value):
            """Concert value to string."""
            if value > 0:
                return '% 7d' % (self._t ** value,)
            return "       "

        print("-" * (8 * self._n + 1))
        for row in range(self._n):
            print("|" + "|".join([tile_string(v) for v in self._state[row, :]]) + "|")
            print("-" * (8 * self._n + 1))

    def state(self):
        """Return current state."""
        return self._state

    def score(self):
        """Return current score."""
        return self._score

    def size(self):
        """Return size of the game."""
        return self._n

    def tile(self):
        """Return tile of the game."""
        return self._t

    def actions_available(self):
        """Return which actions are available."""
        return np.array([self.is_action_available(action) for action in range(4)])

    def max_tile(self):
        """Return maximum tile."""
        return self._t ** np.max(self._state)
