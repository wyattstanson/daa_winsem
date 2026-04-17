
from __future__ import annotations

from typing import List, Tuple


def dp_tsp_bitmask(
    dist: List[List[float]],
    nodes: List[int],
    depot: int = 0,
) -> Tuple[List[int], float]:
    
    m = len(nodes)

   
    if m == 0:
        return [depot, depot], 0.0
    if m == 1:
        c = dist[depot][nodes[0]] + dist[nodes[0]][depot]
        return [depot, nodes[0], depot], c
    if m > 20:
        raise ValueError(
            f"dp_tsp_bitmask received {m} delivery nodes (max 20). "
            "Use two_opt or or_opt for larger instances."
        )

    INF      = float("inf")
    size     = 1 << m          # number of subsets

  
    dp     = [INF] * (size * m)
    parent = [-1]  * (size * m)

    def idx(mask: int, i: int) -> int:
        return mask * m + i


    for i in range(m):
        dp[idx(1 << i, i)] = dist[depot][nodes[i]]

   
    for mask in range(1, size):
        for u in range(m):
            if not (mask & (1 << u)):
                continue
            du = dp[idx(mask, u)]
            if du == INF:
                continue
            node_u = nodes[u]
            for v in range(m):
                if mask & (1 << v):
                    continue
                new_mask  = mask | (1 << v)
                new_cost  = du + dist[node_u][nodes[v]]
                cell      = idx(new_mask, v)
                if new_cost < dp[cell]:
                    dp[cell]     = new_cost
                    parent[cell] = u

    
    full_mask  = size - 1
    best_cost  = INF
    last       = -1
    for u in range(m):
        total = dp[idx(full_mask, u)] + dist[nodes[u]][depot]
        if total < best_cost:
            best_cost = total
            last      = u

 
    route_idx: List[int] = []
    mask = full_mask
    cur  = last
    while cur != -1:
        route_idx.append(cur)
        prev_cur   = parent[idx(mask, cur)]
        mask      ^= (1 << cur)
        cur        = prev_cur
    route_idx.reverse()

    route = [depot] + [nodes[i] for i in route_idx] + [depot]
    return route, best_cost