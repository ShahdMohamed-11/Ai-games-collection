from .heuristic import compute_heuristic
from gui.tree_visualizer import visualizer
from constants import AI_PLAYER, HUMAN_PLAYER

def minimax_decision(board, depth):

    visualizer.clear()
    
    best_col = None
    best_score = float('-inf')
    
    # Root node
    root_id = "root"
    visualizer.add_node(root_id, None, depth, None, None, 'max')
    
    valid_moves = board.get_valid_moves()
    
    for col in valid_moves:
        new_board = board.copy()
        new_board.drop_piece(col, AI_PLAYER)
        node_id = f"move_{col}"
        visualizer.add_node(node_id, root_id, depth-1, None, col, 'min')
        
        score = minimax(new_board, depth - 1, False, parent_id=node_id)
        
        # Update node value
        visualizer.tree_data[node_id]['value'] = score
        
        if score > best_score:
            best_score = score
            best_col = col
    
    # Update root value
    visualizer.tree_data[root_id]['value'] = best_score
    
    # Generate visualization
    output_file = f"minimax_depth_{depth}"
    visualizer.generate_tree("Minimax", depth, output_file)
    
    return best_col

def minimax(board, depth, maximizingPlayer, parent_id=None):

    
    node_id = f"node_{id(board)}_{depth}_{maximizingPlayer}"
    player_type = 'max' if maximizingPlayer else 'min'
    
    # Check terminal states
    if board.is_full():
        ai_fours = board.count_fours(AI_PLAYER)
        human_fours = board.count_fours(HUMAN_PLAYER)
        value = (ai_fours - human_fours) * 10000
        visualizer.add_node(node_id, parent_id, depth, value, None, 'terminal')
        return value

    if depth == 0:
        value = compute_heuristic(board)
        visualizer.add_node(node_id, parent_id, depth, value, None, player_type)
        return value

    valid_moves = board.get_valid_moves()
    
    # Add current node
    visualizer.add_node(node_id, parent_id, depth, None, None, player_type)

    if maximizingPlayer:
        best = float('-inf')
        for col in valid_moves:
            new_board = board.copy()
            new_board.drop_piece(col, AI_PLAYER)
            val = minimax(new_board, depth - 1, False, parent_id=node_id)
            best = max(best, val)
        
        # Update node value
        visualizer.tree_data[node_id]['value'] = best
        return best
    else:
        best = float('inf')
        for col in valid_moves:
            new_board = board.copy()
            new_board.drop_piece(col, HUMAN_PLAYER)
            val = minimax(new_board, depth - 1, True, parent_id=node_id)
            best = min(best, val)
        
        # Update node value
        visualizer.tree_data[node_id]['value'] = best
        return best