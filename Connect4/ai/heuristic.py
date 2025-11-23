from constants import AI_PLAYER, HUMAN_PLAYER, EMPTY


def evaluate_window(window):

    ai = window.count(AI_PLAYER)
    human = window.count(HUMAN_PLAYER)
    empty = window.count(EMPTY)
    

    if ai > 0 and human > 0:
        return 0
    

    if ai == 4:
        return 1000
    if human == 4:
        return -1000
    
    #  (3 + 1 empty)
    if ai == 3 and empty == 1:
        return 100
    if human == 3 and empty == 1:
        return -100
    
    #  (2 + 2 empty)
    if ai == 2 and empty == 2:
        return 20
    if human == 2 and empty == 2:
        return -20
    
    #  (1 + 3 empty)
    if ai == 1 and empty == 3:
        return 5
    if human == 1 and empty == 3:
        return -5
    
    return 0


def compute_heuristic(board):

    score = 0
    rows, cols, grid = board.rows, board.cols, board.grid
    
    
    ai_fours = board.count_fours(AI_PLAYER)
    human_fours = board.count_fours(HUMAN_PLAYER)
    score += (ai_fours - human_fours) * 500
    
    
    center = cols // 2
    for row in range(rows):
        if grid[row][center] == AI_PLAYER:
            score += 6
        elif grid[row][center] == HUMAN_PLAYER:
            score -= 6

    for row in range(rows):
        for col in range(cols - 3):
            window = [grid[row][col + i] for i in range(4)]
            score += evaluate_window(window)
    
    # vertical
    for row in range(rows - 3):
        for col in range(cols):
            window = [grid[row + i][col] for i in range(4)]
            score += evaluate_window(window)
    
    # diagonal /
    for row in range(3, rows):
        for col in range(cols - 3):
            window = [grid[row - i][col + i] for i in range(4)]
            score += evaluate_window(window)
    
    # diagonal \
    for row in range(rows - 3):
        for col in range(cols - 3):
            window = [grid[row + i][col + i] for i in range(4)]
            score += evaluate_window(window)
    
    return score