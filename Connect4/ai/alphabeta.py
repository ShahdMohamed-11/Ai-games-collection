from ai.heuristic import compute_heuristic
from constants import AI_PLAYER, HUMAN_PLAYER
from gui.tree_visualizer import visualizer


def alphabeta_decision(board, depth):

    visualizer.clear()
    
    best_col = None
    best_score = float('-inf')
    alpha = float('-inf')
    beta = float('inf')
    
    # Root node
    root_id = "root"
    visualizer.add_node(root_id, None, depth, None, None, 'max', alpha=alpha, beta=beta)
    
    valid_moves = board.get_valid_moves()
    center = board.cols // 2
    valid_moves.sort(key=lambda x: abs(x - center))
    
    for col in valid_moves:
        new_board = board.copy()
        new_board.drop_piece(col, AI_PLAYER)
        node_id = f"move_{col}"
        visualizer.add_node(node_id, root_id, depth-1, None, col, 'min', alpha=alpha, beta=beta)
        
        score = alphabeta(new_board, depth - 1, alpha, beta, False, parent_id=node_id)
        
        # Update node value
        visualizer.tree_data[node_id]['value'] = score
        
        if score > best_score:
            best_score = score
            best_col = col
        alpha = max(alpha, best_score)
        
        # Update root alpha-beta
        visualizer.tree_data[root_id]['alpha'] = alpha
        visualizer.tree_data[root_id]['beta'] = beta
    
    # Update root value
    visualizer.tree_data[root_id]['value'] = best_score
    
    # Generate visualization
    output_file = f"alphabeta_depth_{depth}"
    visualizer.generate_tree("Alpha-Beta", depth, output_file)
    
    return best_col

def alphabeta(board, depth, alpha, beta, maximizing, parent_id=None):
    
    node_id = f"node_{id(board)}_{depth}_{maximizing}"
    player_type = 'max' if maximizing else 'min'
    
    # Check terminal states
    if board.is_full():
        ai_fours = board.count_fours(AI_PLAYER)
        human_fours = board.count_fours(HUMAN_PLAYER)
        value = (ai_fours - human_fours) * 10000
        visualizer.add_node(node_id, parent_id, depth, value, None, 'terminal', 
                          alpha=alpha, beta=beta)
        return value

    if depth == 0:
        value = compute_heuristic(board)
        visualizer.add_node(node_id, parent_id, depth, value, None, player_type,
                          alpha=alpha, beta=beta)
        return value

    valid_moves = board.get_valid_moves()
    center = board.cols // 2
    valid_moves.sort(key=lambda x: abs(x - center))
    
    # Add current node
    visualizer.add_node(node_id, parent_id, depth, None, None, player_type,
                      alpha=alpha, beta=beta)
    
    if maximizing:
        best = float('-inf')
        for col in valid_moves:
            new_board = board.copy()
            new_board.drop_piece(col, AI_PLAYER)
            
            child_score = alphabeta(new_board, depth - 1, alpha, beta, False, parent_id=node_id)
            best = max(best, child_score)
            alpha = max(alpha, best)
            
            # Update current node alpha-beta
            visualizer.tree_data[node_id]['alpha'] = alpha
            visualizer.tree_data[node_id]['beta'] = beta
            
            if beta <= alpha:
                # This is a pruned branch
                pruned_id = f"pruned_{id(new_board)}_{col}"
                visualizer.add_node(pruned_id, node_id, depth-1, None, col, 'min', 
                                  is_pruned=True, alpha=alpha, beta=beta)
                break
        
        visualizer.tree_data[node_id]['value'] = best
        return best
    else:
        best = float('inf')
        for col in valid_moves:
            new_board = board.copy()
            new_board.drop_piece(col, HUMAN_PLAYER)
            
            child_score = alphabeta(new_board, depth - 1, alpha, beta, True, parent_id=node_id)
            best = min(best, child_score)
            beta = min(beta, best)
            
            # Update current node alpha-beta
            visualizer.tree_data[node_id]['alpha'] = alpha
            visualizer.tree_data[node_id]['beta'] = beta
            
            if beta <= alpha:
                # This is a pruned branch
                pruned_id = f"pruned_{id(new_board)}_{col}"
                visualizer.add_node(pruned_id, node_id, depth-1, None, col, 'max', 
                                  is_pruned=True, alpha=alpha, beta=beta)
                break
        
        visualizer.tree_data[node_id]['value'] = best
        return best