

from __future__ import annotations

import time
from typing import Dict, List, Tuple

from algorithms.greedy_tsp   import greedy_tsp, nearest_insertion_tsp
from algorithms.dp_tsp       import dp_tsp_bitmask
from algorithms.local_search import two_opt, or_opt, full_local_search
from agents.assignment       import assign_deliveries_to_agents





def _pct(a: float, b: float) -> str:
    if b == 0:
        return "N/A"
    return f"{((a - b) / b) * 100:+.2f}%"

def _ms(t: float) -> str:
    return f"{t * 1000:.4f} ms"

SEP  = "═" * 66
SEP2 = "─" * 66




AlgoResult = Tuple[List[int], float, float] 


def benchmark_algorithms(
    dist: List[List[float]],
    nodes: List[int],
    depot: int = 0,
    dp_limit: int = 15,
) -> Dict[str, AlgoResult]:
    
    results: Dict[str, AlgoResult] = {}

    print(f"\n{SEP}")
    print("  SUDOS — Algorithm Comparison Report")
    print(SEP)
    print(f"  Deliveries ({len(nodes)}) : {nodes}")
    print(f"  Depot                : {depot}")
    print(SEP)


    t0 = time.perf_counter()
    g_route, g_cost = greedy_tsp(dist, nodes, depot)
    g_time = time.perf_counter() - t0
    results["Greedy NN"] = (g_route, g_cost, g_time)
    print(f"\n[1] Greedy Nearest-Neighbour           O(n²)")
    print(f"    Cost : {g_cost:>10.2f}   Time : {_ms(g_time)}")
    print(f"    Route: {g_route}")

   
    t0 = time.perf_counter()
    ni_route, ni_cost = nearest_insertion_tsp(dist, nodes, depot)
    ni_time = time.perf_counter() - t0
    results["Nearest Insertion"] = (ni_route, ni_cost, ni_time)
    print(f"\n[2] Nearest-Insertion                  O(n²)")
    print(f"    Cost : {ni_cost:>10.2f}   Time : {_ms(ni_time)}")
    print(f"    vs Greedy NN : {_pct(ni_cost, g_cost)}")
    print(f"    Route: {ni_route}")

  
    t0 = time.perf_counter()
    o2_route, o2_cost = two_opt(g_route[:], dist)
    o2_time = time.perf_counter() - t0
    results["2-Opt"] = (o2_route, o2_cost, o2_time)
    print(f"\n[3] 2-Opt (seeded from NN)             O(n²/pass)")
    print(f"    Cost : {o2_cost:>10.2f}   Time : {_ms(o2_time)}")
    print(f"    vs Greedy NN : {_pct(o2_cost, g_cost)}")
    print(f"    Route: {o2_route}")

    
    t0 = time.perf_counter()
    oo_route, oo_cost = or_opt(o2_route[:], dist)
    oo_time = time.perf_counter() - t0
    results["Or-Opt"] = (oo_route, oo_cost, oo_time)
    print(f"\n[4] Or-Opt (k=1,2,3, after 2-opt)     O(n²/pass)")
    print(f"    Cost : {oo_cost:>10.2f}   Time : {_ms(oo_time)}")
    print(f"    vs 2-Opt     : {_pct(oo_cost, o2_cost)}")
    print(f"    Route: {oo_route}")

    
    t0 = time.perf_counter()
    fl_route, fl_cost = full_local_search(ni_route[:], dist)
    fl_time = time.perf_counter() - t0
    results["Full Local Search"] = (fl_route, fl_cost, fl_time)
    print(f"\n[5] Full Local Search (ins→2opt→oropt)")
    print(f"    Cost : {fl_cost:>10.2f}   Time : {_ms(fl_time)}")
    print(f"    vs Greedy NN : {_pct(fl_cost, g_cost)}")
    print(f"    Route: {fl_route}")

   
    if len(nodes) <= dp_limit:
        t0 = time.perf_counter()
        dp_route, dp_cost = dp_tsp_bitmask(dist, nodes, depot)
        dp_time = time.perf_counter() - t0
        results["DP-TSP (Exact)"] = (dp_route, dp_cost, dp_time)
        print(f"\n[6] DP-TSP / Held-Karp (EXACT)         O(2ⁿ·n²)")
        print(f"    Cost : {dp_cost:>10.2f}   Time : {_ms(dp_time)}")
        print(f"    Route: {dp_route}")
        print(f"\n  ── Optimality Gaps vs Exact ──")
        for name, (_, c, _) in results.items():
            if name != "DP-TSP (Exact)":
                gap = _pct(c, dp_cost)
                print(f"    {name:<25} {gap}")
    else:
        print(f"\n[6] DP-TSP skipped — {len(nodes)} nodes > limit ({dp_limit}).")
        print(f"    Full Local Search is the best result.")

    best_name = min(results, key=lambda k: results[k][1])
    best_cost = results[best_name][1]
    print(f"\n  ✓  Best result: {best_name} — cost {best_cost:.2f}")
    print(f"{SEP}\n")
    return results




def print_complexity_table() -> None:
    rows = [
        ("Paradigm",       "Algorithm",             "Time",        "Space",   "Optimal?"),
        ("─"*12,           "─"*24,                  "─"*16,        "─"*8,     "─"*9),
        ("Graph",          "Dijkstra (per source)",  "O((V+E)logV)","O(V)",    "Yes (SP)"),
        ("DP",             "Floyd-Warshall",          "O(V³)",       "O(V²)",   "Yes (SP)"),
        ("Greedy",         "Nearest-Neighbour TSP",   "O(n²)",       "O(n)",    "No"),
        ("Greedy",         "Nearest-Insertion TSP",   "O(n²)",       "O(n)",    "No"),
        ("Local Search",   "2-Opt",                   "O(n²/pass)",  "O(n)",    "No"),
        ("Local Search",   "Or-Opt (k=1,2,3)",        "O(n²/pass)",  "O(n)",    "No"),
        ("Local Search",   "3-Opt",                   "O(n³/pass)",  "O(n)",    "No"),
        ("DP",             "Held-Karp / Bitmask-DP",  "O(2ⁿ·n²)",   "O(2ⁿ·n)", "Yes"),
        ("VRP Heuristic",  "Clarke-Wright Savings",   "O(n² log n)", "O(n²)",   "No"),
    ]
    print(f"\n{SEP}")
    print("  SUDOS — Algorithm Complexity Reference")
    print(SEP)
    fmt = "  {:<14}  {:<26}  {:<16}  {:<10}  {}"
    for r in rows:
        print(fmt.format(*r))
    print(SEP + "\n")




def compare_partitioning(
    deliveries: List[int],
    num_agents: int,
    dist: List[List[float]],
    depot: int = 0,
) -> None:
  
    print(f"\n{SEP}")
    print(f"  Multi-Agent Partitioning Comparison  ({num_agents} agents)")
    print(SEP)

    for strategy in ("round_robin", "clarke_wright"):
        t0 = time.perf_counter()
        results = assign_deliveries_to_agents(
            deliveries, num_agents, dist, depot,
            routing="local_search",
            partitioning=strategy,
        )
        elapsed = time.perf_counter() - t0
        total   = sum(c for _, _, c in results)

        label = "Round-Robin   " if strategy == "round_robin" else "Clarke-Wright "
        print(f"\n  [{label}]  total cost = {total:.2f}   ({_ms(elapsed)})")
        for aid, route, cost in results:
            print(f"    Agent {aid+1}: {route}  →  {cost:.2f}")

    print(SEP + "\n")