

from __future__ import annotations

from typing import List, Optional, Tuple


def floyd_warshall(
    n: int,
    edges: List[Tuple[int, int, float]],
    track_paths: bool = False,
) -> Tuple[List[List[float]], Optional[List[List[int]]]]:
   
    INF  = float("inf")
    dist: List[List[float]] = [[INF] * n for _ in range(n)]
    next_node: Optional[List[List[int]]] = None

    for i in range(n):
        dist[i][i] = 0.0

    for u, v, w in edges:
        w = float(w)
        if w < dist[u][v]:
            dist[u][v] = w
            dist[v][u] = w

    if track_paths:
        next_node = [[-1] * n for _ in range(n)]
        for u, v, _ in edges:
            if next_node[u][v] == -1 or dist[u][v] <= dist[u][next_node[u][v]]:
                next_node[u][v] = v
                next_node[v][u] = u
        for i in range(n):
            next_node[i][i] = i

    for k in range(n):
        for i in range(n):
            if dist[i][k] == INF:
                continue
            for j in range(n):
                via_k = dist[i][k] + dist[k][j]
                if via_k < dist[i][j]:
                    dist[i][j] = via_k
                    if track_paths and next_node is not None:
                        next_node[i][j] = next_node[i][k]

    return dist, next_node


def reconstruct_path(
    next_node: List[List[int]], src: int, dst: int
) -> List[int]:
    
    if next_node[src][dst] == -1:
        return []
    path = [src]
    while path[-1] != dst:
        path.append(next_node[path[-1]][dst])
    return path