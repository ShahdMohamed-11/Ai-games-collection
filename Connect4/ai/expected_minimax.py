from ai.heuristic import compute_heuristic
from constants import AI_PLAYER, HUMAN_PLAYER
from gui.tree_visualizer import visualizer

P_MAIN = 0.6
P_LEFT_or_RIGHT = 0.4



def expected_minimax_decision(board, depth):
 
    visualizer.clear()

    best_col = None
    best_score = float('-inf')

    root_id = "root"
    visualizer.add_node(root_id, None, depth, None, None, 'max')

    valid_moves = board.get_valid_moves()


    for col in valid_moves:
        node_id = f"move_{col}"
        
        visualizer.add_node(node_id, root_id, depth - 1,
                            None, col, 'min')

        expected_score = compute_expected_value(
            board, col, depth, parent_id=node_id
        )

        
        visualizer.tree_data[node_id]['value'] = expected_score

        if expected_score > best_score:
            best_score = expected_score
            best_col = col

    visualizer.tree_data[root_id]['value'] = best_score
    visualizer.generate_tree("Expected-Minimax", depth, f"expected_minimax_depth_{depth}")

    return best_col


def expected_minimax(board, depth, maximizingPlayer, parent_id=None):

    node_id = f"node_{id(board)}_{depth}_{maximizingPlayer}"
    node_type = "max" if maximizingPlayer else "min"

   # Check terminal states
    if board.is_full():
        ai_fours = board.count_fours(AI_PLAYER)
        human_fours = board.count_fours(HUMAN_PLAYER)
        value = (ai_fours - human_fours) * 10000
        visualizer.add_node(node_id, parent_id, depth, value, None, 'terminal')
        return value

    if depth == 0:
        value = compute_heuristic(board)
        visualizer.add_node(node_id, parent_id, depth, value, None, node_type)
        return value


    valid_moves = board.get_valid_moves()
  
    visualizer.add_node(node_id, parent_id, depth, None, None, node_type)

    # MAX layer
    if maximizingPlayer:
        best_val = float('-inf')
        for col in valid_moves:

            expected_val = compute_expected_value(
                board, col, depth, parent_id=node_id
            )

            best_val = max(best_val, expected_val)

        visualizer.tree_data[node_id]['value'] = best_val
        return best_val

    # MIN layer
    else:
        best_val = float('inf')
        for col in valid_moves:

            new_board = board.copy()
            new_board.drop_piece(col, HUMAN_PLAYER)
            val = expected_minimax(new_board, depth - 1, False, parent_id=node_id)
            best_val = min(best_val, val)

        visualizer.tree_data[node_id]['value'] = best_val
        return best_val



def compute_expected_value(board, col, depth, parent_id):

    outcomes = []

    # MAIN drop (prob 0.6)
    new_board_main = board.copy()
    if new_board_main.drop_piece(col, AI_PLAYER):
        outcomes.append((P_MAIN, new_board_main))

    # LEFT or RIGHT
    for i in range(board.cols):
        if i == col:
            continue
        new_board = board.copy()
        if new_board.drop_piece(i, AI_PLAYER):
            outcomes.append((P_LEFT_or_RIGHT, new_board))
        
        
    # Compute weighted expected score
    total = 0
    for p, b in outcomes:
        child_id = f"p_{id(b)}_{col}_{p}"
        score = expected_minimax(b, depth - 1, False, parent_id=child_id)
        total += p * score

    return total
