from ai.heuristic import compute_heuristic
from constants import AI_PLAYER, HUMAN_PLAYER


def alphabeta_decision(board, depth):
    best_col = None
    best_score = float('-inf')
    alpha = float('-inf')
    beta = float('inf')
    
    valid_moves = board.get_valid_moves()
    center = board.cols // 2
    valid_moves.sort(key=lambda x: abs(x - center))
    
    for col in valid_moves:
        new_board = board.copy()
        new_board.drop_piece(col, AI_PLAYER)
        
        score = alphabeta(new_board, depth - 1, alpha, beta, False)
        
        if score > best_score:
            best_score = score
            best_col = col
        alpha = max(alpha, best_score)
    
    return best_col


def alphabeta(board, depth, alpha, beta, maximizing):

    if board.is_full():

        ai_fours = board.count_fours(AI_PLAYER)
        human_fours = board.count_fours(HUMAN_PLAYER)
       
        return (ai_fours - human_fours) * 10000
    
    if depth == 0:
        return compute_heuristic(board)
    
    valid_moves = board.get_valid_moves()
    center = board.cols // 2
    valid_moves.sort(key=lambda x: abs(x - center))
    
    if maximizing:
        best = float('-inf')
        for col in valid_moves:
            new_board = board.copy()
            new_board.drop_piece(col, AI_PLAYER)
            score = alphabeta(new_board, depth - 1, alpha, beta, False)
            best = max(best, score)
            alpha = max(alpha, best)
            if beta <= alpha:
                break
        return best
    else:
        best = float('inf')
        for col in valid_moves:
            new_board = board.copy()
            new_board.drop_piece(col, HUMAN_PLAYER)
            score = alphabeta(new_board, depth - 1, alpha, beta, True)
            best = min(best, score)
            beta = min(beta, best)
            if beta <= alpha:
                break
        return best