from game import Game
from gui import Connect4GUI
from constants import ROWS, COLUMNS

if __name__ == "__main__":
    depth = int(input("Enter search depth K: "))
    print("Choose Algorithm: 1=minimax  2=alpha-beta  3=expected minimax")
    choice = int(input("> "))

    alg = "minimax" if choice == 1 else "alphabeta" if choice == 2 else "expected"

    game = Game(ROWS, COLUMNS, depth, alg)
    gui = Connect4GUI(game)
    gui.run()
# Start of program.

# Ask user for depth K.

# Ask user to select algorithm (minimax, alpha-beta, expected minimax).

# Create a Game object with board, depth, and algorithm.

# Create GUI object, pass the game to it.

# Start GUI main loop.