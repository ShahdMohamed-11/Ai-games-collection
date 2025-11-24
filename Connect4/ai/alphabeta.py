from ai.heuristic import compute_heuristic
from constants import AI_PLAYER, HUMAN_PLAYER
from gui.tree_visualizer import visualizer, TreeNode, start_visualization
from ai.stats_tracker import stats


def alphabeta_decision(board, depth, visualize=True):
    """
    Main entry point for alpha-beta decision making with optional visualization.
    """
    # Reset and start tracking
    stats.reset()
    stats.start_timer()
    
    if visualize:
        start_visualization()
        visualizer.root = None
    
    best_col = None
    best_score = float('-inf')
    alpha = float('-inf')
    beta = float('inf')
    
    valid_moves = board.get_valid_moves()
    center = board.cols // 2
    valid_moves.sort(key=lambda x: abs(x - center))
    
    # Create root node
    root_node = TreeNode(col="ROOT", score=None, depth=depth, 
                        is_maximizing=True, alpha=alpha, beta=beta)
    if visualize:
        visualizer.root = root_node
    
    for col in valid_moves:
        new_board = board.copy()
        new_board.drop_piece(col, AI_PLAYER)
        
        # Create child node
        child_node = TreeNode(col=col, score=None, depth=depth-1, 
                             is_maximizing=False, alpha=alpha, beta=beta)
        root_node.add_child(child_node)
        
        score = alphabeta(new_board, depth - 1, alpha, beta, False, 
                         child_node, visualize)
        
        child_node.score = score
        
        if score > best_score:
            best_score = score
            best_col = col
        alpha = max(alpha, best_score)
        
        # Update alpha in child nodes
        child_node.alpha = alpha
    
    root_node.score = best_score
    
    # Stop tracking
    stats.stop_timer()
    
    if visualize:
        visualizer.update_display()
        # Give time for final render
        import time
        time.sleep(1)
    
    return best_col


def alphabeta(board, depth, alpha, beta, maximizing, parent_node=None, visualize=True):
    # Increment node count
    stats.increment_nodes()
    
    # Check for terminal states
    if board.is_full():
        ai_fours = board.count_fours(AI_PLAYER)
        human_fours = board.count_fours(HUMAN_PLAYER)
        score = (ai_fours - human_fours) * 10000
        
        if parent_node:
            parent_node.score = score
        return score
    
    if depth == 0:
        score = compute_heuristic(board)
        if parent_node:
            parent_node.score = score
        return score
    
    valid_moves = board.get_valid_moves()
    center = board.cols // 2
    valid_moves.sort(key=lambda x: abs(x - center))
    
    if maximizing:
        best = float('-inf')
        for i, col in enumerate(valid_moves):
            new_board = board.copy()
            new_board.drop_piece(col, AI_PLAYER)
            
            # Create child node
            child_node = None
            if parent_node and visualize:
                child_node = TreeNode(col=col, score=None, depth=depth-1, 
                                     is_maximizing=True, alpha=alpha, beta=beta)
                parent_node.add_child(child_node)
            
            score = alphabeta(new_board, depth - 1, alpha, beta, False, 
                            child_node, visualize)
            
            if child_node:
                child_node.score = score
            
            best = max(best, score)
            alpha = max(alpha, best)
            
            # Update alpha in child node
            if child_node:
                child_node.alpha = alpha
            
            # Check for pruning
            if beta <= alpha:
                # Count pruned nodes
                remaining_count = len(valid_moves) - i - 1
                stats.nodes_pruned += remaining_count
                
                # Mark remaining moves as pruned
                if parent_node and visualize:
                    for remaining_col in valid_moves[i + 1:]:
                        pruned_node = TreeNode(col=remaining_col, score="pruned", 
                                              depth=depth-1, is_maximizing=True, 
                                              alpha=alpha, beta=beta)
                        pruned_node.pruned = True
                        parent_node.add_child(pruned_node)
                break
        
        if parent_node:
            parent_node.score = best
        return best
    else:
        best = float('inf')
        for i, col in enumerate(valid_moves):
            new_board = board.copy()
            new_board.drop_piece(col, HUMAN_PLAYER)
            
            # Create child node
            child_node = None
            if parent_node and visualize:
                child_node = TreeNode(col=col, score=None, depth=depth-1, 
                                     is_maximizing=False, alpha=alpha, beta=beta)
                parent_node.add_child(child_node)
            
            score = alphabeta(new_board, depth - 1, alpha, beta, True, 
                            child_node, visualize)
            
            if child_node:
                child_node.score = score
            
            best = min(best, score)
            beta = min(beta, best)
            
            # Update beta in child node
            if child_node:
                child_node.beta = beta
            
            # Check for pruning
            if beta <= alpha:
                # Count pruned nodes
                remaining_count = len(valid_moves) - i - 1
                stats.nodes_pruned += remaining_count
                
                # Mark remaining moves as pruned
                if parent_node and visualize:
                    for remaining_col in valid_moves[i + 1:]:
                        pruned_node = TreeNode(col=remaining_col, score="pruned", 
                                              depth=depth-1, is_maximizing=False, 
                                              alpha=alpha, beta=beta)
                        pruned_node.pruned = True
                        parent_node.add_child(pruned_node)
                break
        
        if parent_node:
            parent_node.score = best
        return best