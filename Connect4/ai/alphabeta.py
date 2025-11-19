from .heuristic import compute_heuristic
from .tree_printer import print_tree_node

def alphabeta_decision(board, depth):
    pass

def alphabeta(board, depth, alpha, beta, maximizingPlayer):
    print_tree_node(board, depth)
    pass


# 7. ai/alphabeta.py

# Same as minimax, but prune branches using alpha and beta.

# alphabeta_decision(board, depth)

# Same as minimax_decision, but calls alphabeta().

# alphabeta(board, depth, alpha, beta, maximizingPlayer)

# Recursive minimax with pruning:

# If depth==0 or terminal → return heuristic

# MaximizingPlayer:

# best_score = -∞

# For each valid move:

# Recursive call

# best_score = max(best_score, score)

# alpha = max(alpha, best_score)

# if beta <= alpha → prune remaining children

# Return best_score

# MinimizingPlayer:

# best_score = +∞

# For each valid move:

# Recursive call

# best_score = min(best_score, score)

# beta = min(beta, best_score)

# if beta <= alpha → prune remaining children

# Return best_score