

from __future__ import annotations

import heapq
from typing import Dict, List, Optional, Tuple


def dijkstra(
    graph: Dict[int, List[Tuple[int, float]]],
    start: int,
    n: int,
    target: Optional[int] = None,
) -> List[float]:
    
    INF  = float("inf")
    dist = [INF] * n
    dist[start] = 0.0
    heap = [(0.0, start)]        

    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:            
            continue
        if target is not None and u == target:
            break                 
        for v, w in graph[u]:
            nd = dist[u] + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))

    return dist


def dijkstra_with_path(
    graph: Dict[int, List[Tuple[int, float]]],
    start: int,
    target: int,
    n: int,
) -> Tuple[float, List[int]]:
   
    INF  = float("inf")
    dist = [INF] * n
    prev = [-1]  * n
    dist[start] = 0.0
    heap = [(0.0, start)]

    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        if u == target:
            break
        for v, w in graph[u]:
            nd = dist[u] + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(heap, (nd, v))

    if dist[target] == INF:
        return INF, []

  
    path: List[int] = []
    cur = target
    while cur != -1:
        path.append(cur)
        cur = prev[cur]
    path.reverse()
    return dist[target], path