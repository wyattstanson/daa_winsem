
from __future__ import annotations

import random

from core.graph          import (build_adjacency_list, build_distance_matrix,
                                  generate_random_graph, generate_euclidean_graph)
from algorithms.floyd_warshall import floyd_warshall, reconstruct_path
from agents.assignment         import assign_deliveries_to_agents
from utils.benchmark           import (benchmark_algorithms,
                                        print_complexity_table,
                                        compare_partitioning)




def demo_small() -> None:
   
    print("\n" + "═"*66)
    print("  DEMO 1 — Small City Graph  (10 nodes · 6 deliveries)")
    print("═"*66)

    n = 10
    edges = [
        (0,1,10),(0,2,15),(0,3,20),
        (1,2, 9),(1,4,12),(1,5,18),
        (2,3,11),(2,5,14),(2,6,22),
        (3,6,16),(3,7,25),
        (4,5, 8),(4,8,13),
        (5,6, 7),(5,8,19),(5,9,17),
        (6,7,10),(6,9,15),
        (7,9,12),
        (8,9, 6),
    ]
    graph = build_adjacency_list(edges, n)
    dist  = build_distance_matrix(graph, n)

    benchmark_algorithms(dist, nodes=[1,3,5,7,8,9], depot=0)
    compare_partitioning([1,3,5,7,8,9], num_agents=3, dist=dist, depot=0)


def demo_medium() -> None:
   
    print("\n" + "═"*66)
    print("  DEMO 2 — Medium Random Graph  (15 nodes · 8 deliveries)")
    print("═"*66)

    edges = generate_random_graph(n=15, density=0.4, max_weight=30, seed=42)
    graph = build_adjacency_list(edges, 15)
    dist  = build_distance_matrix(graph, 15)
    nodes = random.Random(42).sample(range(1, 15), 8)

    benchmark_algorithms(dist, nodes=nodes, depot=0)


def demo_large() -> None:

    print("\n" + "═"*66)
    print("  DEMO 3 — Large Graph  (30 nodes · 20 deliveries · 4 agents)")
    print("═"*66)

    edges = generate_random_graph(n=30, density=0.35, max_weight=40, seed=7)
    graph = build_adjacency_list(edges, 30)
    dist  = build_distance_matrix(graph, 30)
    nodes = random.Random(7).sample(range(1, 30), 20)


    benchmark_algorithms(dist, nodes=nodes, depot=0, dp_limit=0)

    print("  Multi-agent dispatch (4 agents, Clarke-Wright + local search)")
    results = assign_deliveries_to_agents(
        nodes, num_agents=4, dist=dist, depot=0,
        routing="local_search", partitioning="clarke_wright"
    )
    total = 0.0
    for aid, route, cost in results:
        print(f"  Agent {aid+1}: {route}")
        print(f"           cost = {cost:.2f}")
        total += cost
    print(f"  Total fleet cost : {total:.2f}\n")


def demo_floyd_warshall() -> None:
   
    print("\n" + "═"*66)
    print("  DEMO 4 — Floyd-Warshall  (distance matrix + path recovery)")
    print("═"*66)

    edges = [
        (0,1,10),(0,2,15),(0,3,20),
        (1,2, 9),(1,3,12),
        (2,3,10),
    ]
    n  = 4
    dist, nxt = floyd_warshall(n, edges, track_paths=True)

    print("\n  All-pairs distance matrix:")
    header = "       " + "  ".join(f"  {j}" for j in range(n))
    print(header)
    for i in range(n):
        row = "  ".join(f"{dist[i][j]:4.0f}" for j in range(n))
        print(f"    {i} │ {row}")

    if nxt:
        print("\n  Shortest paths from node 0:")
        for dst in range(1, n):
            path = reconstruct_path(nxt, 0, dst)
            print(f"    0 → {dst}  :  {' → '.join(map(str, path))}  "
                  f"(cost {dist[0][dst]:.0f})")
    print()


def demo_euclidean() -> None:

    print("\n" + "═"*66)
    print("  DEMO 5 — Euclidean City Graph  (12 nodes, coordinate-based)")
    print("═"*66)

    edges, coords = generate_euclidean_graph(n=12, grid=100, seed=21)
    graph = build_adjacency_list(edges, 12)
    dist  = build_distance_matrix(graph, 12)
    nodes = list(range(1, 12))

    print("\n  Node coordinates:")
    for i, (x, y) in enumerate(coords):
        print(f"    Node {i:2d}: ({x:5.1f}, {y:5.1f})")

    benchmark_algorithms(dist, nodes=nodes, depot=0, dp_limit=0)



if __name__ == "__main__":
    print("\n  SUDOS — Smart Urban Delivery Optimization System")
    print("     Design and Analysis of Algorithms  ·  Project Kit-01\n")

    print_complexity_table()
    demo_small()
    demo_medium()
    demo_large()
    demo_floyd_warshall()
    demo_euclidean()

    print("  All demos complete.\n")