

from __future__ import annotations

import math
import random
from typing import Dict, List, Optional, Tuple

AdjList  = Dict[int, List[Tuple[int, float]]]
EdgeList = List[Tuple[int, int, float]]



def build_adjacency_list(edges: EdgeList, n: int) -> AdjList:
    
    graph: AdjList = {i: [] for i in range(n)}
    for u, v, w in edges:
        if w < 0:
            raise ValueError(f"Negative edge weight {w} on ({u},{v}) — "
                             "Dijkstra requires non-negative weights.")
        graph[u].append((v, float(w)))
        graph[v].append((u, float(w)))
    return graph


def build_distance_matrix(graph: AdjList, n: int) -> List[List[float]]:
   
    from algorithms.dijkstra import dijkstra   # deferred → no circular import
    return [dijkstra(graph, src, n) for src in range(n)]




def generate_random_graph(
    n: int,
    density: float = 0.5,
    max_weight: int = 50,
    seed: Optional[int] = None,
) -> EdgeList:
    
    rng = random.Random(seed)
    edges: EdgeList = []

    
    nodes = list(range(n))
    rng.shuffle(nodes)
    for i in range(n - 1):
        w = rng.randint(1, max_weight)
        edges.append((nodes[i], nodes[i + 1], w))

   
    for i in range(n):
        for j in range(i + 2, n):
            if rng.random() < density:
                w = rng.randint(1, max_weight)
                edges.append((i, j, w))

    return edges


def generate_euclidean_graph(
    n: int,
    grid: int = 100,
    seed: Optional[int] = None,
    connect_radius: Optional[float] = None,
) -> Tuple[EdgeList, List[Tuple[float, float]]]:
   
    rng = random.Random(seed)
    coords = [(rng.uniform(0, grid), rng.uniform(0, grid)) for _ in range(n)]

    def dist(a: int, b: int) -> float:
        return math.hypot(coords[a][0] - coords[b][0],
                          coords[a][1] - coords[b][1])

    radius = connect_radius or grid / 3.0
    edges: EdgeList = []
    in_tree = {0}
   
    for i in range(1, n):
        nearest = min(range(i), key=lambda j: dist(i, j))
        edges.append((i, nearest, round(dist(i, nearest), 2)))
        in_tree.add(i)

   
    for i in range(n):
        for j in range(i + 1, n):
            d = dist(i, j)
            if d <= radius:
                edges.append((i, j, round(d, 2)))

    return edges, coords



def is_connected(graph: AdjList, n: int) -> bool:
   
    if n == 0:
        return True
    visited = {0}
    queue   = [0]
    while queue:
        u = queue.pop()
        for v, _ in graph[u]:
            if v not in visited:
                visited.add(v)
                queue.append(v)
    return len(visited) == n


def validate_route(route: List[int], deliveries: List[int], depot: int) -> bool:
    
    if not route or route[0] != depot or route[-1] != depot:
        return False
    interior = route[1:-1]
    return sorted(interior) == sorted(deliveries)