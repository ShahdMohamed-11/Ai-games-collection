from board import Board
from ai.minimax import minimax_decision
from ai.alphabeta import alphabeta_decision
from ai.expected_minimax import expected_minimax_decision

class Game:
    def __init__(self, rows, cols, depth, algorithm):
        self.board = Board(rows, cols)
        self.depth = depth
        self.algorithm = algorithm  # "minimax", "alphabeta", "expected"

    def ai_move(self):
        """Choose and perform the AI move based on selected algorithm."""
        if self.algorithm == "minimax":
            col = minimax_decision(self.board, self.depth)
        elif self.algorithm == "alphabeta":
            col = alphabeta_decision(self.board, self.depth)
        elif self.algorithm == "expected":
            col = expected_minimax_decision(self.board, self.depth)

        self.board.drop_piece(col, 1)

    def human_move(self, col):
        """Perform human move."""
        self.board.drop_piece(col, -1)

    def is_game_over(self):
        """Check if game ended."""
        pass


# Game class controls the overall game flow.

# __init__

# Initialize a new Board object.

# Store depth K and algorithm choice.

# Initialize game state (whose turn, game over flag, etc.)

# ai_move()

# Depending on chosen algorithm:

# Call minimax_decision() OR alphabeta_decision() OR expected_minimax_decision() with current board and depth K.

# Drop AI piece in the column returned by the algorithm.

# Update board state.

# Check if AI wins after move.

# Print minimax tree (inside algorithm function).

# human_move(col)

# Drop human piece in chosen column.

# Update board state.

# Check if human wins after move.

# is_game_over()

# Check if board is full OR if either player has won.

# Return True/False.