from .heuristic import compute_heuristic
from .tree_printer import print_tree_node

P_MAIN = 0.6
P_LEFT = 0.2
P_RIGHT = 0.2

def expected_minimax_decision(board, depth):
    pass

def expected_minimax(board, depth, maximizingPlayer):
    print_tree_node(board, depth)
    pass


# 8. ai/expected_minimax.py

# Like minimax, but considers probabilities.

# expected_minimax_decision(board, depth)

# Root function.

# For each valid move:

# Simulate move with probabilities:

# 0.6 → main column

# 0.2 → left column

# 0.2 → right column

# Call expected_minimax() on resulting boards.

# Compute expected value = weighted sum.

# Return column with maximum expected value.

# expected_minimax(board, depth, maximizingPlayer)

# Recursive:

# Print tree node.

# Base case: depth == 0 or terminal → return heuristic

# For each possible move:

# Compute expected score = sum(probabilities × minimax of resulting boards)

# Return max (if AI) or min (if human).