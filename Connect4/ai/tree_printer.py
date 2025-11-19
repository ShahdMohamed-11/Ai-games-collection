def print_tree_node(board, depth):
    """Print board and depth for tracing minimax tree"""
    print(f"Depth = {depth}")
    board.print_board()
    print("---------------------")


# 5. ai/tree_printer.py

# print_tree_node(board, depth)

# Print the board state at current node.

# Print the depth (level in the minimax tree).

# Optional: print score if leaf node (heuristic).

# Used in every minimax/alphabeta/expected_minimax recursive call to visualize tree.