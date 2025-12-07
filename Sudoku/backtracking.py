import copy
from collections import deque
from arc_consistency import ac3


def backtracking_solver_fc(board, domains, neighbors, callback=None):

    empty = find_empty_mrv_fc(domains, board)
    if empty is None:
        return True  

    row, col = empty
    cell = (row, col)

    for value in lcv_order(cell, domains, neighbors):
        if value not in domains[cell]:
            continue

        # Save state
        saved_domains = copy.deepcopy(domains)
        saved_board = copy.deepcopy(board)


        board[row][col] = value
        domains[cell] = {value}

        # Forward checking
        fc_ok = forward_check(cell, value, domains, neighbors)
        if not fc_ok:
            # undo and continue
            board[row][col] = 0
            domains.clear(); domains.update(saved_domains)
            continue

        # Re-run arc consistency after the assignment
        ac3_ok = ac3(domains, neighbors)
        if not ac3_ok:
            # assignment leads to inconsistency -> undo and continue
            board[row][col] = 0
            domains.clear(); domains.update(saved_domains)
            continue

        if callback:

            test_board = copy.deepcopy(board)
            test_domains = copy.deepcopy(domains)
            solvable = backtracking_solver_fc(test_board, test_domains, neighbors, callback=None)
            if solvable:
                callback(board)
                return True
            else:
                # Undo and try next value
                board[row][col] = 0
                domains.clear(); domains.update(saved_domains)
                continue
        else:

            if backtracking_solver_fc(board, domains, neighbors, callback=None):
                return True
            # undo and try next value
            board[row][col] = 0
            domains.clear(); domains.update(saved_domains)
            
            



def find_empty_mrv_fc(domains, board):

    min_len = 10
    best_cell = None
    
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                n = len(domains[(r, c)])
                if n < min_len:
                    min_len = n
                    best_cell = (r, c)
    
    return best_cell


def lcv_order(cell, domains, neighbors):

    counts = []
    
    for val in domains[cell]:

        count = sum(1 for neigh in neighbors[cell] if val in domains[neigh])
        counts.append((count, val))
    
    counts.sort()
    return [v for _, v in counts]



def forward_check(cell, value, domains, neighbors):

    for neigh in neighbors[cell]:
        if value in domains[neigh]:
            domains[neigh].remove(value)
            
            if len(domains[neigh]) == 0:
                return False
    
    return True


def is_complete(board):

    return all(board[r][c] != 0 for r in range(9) for c in range(9))