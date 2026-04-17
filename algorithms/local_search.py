

from __future__ import annotations

from typing import List, Tuple




def tour_cost(route: List[int], dist: List[List[float]]) -> float:
    """Total cost of a closed tour."""
    return sum(dist[route[i]][route[i + 1]] for i in range(len(route) - 1))


def two_opt(
    route: List[int],
    dist: List[List[float]],
    max_iter: int = 2000,
) -> Tuple[List[int], float]:
    
    best      = route[:]
    best_cost = tour_cost(best, dist)
    n         = len(best)
    improved  = True
    itr       = 0

    while improved and itr < max_iter:
        improved = False
        itr     += 1
        for i in range(1, n - 2):
            ri_prev = best[i - 1]
            ri      = best[i]
            for j in range(i + 1, n - 1):
                rj      = best[j]
                rj_next = best[j + 1]
                delta = (dist[ri_prev][rj] + dist[ri][rj_next]
                         - dist[ri_prev][ri] - dist[rj][rj_next])
                if delta < -1e-10:
                    best[i : j + 1] = best[i : j + 1][::-1]
                    best_cost += delta
                    ri = best[i]          
                    improved = True

    return best, best_cost



def or_opt(
    route: List[int],
    dist: List[List[float]],
    chain_lengths: Tuple[int, ...] = (1, 2, 3),
    max_iter: int = 500,
) -> Tuple[List[int], float]:
    
    best      = route[:]
    best_cost = tour_cost(best, dist)
    improved  = True
    itr       = 0

    while improved and itr < max_iter:
        improved = False
        itr     += 1
        for k in chain_lengths:
            n = len(best)
            for i in range(1, n - k - 1):         
                # Removal cost delta
                prev_i  = best[i - 1]
                chain   = best[i : i + k]
                after   = best[i + k]
                removal = (dist[prev_i][after]
                           - dist[prev_i][chain[0]]
                           - dist[chain[-1]][after])

               
                for j in range(1, n - 1):
                    if j == i - 1 or j == i + k - 1:
                        continue                    
                    if i <= j < i + k:
                        continue                   

                    prev_j  = best[j]
                    next_j  = best[j + 1] if j + 1 < n else best[0]
                    insertion = (dist[prev_j][chain[0]]
                                 + dist[chain[-1]][next_j]
                                 - dist[prev_j][next_j])
                    delta = removal + insertion

                    if delta < -1e-10:
                       
                        new_route = best[:i] + best[i + k:]
                        # Adjust j for the removed segment
                        insert_at = j if j < i else j - k + 1
                        new_route = (new_route[:insert_at]
                                     + chain
                                     + new_route[insert_at:])
                        new_cost  = best_cost + delta
                        best      = new_route
                        best_cost = new_cost
                        improved  = True
                        break              
                if improved:
                    break
            if improved:
                break

    return best, best_cost



def three_opt(
    route: List[int],
    dist: List[List[float]],
    max_iter: int = 200,
) -> Tuple[List[int], float]:
    
    def seg_cost(a: int, b: int) -> float:
        return dist[route[a]][route[b]]

    best      = route[:]
    best_cost = tour_cost(best, dist)
    n_inner   = len(best) - 1   
    improved  = True
    itr       = 0

    while improved and itr < max_iter:
        improved = False
        itr     += 1

        for i in range(1, n_inner - 2):
            for j in range(i + 1, n_inner - 1):
                for k in range(j + 1, n_inner):
                  
                    A, B = best[i - 1], best[i]
                    C, D = best[j],     best[j + 1]
                    E, F = best[k],     best[k + 1]

                    d0 = dist[A][B] + dist[C][D] + dist[E][F]

                   
                    candidates = [
                      
                        (dist[A][C] + dist[B][D] + dist[E][F],
                         best[:i] + best[i:j+1][::-1] + best[j+1:k+1] + best[k+1:]),
                        (dist[A][B] + dist[C][E] + dist[D][F],
                         best[:i] + best[i:j+1] + best[j+1:k+1][::-1] + best[k+1:]),
                        (dist[A][C] + dist[B][E] + dist[D][F],
                         best[:i] + best[i:j+1][::-1] + best[j+1:k+1][::-1] + best[k+1:]),
                        # True 3-opt
                        (dist[A][D] + dist[E][B] + dist[C][F],
                         best[:i] + best[j+1:k+1] + best[i:j+1] + best[k+1:]),
                        (dist[A][D] + dist[E][C] + dist[B][F],
                         best[:i] + best[j+1:k+1] + best[i:j+1][::-1] + best[k+1:]),
                        (dist[A][E] + dist[D][B] + dist[C][F],
                         best[:i] + best[j+1:k+1][::-1] + best[i:j+1] + best[k+1:]),
                        (dist[A][E] + dist[D][C] + dist[B][F],
                         best[:i] + best[j+1:k+1][::-1] + best[i:j+1][::-1] + best[k+1:]),
                    ]

                    best_delta = 0.0
                    best_move  = None
                    for new_d, new_route in candidates:
                        delta = new_d - d0
                        if delta < best_delta - 1e-10:
                            best_delta = delta
                            best_move  = new_route

                    if best_move is not None:
                        best      = best_move
                        best_cost += best_delta
                        improved   = True
                        break
                if improved:
                    break
            if improved:
                break

    return best, best_cost




def full_local_search(
    route: List[int],
    dist: List[List[float]],
    use_three_opt: bool = False,
) -> Tuple[List[int], float]:
    
    route, cost = two_opt(route, dist)
    route, cost = or_opt(route, dist)
    if use_three_opt:
        route, cost = three_opt(route, dist)
    return route, cost