from ai.heuristic import compute_heuristic
from constants import AI_PLAYER, HUMAN_PLAYER
from gui.tree_visualizer import visualizer, TreeNode, start_visualization


def minimax_decision(board, depth, visualize=True):
    """
    Main entry point for minimax decision making with optional visualization.
    """
    if visualize:
        start_visualization()
        visualizer.root = None
        print(f"Starting Minimax with depth={depth}")
    
    best_col = None
    best_score = float('-inf')
    
    # Create root node
    root_node = TreeNode(col="ROOT", score=None, depth=depth, 
                        is_maximizing=True, alpha=None, beta=None)
    if visualize:
        visualizer.root = root_node
    
    valid_moves = board.get_valid_moves()
    print(f"Valid moves: {valid_moves}")
    
    for col in valid_moves:
        new_board = board.copy()
        new_board.drop_piece(col, AI_PLAYER)
        
        # Create child node for this move
        child_node = None
        if visualize:
            child_node = TreeNode(col=f"Col {col}", score=None, depth=depth-1,
                                 is_maximizing=False, alpha=None, beta=None)
            root_node.add_child(child_node)
        
        score = minimax(new_board, depth - 1, False, child_node, visualize)
        
        if child_node:
            child_node.score = score
        
        print(f"Move {col} score: {score}")
        
        if score > best_score:
            best_score = score
            best_col = col
    
    root_node.score = best_score
    print(f"Best move: {best_col} with score: {best_score}")
    
    if visualize:
        print(f"Tree has {len(root_node.children)} children")
        visualizer.update_display()
        import time
        time.sleep(1)
    
    return best_col


def minimax(board, depth, maximizing_player, parent_node=None, visualize=True):
    """
    Minimax algorithm with tree node tracking.
    """
    # Check terminal states
    if board.is_full():
        ai_fours = board.count_fours(AI_PLAYER)
        human_fours = board.count_fours(HUMAN_PLAYER)
        value = (ai_fours - human_fours) * 10000
        
        if parent_node:
            parent_node.score = value
        return value

    if depth == 0:
        value = compute_heuristic(board)
        if parent_node:
            parent_node.score = value
        return value

    valid_moves = board.get_valid_moves()

    if maximizing_player:
        best = float('-inf')
        
        for col in valid_moves:
            new_board = board.copy()
            new_board.drop_piece(col, AI_PLAYER)
            
            # Create child node
            child_node = None
            if parent_node and visualize:
                child_node = TreeNode(col=f"Col {col}", score=None, depth=depth-1,
                                     is_maximizing=True, alpha=None, beta=None)
                parent_node.add_child(child_node)
            
            val = minimax(new_board, depth - 1, False, child_node, visualize)
            
            if child_node:
                child_node.score = val
            
            best = max(best, val)
        
        if parent_node:
            parent_node.score = best
        return best
    else:
        best = float('inf')
        
        for col in valid_moves:
            new_board = board.copy()
            new_board.drop_piece(col, HUMAN_PLAYER)
            
            # Create child node
            child_node = None
            if parent_node and visualize:
                child_node = TreeNode(col=f"Col {col}", score=None, depth=depth-1,
                                     is_maximizing=False, alpha=None, beta=None)
                parent_node.add_child(child_node)
            
            val = minimax(new_board, depth - 1, True, child_node, visualize)
            
            if child_node:
                child_node.score = val
            
            best = min(best, val)
        
        if parent_node:
            parent_node.score = best
        return best