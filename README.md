# **CS 57100 Final Project: $\mathbf{2048^3}$ - A Twist on 2048**

## **Overview**
This project explores AI strategies for a custom version of the game **2048**,
called **2048³**, featuring a larger 6x6 board, powers of 3 tiles, and double
the random tile spawn. Three algorithms were developed and evaluated:
**Random Moves** as a baseline, **Monte Carlo Tree Search (MCTS)** for
probabilistic simulations, and **Expectimax** with a heuristic evaluation.
Results showed that MCTS achieved the highest scores but with greater variance,
while Expectimax provided more consistent performance. While we explored a
specific variant of 2048, our framework allows for a generalized 2048 game, with
arbitrary board size, merge requirements, and random tile spawn. The full report
is available [here](report.pdf).

## **How to Run**
1. Clone this repository.  
   ```bash
   git clone https://github.com/kambhani/2048-AI.git
   cd 2048-AI
   ```
2. Install dependencies:
    ```bash
   pip install -r requirements.txt
   ```

3. Run the game with an AI strategy:
    ```bash
    python random_action.py
    python expectimax.py
    python mcts.py  
    ```
   
## **Customization**
- The game logic is stored in `game.py`, where the parameters `n`, `t`, and `r` control the grid size, merge size, and random tile spawn respectively. For example, setting these values to 4, 2, and 1 respectively simulates the original 2048 game. Our analysis uses the values 6, 3, and 2.
- To implement your own strategy, we recommend copying `random_action.py` and changing the `play_game` function, adding additional functions as needed.

## **Contributors**
- Anish Kambhampati
- Avi Khandelwal
- Siddharth Prabakar
- Ryan Rittner

## **License**
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
