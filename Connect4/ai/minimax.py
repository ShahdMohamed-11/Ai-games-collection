from .heuristic import compute_heuristic
from .tree_printer import print_tree_node

def minimax_decision(board, depth):

    """Root call: choose best move for AI."""
    pass

def minimax(board, depth, maximizingPlayer):
    """Recursive minimax."""
    print_tree_node(board, depth)  # print tree for assignment
    pass


# 6. ai/minimax.py

# Minimax algorithm without alpha-beta.

# minimax_decision(board, depth)

# Root function called from ai_move().

# For each valid column:

# Simulate dropping AI piece.

# Call minimax() on new board with depth-1 and maximizing=False.

# Store score for each column.

# Return column with maximum score.

# minimax(board, depth, maximizingPlayer)

# Recursive function.

# Print board using print_tree_node().

# Base cases:

# If depth == 0 OR board is full OR someone has won:

# Return compute_heuristic(board) score.

# If maximizingPlayer (AI):

# Initialize best_score = -∞

# For each valid move:

# Simulate move → new board

# Call minimax(new_board, depth-1, maximizing=False)

# Update best_score = max(best_score, returned_score)

# Return best_score.

# If minimizingPlayer (human):

# Initialize best_score = +∞

# For each valid move:

# Simulate move → new board

# Call minimax(new_board, depth-1, maximizing=True)

# Update best_score = min(best_score, returned_score)

# Return best_score.