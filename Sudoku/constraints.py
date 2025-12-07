
def is_valid(board, row, col, value):

    # Check row constraint
    for c in range(9):
        if c != col and board[row][c] == value:
            return False
    
    # Check column constraint
    for r in range(9):
        if r != row and board[r][col] == value:
            return False
    
    # Check 3x3 box constraint
    start_r, start_c = (row // 3) * 3, (col // 3) * 3
    for r in range(start_r, start_r + 3):
        for c in range(start_c, start_c + 3):
            if (r, c) != (row, col) and board[r][c] == value:
                return False
    
    return True


def get_valid_values(board, row, col):

    valid = set(range(1, 10))
    for val in range(1, 10):
        if not is_valid(board, row, col, val):
            valid.discard(val)
    return valid
