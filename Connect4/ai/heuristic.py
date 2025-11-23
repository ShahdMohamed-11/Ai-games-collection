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
    
    
    return 0


def compute_heuristic(board):

    score = 0
    rows, cols, grid = board.rows, board.cols, board.grid
    
    
    # horizontal
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