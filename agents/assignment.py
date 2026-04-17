
from __future__ import annotations

from typing import List, Optional, Tuple

from algorithms.greedy_tsp   import greedy_tsp, nearest_insertion_tsp
from algorithms.dp_tsp       import dp_tsp_bitmask
from algorithms.local_search import full_local_search, two_opt


VALID_ALGORITHMS    = {"greedy", "insertion", "dp", "local_search"}
VALID_PARTITIONING  = {"round_robin", "clarke_wright"}




def _round_robin(deliveries: List[int], k: int) -> List[List[int]]:
    
    buckets: List[List[int]] = [[] for _ in range(k)]
    for idx, node in enumerate(deliveries):
        buckets[idx % k].append(node)
    return buckets


def _clarke_wright(
    deliveries: List[int],
    k: int,
    dist: List[List[float]],
    depot: int,
) -> List[List[int]]:
    
    if len(deliveries) <= k:
        buckets = [[d] for d in deliveries]
        while len(buckets) < k:
            buckets.append([])
        return buckets


    routes: List[List[int]] = [[d] for d in deliveries]

    savings: List[Tuple[float, int, int]] = []
    n = len(deliveries)
    for i in range(n):
        for j in range(i + 1, n):
            s = (dist[depot][deliveries[i]]
                 + dist[depot][deliveries[j]]
                 - dist[deliveries[i]][deliveries[j]])
            savings.append((s, i, j))
    savings.sort(reverse=True)

   
    node_to_route = {d: idx for idx, d in enumerate(deliveries)}

    merged = True
    while merged and len(routes) > k:
        merged = False
        for s, i, j in savings:
            if s <= 0:
                break
            ri = node_to_route.get(deliveries[i])
            rj = node_to_route.get(deliveries[j])
            if ri is None or rj is None or ri == rj:
                continue

            route_a = routes[ri]
            route_b = routes[rj]

           
            merged_route: Optional[List[int]] = None
            if route_a[-1] == deliveries[i] and route_b[0] == deliveries[j]:
                merged_route = route_a + route_b
            elif route_a[0] == deliveries[i] and route_b[-1] == deliveries[j]:
                merged_route = route_b + route_a
            elif route_a[-1] == deliveries[i] and route_b[-1] == deliveries[j]:
                merged_route = route_a + route_b[::-1]
            elif route_a[0] == deliveries[i] and route_b[0] == deliveries[j]:
                merged_route = route_a[::-1] + route_b

            if merged_route is not None:
               
                routes[ri] = merged_route
                routes[rj] = []             
                for node in merged_route:
                    node_to_route[node] = ri
                merged = True
                break

    routes = [r for r in routes if r]
    while len(routes) < k:
        routes.append([])
   
    while len(routes) > k:
        routes.sort(key=len, reverse=True)
        largest = routes.pop(0)
        mid = len(largest) // 2
        routes.append(largest[:mid])
        routes.append(largest[mid:])

    return routes[:k]




def _route_agent(
    nodes: List[int],
    dist: List[List[float]],
    depot: int,
    algorithm: str,
) -> Tuple[List[int], float]:
    
    if not nodes:
        return [depot, depot], 0.0

    if algorithm == "dp":
        if len(nodes) > 15:
            # Safety fallback for large sub-sets
            route, cost = nearest_insertion_tsp(dist, nodes, depot)
            route, cost = full_local_search(route, dist)
        else:
            route, cost = dp_tsp_bitmask(dist, nodes, depot)

    elif algorithm == "local_search":
        route, cost = nearest_insertion_tsp(dist, nodes, depot)
        route, cost = full_local_search(route, dist)

    elif algorithm == "insertion":
        route, cost = nearest_insertion_tsp(dist, nodes, depot)

    else:  # greedy (default)
        route, cost = greedy_tsp(dist, nodes, depot)

    return route, cost


def assign_deliveries_to_agents(
    deliveries: List[int],
    num_agents: int,
    dist: List[List[float]],
    depot: int = 0,
    routing: str = "local_search",
    partitioning: str = "clarke_wright",
) -> List[Tuple[int, List[int], float]]:
    
    if routing not in VALID_ALGORITHMS:
        raise ValueError(f"routing must be one of {VALID_ALGORITHMS}")
    if partitioning not in VALID_PARTITIONING:
        raise ValueError(f"partitioning must be one of {VALID_PARTITIONING}")

    if partitioning == "clarke_wright":
        buckets = _clarke_wright(deliveries, num_agents, dist, depot)
    else:
        buckets = _round_robin(deliveries, num_agents)

    results: List[Tuple[int, List[int], float]] = []
    for agent_id, nodes in enumerate(buckets):
        route, cost = _route_agent(nodes, dist, depot, routing)
        results.append((agent_id, route, cost))

    return results