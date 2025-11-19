class Board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]

    def drop_piece(self, col, player):
        """Place a piece in the given column."""
        pass

    def is_valid_column(self, col):
        """Check if move is valid."""
        pass

    def get_valid_moves(self):
        """Return list of valid columns."""
        pass

    def check_winner(self, player):
        """Check if player has connect 4."""
        pass

    def copy(self):
        """Return deep copy of board."""
        pass

    def print_board(self):
        """Print board for debugging."""
        pass

# Board class handles all board operations.

# __init__

# Create empty 2D array for rows × columns.

# drop_piece(col, player)

# Place the piece in the lowest empty row of the column.

# is_valid_column(col)

# Return True if column is not full.

# get_valid_moves()

# Return a list of all columns that are not full.

# check_winner(player)

# Check all horizontal, vertical, and diagonal sequences of 4 for the player.
# copy()

# Return a deep copy of the board (needed for simulating moves in minimax).

# print_board()

# Print the board to console (used in print_tree_node for tree visualization).
