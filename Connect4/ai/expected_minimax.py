from ai.heuristic import compute_heuristic
from constants import AI_PLAYER, HUMAN_PLAYER
from gui.tree_visualizer import visualizer, TreeNode

P_MAIN = 0.6
P_LEFT_or_RIGHT = 0.4


def expected_minimax_decision(board, depth):
    """
    Main decision function using expected minimax with tree visualization
    """
    best_col = None
    best_score = float('-inf')
    
    # Create root node for the tree
    root = TreeNode(
        col=None,
        score=None,
        depth=depth,
        is_maximizing=True,
        alpha=float('-inf'),
        beta=float('inf')
    )
    visualizer.root = root
    
    valid_moves = board.get_valid_moves()
    
    for col in valid_moves:
        # Compute expected value for this move
        expected_score = compute_expected_value(
            board, col, depth, parent_node=root
        )
        
        # Create child node for this move
        move_node = TreeNode(
            col=col,
            score=expected_score,
            depth=depth,
            is_maximizing=True,
            alpha=float('-inf'),
            beta=float('inf')
        )
        root.add_child(move_node)
        
        if expected_score > best_score:
            best_score = expected_score
            best_col = col
    
    # Update root score
    root.score = best_score
    
    # Render the tree
    visualizer.update_display()
    
    return best_col


def expected_minimax(board, depth, maximizingPlayer, parent_node=None):
    """
    Expected minimax algorithm with tree visualization
    """
    # Create current node
    current_node = TreeNode(
        col=None,
        score=None,
        depth=depth,
        is_maximizing=maximizingPlayer,
        alpha=float('-inf'),
        beta=float('inf')
    )
    
    if parent_node is not None:
        parent_node.add_child(current_node)
    
    # Check terminal states
    if board.is_full():
        ai_fours = board.count_fours(AI_PLAYER)
        human_fours = board.count_fours(HUMAN_PLAYER)
        value = (ai_fours - human_fours) * 10000
        current_node.score = value
        return value
    
    if depth == 0:
        value = compute_heuristic(board)
        current_node.score = value
        return value
    
    valid_moves = board.get_valid_moves()
    
    # MAX layer
    if maximizingPlayer:
        best_val = float('-inf')
        for col in valid_moves:
            expected_val = compute_expected_value(
                board, col, depth, parent_node=current_node
            )
            best_val = max(best_val, expected_val)
        
        current_node.score = best_val
        return best_val
    
    # MIN layer
    else:
        best_val = float('inf')
        for col in valid_moves:
            new_board = board.copy()
            new_board.drop_piece(col, HUMAN_PLAYER)
            val = expected_minimax(new_board, depth - 1, True, parent_node=current_node)
            best_val = min(best_val, val)
        
        current_node.score = best_val
        return best_val


def compute_expected_value(board, col, depth, parent_node):
    """
    Compute expected value considering stochastic outcomes
    """
    # Create an expectation node
    expectation_node = TreeNode(
        col=col,
        score=None,
        depth=depth,
        is_maximizing=False,  # Chance nodes can be treated as min nodes visually
        alpha=float('-inf'),
        beta=float('inf')
    )
    
    if parent_node is not None:
        parent_node.add_child(expectation_node)
    
    outcomes = []
    
    # MAIN drop (prob 0.6)
    new_board_main = board.copy()
    if new_board_main.drop_piece(col, AI_PLAYER):
        outcomes.append((P_MAIN, new_board_main))
    
    # LEFT or RIGHT drops (prob 0.4 distributed among other columns)
    other_cols = [i for i in range(board.cols) if i != col]
    if other_cols:
        prob_per_other = P_LEFT_or_RIGHT / len(other_cols)
        for i in other_cols:
            new_board = board.copy()
            if new_board.drop_piece(i, AI_PLAYER):
                outcomes.append((prob_per_other, new_board))
    
    # Compute weighted expected score
    total = 0
    for prob, outcome_board in outcomes:
        score = expected_minimax(outcome_board, depth - 1, False, parent_node=expectation_node)
        total += prob * score
    
    expectation_node.score = total
    return total