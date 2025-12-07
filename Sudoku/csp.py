
from constraints import is_valid, get_valid_values


def build_csp(board):

    domains = {}
    neighbors = {}
    
    for r in range(9):
        for c in range(9):
            cell = (r, c)
            
            # Initialize domain
            if board[r][c] != 0:
                # Cell already has a value
                domains[cell] = {board[r][c]}
            else:
                # Cell is empty, find valid values
                domains[cell] = get_valid_values(board, r, c)
            
            # Build neighbor set (same row, column, and 3x3 box)
            neigh = set()
            
            # Same row neighbors
            for cc in range(9):
                if cc != c:
                    neigh.add((r, cc))
            
            # Same column neighbors
            for rr in range(9):
                if rr != r:
                    neigh.add((rr, c))
            
            # Same 3x3 box neighbors
            start_r, start_c = (r // 3) * 3, (c // 3) * 3
            for rr in range(start_r, start_r + 3):
                for cc in range(start_c, start_c + 3):
                    if (rr, cc) != (r, c):
                        neigh.add((rr, cc))
            
            neighbors[cell] = list(neigh)
    
    return domains, neighbors
