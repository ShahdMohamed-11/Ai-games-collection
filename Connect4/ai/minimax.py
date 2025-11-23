from .heuristic import compute_heuristic
# from .tree_printer import print_tree_node
from constants import AI_PLAYER, HUMAN_PLAYER

def minimax_decision(board, depth):

    best_col = None
    best_score = float('-inf')

    valid_moves = board.get_valid_moves()
    
    for col in valid_moves:
        new_board = board.copy()
        new_board.drop_piece(col, AI_PLAYER)
        score = minimax(new_board, depth - 1, False)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col


def minimax(board, depth, maximizingPlayer):

    # print_tree_node(board, depth)

    if board.is_full():
        ai_fours = board.count_fours(AI_PLAYER)
        human_fours = board.count_fours(HUMAN_PLAYER)
        return (ai_fours - human_fours) * 10000

    if depth == 0:
        return compute_heuristic(board)

    valid_moves = board.get_valid_moves()

    if maximizingPlayer:
        best = float('-inf')
        for col in valid_moves:
            new_board = board.copy()
            new_board.drop_piece(col, AI_PLAYER)
            val = minimax(new_board, depth - 1, False)
            if val > best:
                best = val
        return best
    else:
        best = float('inf')
        for col in valid_moves:
            new_board = board.copy()
            new_board.drop_piece(col, HUMAN_PLAYER)
            val = minimax(new_board, depth - 1, True)
            if val < best:
                best = val
        return best
