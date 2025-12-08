import copy
import time
ac3_steps_global = []
ac3_run_counter = 0 
from arc_consistency import ac3_with_tracking

def backtracking_solver_fc(board, domains, neighbors, callback=None):
    global ac3_run_counter

    empty = find_empty_mrv_fc(domains, board)
    
    if empty is None:
        return True
    
    row, col = empty
    cell = (row, col)

    for value in lcv_order(cell, domains, neighbors):
        if value in domains[cell]:

            board[row][col] = value
            saved_domains = copy.deepcopy(domains)
            domains[cell] = {value}

            if forward_check(cell, value, domains, neighbors):

                ac3_run_counter += 1 
                success, ac3_new_steps = ac3_with_tracking(domains, neighbors)
                for s in ac3_new_steps:
                    s["run"] = ac3_run_counter
                ac3_steps_global.extend(ac3_new_steps)

                if not success:
                    board[row][col] = 0
                    domains.clear()
                    domains.update(saved_domains)
                    continue

                if callback:
                    callback(board)

                if backtracking_solver_fc(board, domains, neighbors, callback):
                    return True

            # revert
            board[row][col] = 0
            domains.clear()
            domains.update(saved_domains)

    return False



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