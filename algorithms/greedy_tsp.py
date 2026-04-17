
from __future__ import annotations

from typing import List, Tuple



def greedy_tsp(
    dist: List[List[float]],
    nodes: List[int],
    depot: int = 0,
) -> Tuple[List[int], float]:
    
    if not nodes:
        return [depot, depot], 0.0

    unvisited = set(nodes)
    path      = [depot]
    cost      = 0.0
    current   = depot

    while unvisited:
    
        nxt = min(unvisited, key=lambda x: dist[current][x])
        cost     += dist[current][nxt]
        path.append(nxt)
        unvisited.remove(nxt)
        current = nxt

    cost     += dist[current][depot]
    path.append(depot)
    return path, cost



def nearest_insertion_tsp(
    dist: List[List[float]],
    nodes: List[int],
    depot: int = 0,
) -> Tuple[List[int], float]:
    
    if not nodes:
        return [depot, depot], 0.0

    
    first = min(nodes, key=lambda x: dist[depot][x])
    tour      = [depot, first, depot]
    in_tour   = {depot, first}
    remaining = set(nodes) - {first}

    while remaining:
        
        best_node = min(
            remaining,
            key=lambda u: min(dist[u][v] for v in tour[:-1])   
        )

       
        best_pos  = 1
        best_delta = float("inf")
        for i in range(len(tour) - 1):
            delta = (dist[tour[i]][best_node]
                     + dist[best_node][tour[i + 1]]
                     - dist[tour[i]][tour[i + 1]])
            if delta < best_delta:
                best_delta = delta
                best_pos   = i + 1

        tour.insert(best_pos, best_node)
        in_tour.add(best_node)
        remaining.remove(best_node)

    cost = sum(dist[tour[i]][tour[i + 1]] for i in range(len(tour) - 1))
    return tour, cost



def tour_cost(route: List[int], dist: List[List[float]]) -> float:

    return sum(dist[route[i]][route[i + 1]] for i in range(len(route) - 1))