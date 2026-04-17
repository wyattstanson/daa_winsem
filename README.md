# SUDOS — Smart Urban Delivery Optimization System

> **DAA Project Kit-01** · Design and Analysis of Algorithms · Python 3.8+

SUDOS models a city road network as a **weighted directed graph** and solves the resulting Vehicle Routing Problem (VRP) using a full hierarchy of DAA paradigms: Greedy, Graph (SSSP/APSP), Dynamic Programming, and Local Search approximation.

---

## 
Highlights

| Feature | Detail |
|---|---|
| **5 algorithms** | Dijkstra, Floyd-Warshall, Greedy TSP, Held-Karp DP, Local Search |
| **Local search pipeline** | Nearest-Insertion → 2-Opt → Or-Opt (k=1,2,3) → 3-Opt |
| **Optimality gap** | **0–9%** from exact optimal (verified against Held-Karp) |
| **VRP partitioning** | Round-Robin vs Clarke-Wright Savings (15–30% cost reduction) |
| **No external packages** | Pure Python 3.8+ standard library only |
| **40+ unit tests** | Full pytest suite with correctness proofs |

---

##  Project Structure

```
DAA_WINSEM/
├── main.py                      ← Entry point: 5 working demo scenarios
├── requirements.txt
│
├── agents/
│   ├── __init__.py
│   └── assignment.py            ← Round-Robin + Clarke-Wright Savings VRP
│
├── algorithms/
│   ├── __init__.py
│   ├── dijkstra.py              ← SSSP + path reconstruction + early exit
│   │                               O((V+E) log V)
│   ├── dp_tsp.py                ← Held-Karp exact TSP, flat array DP
│   │                               O(2ⁿ·n²), n ≤ 20
│   ├── floyd_warshall.py        ← APSP + next-hop matrix for path recovery
│   │                               O(V³)
│   ├── greedy_tsp.py            ← Nearest-Neighbour + Nearest-Insertion
│   │                               O(n²)
│   └── local_search.py          ← 2-Opt, Or-Opt (k=1,2,3), 3-Opt,
│                                   full_local_search() pipeline
│
├── core/
│   ├── __init__.py
│   └── graph.py                 ← Adjacency list, distance matrix
│                                   (Dijkstra-precomputed), random graph
│                                   generator, Euclidean graph generator,
│                                   connectivity check, route validator
│
└── utils/
    ├── __init__.py
    ├── benchmark.py             ← Full comparison report, complexity table,
    │                               partitioning comparison
    └── test_algorithms.py       ← 40+ unit tests
```

---

##  Quick Start

```bash
# Clone the repo
git clone https://github.com/your-username/SUDOS-DAA.git
cd SUDOS-DAA/DAA_WINSEM

# Run all 5 demo scenarios
python main.py

# Run the full test suite
pytest utils/test_algorithms.py -v

# Run the benchmark report
python -c "from utils.benchmark import run_full_benchmark; run_full_benchmark()"
```

**Requirements:** Python 3.8+ · No external packages · `pytest` for tests only

---

##  Algorithms

### Graph Algorithms

#### Dijkstra's SSSP — `O((V+E) log V)`
Single-source shortest paths using a min-heap priority queue. SUDOS precomputes the full n×n distance matrix at graph construction time, so all routing lookups are O(1). Includes early-exit optimisation for single-pair queries and full path reconstruction via a predecessor array.

#### Floyd-Warshall APSP — `O(V³)`
All-pairs shortest paths with a **next-hop matrix** for O(path_length) path recovery. Includes negative-cycle detection. Used for dense graph analysis and comparative benchmarking.

---

### TSP Constructive Heuristics — `O(n²)`

#### Nearest-Neighbour (NN)
Greedy construction: always move to the closest unvisited node. Fast but can produce tours up to O(log n) times optimal in the worst case.

#### Nearest-Insertion (NI)
Maintains a partial tour; inserts the closest un-toured node at the cheapest position. Produces significantly better seeds for local search than NN, especially on clustered instances.

---

### Exact TSP — `O(2ⁿ · n²)` — `n ≤ 20`

#### Held-Karp Dynamic Programming
Bitmask DP where `dp[S][v]` = minimum cost to visit exactly the nodes in bitmask `S`, ending at node `v`. Provably optimal.

**SUDOS optimisation:** stores `dp` as a **flat 1D array** indexed by `S * n + v` instead of a list-of-lists, achieving ~20% speedup through better cache locality.

---

### Local Search Refinement

| Move | Complexity | Effect |
|---|---|---|
| **2-Opt** | O(n²) / pass | Removes crossing edges by reversing tour segments |
| **Or-Opt k=1** | O(n²) / pass | Relocates single nodes to cheaper positions |
| **Or-Opt k=2,3** | O(n²) / pass | Relocates pairs/triples of consecutive nodes |
| **3-Opt** | O(n³) / pass | Three-edge swap for final polishing |

#### `full_local_search()` Pipeline
```
NI seed → 2-Opt → Or-Opt(k=1) → Or-Opt(k=2) → Or-Opt(k=3) → 3-Opt
```
Achieves **0–9% gap from exact optimal** on tested graphs. Or-Opt alone typically adds **5–25% improvement** after 2-Opt reaches its local optimum.

---

### VRP Agent Partitioning

#### Round-Robin — `O(n log n)`
Sort delivery nodes by distance from depot; assign cyclically. Simple but ignores geographic clustering.

#### Clarke-Wright Savings — `O(n² log n)`
Computes savings `s(i,j) = d(depot,i) + d(depot,j) − d(i,j)` for all pairs, then greedily merges routes by decreasing savings. Results in **15–30% lower total fleet cost** vs Round-Robin by naturally grouping nearby deliveries.

---

##  Benchmark Results

### Algorithm Comparison (15-node graph)

| Algorithm | Optimality Gap | Wall-clock |
|---|---|---|
| Held-Karp DP (exact) | 0% | ~800 ms |
| Full pipeline (NI → 2-opt → Or-opt) | **0–9%** | **~2 ms** |
| Nearest-Insertion only | 10–25% | < 1 ms |
| Nearest-Neighbour only | 15–35% | < 1 ms |

### Partitioning Comparison (30 nodes, 4 agents)

| Strategy | Total Fleet Cost | Balance |
|---|---|---|
| Round-Robin | Baseline | Imbalanced |
| Clarke-Wright | **15–30% lower** | More balanced |

---

##  Demo Scenarios

Run `python main.py` to execute all five:

| # | Scenario | Graph | Agents | What it shows |
|---|---|---|---|---|
| 1 | Small City | 10 nodes | 1 | Greedy vs Held-Karp, optimality gap |
| 2 | Medium City | 15 nodes | 2 | Round-Robin partition, 2-Opt, Or-Opt |
| 3 | Large City | 30 nodes | 4 | Clarke-Wright vs Round-Robin, full pipeline |
| 4 | Floyd-Warshall | 15 nodes (dense) | 1 | APSP matrix, path recovery |
| 5 | Euclidean City | 20 nodes (XY) | 2 | Coordinate-based graph, full pipeline |

---

## Testing

```bash
pytest utils/test_algorithms.py -v
```

**40+ tests across 8 categories:**

- Graph construction & connectivity (8 tests)
- Dijkstra correctness vs BFS, triangle inequality (6 tests)
- Floyd-Warshall APSP consistency, path recovery, negative cycles (5 tests)
- Greedy TSP tour completeness, depot start/end (7 tests)
- Held-Karp exact optimality vs brute-force (n ≤ 8) (5 tests)
- Local search monotone improvement, convergence (6 tests)
- Agent assignment correctness, CW vs RR cost (6 tests)
- Integration / smoke tests on all 5 demo configs (4 tests)

---

##  Complexity Reference

| Algorithm | Time | Space | Optimal? |
|---|---|---|---|
| Dijkstra SSSP | O((V+E) log V) | O(V+E) | ✅ SSSP |
| Floyd-Warshall APSP | O(V³) | O(V²) | ✅ APSP |
| Nearest-Neighbour TSP | O(n²) | O(n) | ❌ |
| Nearest-Insertion TSP | O(n²) | O(n) | ❌ |
| Held-Karp DP TSP | O(2ⁿ·n²) | O(2ⁿ·n) | ✅ n≤20 |
| 2-Opt | O(n²)/pass | O(n) | ❌ |
| Or-Opt (k=1,2,3) | O(n²)/pass | O(n) | ❌ |
| 3-Opt | O(n³)/pass | O(n) | ❌ |
| Round-Robin VRP | O(n log n) | O(n) | ❌ |
| Clarke-Wright VRP | O(n² log n) | O(n²) | ❌ |

---

## 🗺️ Roadmap

- [ ] `matplotlib` visualisation — agent routes in distinct colours
- [ ] Streamlit web app — sliders for agents, graph size, algorithm
- [ ] OpenStreetMap integration via `osmnx`
- [ ] Lin-Kernighan-style moves (LK-3, LK-4)
- [ ] Time-windowed VRP with delivery deadlines
- [ ] Parallel local search (multi-core restarts)

---

##  References

1. Cormen, T. H. et al. *Introduction to Algorithms* (4th ed.). MIT Press, 2022.
2. Clarke, G. & Wright, J. W. "Scheduling of vehicles from a central depot." *Operations Research*, 12(4), 1964.
3. Held, M. & Karp, R. M. "A dynamic programming approach to sequencing problems." *JSIAM*, 10(1), 1962.
4. Lin, S. & Kernighan, B. W. "An effective heuristic for the traveling-salesman problem." *Operations Research*, 21(2), 1973.
5. Or, I. *Traveling Salesman-Type Combinatorial Problems* (PhD thesis). Northwestern University, 1976.

---

##  License

Academic project — DAA Kit-01. For educational use.
