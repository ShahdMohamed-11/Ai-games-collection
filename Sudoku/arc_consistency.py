
from collections import deque


def ac3_with_tracking(domains, neighbors):

    ac3_steps = []
    queue = deque()
    

    for Xi in domains.keys():
        for Xj in neighbors[Xi]:
            queue.append((Xi, Xj))
    
    while queue:
        Xi, Xj = queue.popleft()
        intial_domain_Xi = domains[Xi].copy()
        if revise(Xi, Xj, domains):
            ac3_steps.append({
                'arc': (Xi, Xj),
                'domain_Xi': domains[Xi].copy(),
                'initial_domain_Xi': intial_domain_Xi,
                'action': 'revised'
            })
            
 
            if len(domains[Xi]) == 0:
                return False, ac3_steps
            

            for Xk in neighbors[Xi]:
                if Xk != Xj:
                    queue.append((Xk, Xi))
    
    return True, ac3_steps


def ac3(domains, neighbors):
    
    queue = deque()

    for Xi in domains.keys():
        for Xj in neighbors[Xi]:
            queue.append((Xi, Xj))

    while queue:
        Xi, Xj = queue.popleft()
        if revise(Xi, Xj, domains):
            if len(domains[Xi]) == 0:
                return False
            for Xk in neighbors[Xi]:
                if Xk != Xj:
                    queue.append((Xk, Xi))
    return True



def revise(Xi, Xj, domains):

    revised = False
    to_remove = []
    
    for v in domains[Xi]:

        if not any(v != w for w in domains[Xj]):
            to_remove.append(v)
    

    for v in to_remove:
        domains[Xi].remove(v)
        revised = True
    
    return revised

def update_board_with_domains(board, domains):
    flag = False
    for (r, c), domain in domains.items():
        if len(domain) == 1 and board[r][c] == 0:
            board[r][c] = next(iter(domain))
            flag = True
            
    return flag
