
from __future__ import annotations

import math
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest

from core.graph          import (build_adjacency_list, build_distance_matrix,
                                  generate_random_graph, is_connected, validate_route)
from algorithms.dijkstra import dijkstra, dijkstra_with_path
from algorithms.floyd_warshall import floyd_warshall, reconstruct_path
from algorithms.greedy_tsp     import greedy_tsp, nearest_insertion_tsp, tour_cost
from algorithms.dp_tsp         import dp_tsp_bitmask
from algorithms.local_search   import two_opt, or_opt, full_local_search




EDGES_4 = [(0,1,10),(0,2,15),(0,3,20),(1,2,9),(1,3,12),(2,3,10)]
N4 = 4

EDGES_6 = [
    (0,1,10),(0,2,15),(0,3,20),(0,4,25),(0,5,30),
    (1,2, 9),(1,3,12),(1,4,18),(1,5,22),
    (2,3,10),(2,4,14),(2,5,17),
    (3,4, 8),(3,5,12),
    (4,5, 7),
]
N6 = 6

@pytest.fixture
def graph4():
    return build_adjacency_list(EDGES_4, N4)

@pytest.fixture
def dist4(graph4):
    return build_distance_matrix(graph4, N4)

@pytest.fixture
def graph6():
    return build_adjacency_list(EDGES_6, N6)

@pytest.fixture
def dist6(graph6):
    return build_distance_matrix(graph6, N6)




class TestGraph:
    def test_adjacency_list_undirected(self, graph4):
        # Every edge appears in both directions
        assert any(v == 1 for v, _ in graph4[0])
        assert any(v == 0 for v, _ in graph4[1])

    def test_adjacency_list_weights(self, graph4):
        weights = {v: w for v, w in graph4[0]}
        assert weights[1] == 10
        assert weights[2] == 15

    def test_negative_weight_raises(self):
        with pytest.raises(ValueError):
            build_adjacency_list([(0, 1, -5)], 2)

    def test_is_connected_true(self, graph4):
        assert is_connected(graph4, N4)

    def test_is_connected_false(self):
        isolated = build_adjacency_list([(0, 1, 5)], 3)
        assert not is_connected(isolated, 3)

    def test_random_graph_connected(self):
        edges = generate_random_graph(20, density=0.3, seed=99)
        g = build_adjacency_list(edges, 20)
        assert is_connected(g, 20)

    def test_validate_route_ok(self):
        assert validate_route([0,1,2,3,0], [1,2,3], depot=0)

    def test_validate_route_bad_depot(self):
        assert not validate_route([1,2,3,0], [2,3], depot=0)

    def test_validate_route_missing_node(self):
        assert not validate_route([0,1,3,0], [1,2,3], depot=0)




class TestDijkstra:
    def test_self_distance_zero(self, graph4):
        assert dijkstra(graph4, 0, N4)[0] == 0.0

    def test_direct_edge(self, graph4):
        assert dijkstra(graph4, 0, N4)[1] == 10.0

    def test_indirect_shorter(self, graph4):
        # 0→2 direct=15; 0→1→2=10+9=19; shortest is 15
        assert dijkstra(graph4, 0, N4)[2] == 15.0

    def test_symmetry(self, graph4):
        d01 = dijkstra(graph4, 0, N4)[1]
        d10 = dijkstra(graph4, 1, N4)[0]
        assert math.isclose(d01, d10)

    def test_unreachable(self):
        g = {0: [(1, 5)], 1: [(0, 5)], 2: []}
        assert dijkstra(g, 0, 3)[2] == float("inf")

    def test_with_path_basic(self, graph4):
        cost, path = dijkstra_with_path(graph4, 0, 3, N4)
        assert path[0] == 0 and path[-1] == 3
        assert math.isclose(cost, 20.0)   

    def test_with_path_unreachable(self):
        g = {0: [(1, 5)], 1: [(0, 5)], 2: []}
        cost, path = dijkstra_with_path(g, 0, 2, 3)
        assert cost == float("inf")
        assert path == []

    def test_early_termination(self, graph4):
        
        d = dijkstra(graph4, 0, N4, target=2)
        assert d[2] == 15.0




class TestFloydWarshall:
    def test_zero_diagonal(self):
        dist, _ = floyd_warshall(N4, EDGES_4)
        for i in range(N4):
            assert dist[i][i] == 0.0

    def test_symmetry(self):
        dist, _ = floyd_warshall(N4, EDGES_4)
        for i in range(N4):
            for j in range(N4):
                assert math.isclose(dist[i][j], dist[j][i])

    def test_matches_dijkstra(self, dist4):
        fw, _ = floyd_warshall(N4, EDGES_4)
        for i in range(N4):
            for j in range(N4):
                assert math.isclose(fw[i][j], dist4[i][j], rel_tol=1e-9)

    def test_path_reconstruction(self):
        _, nxt = floyd_warshall(N4, EDGES_4, track_paths=True)
        assert nxt is not None
        path = reconstruct_path(nxt, 0, 3)
        assert path[0] == 0 and path[-1] == 3

    def test_no_path(self):
        dist, nxt = floyd_warshall(3, [(0,1,5)], track_paths=True)
        assert dist[0][2] == float("inf")




class TestGreedyTSP:
    def test_empty(self, dist4):
        route, cost = greedy_tsp(dist4, [], depot=0)
        assert route == [0, 0] and cost == 0.0

    def test_single(self, dist4):
        route, cost = greedy_tsp(dist4, [2], depot=0)
        assert route[0] == route[-1] == 0
        assert 2 in route
        assert math.isclose(cost, dist4[0][2] + dist4[2][0])

    def test_depot_at_both_ends(self, dist4):
        route, _ = greedy_tsp(dist4, [1,2,3], depot=0)
        assert route[0] == 0 and route[-1] == 0

    def test_all_visited(self, dist4):
        nodes = [1, 2, 3]
        route, _ = greedy_tsp(dist4, nodes)
        assert set(nodes).issubset(set(route))

    def test_cost_matches_route(self, dist4):
        route, cost = greedy_tsp(dist4, [1,2,3])
        assert math.isclose(cost, tour_cost(route, dist4))


class TestNearestInsertion:
    def test_depot_at_both_ends(self, dist6):
        route, _ = nearest_insertion_tsp(dist6, [1,2,3,4,5])
        assert route[0] == route[-1] == 0

    def test_all_visited(self, dist6):
        nodes = [1,2,3,4,5]
        route, _ = nearest_insertion_tsp(dist6, nodes)
        assert set(nodes).issubset(set(route))

    def test_cost_consistent(self, dist6):
        route, cost = nearest_insertion_tsp(dist6, [1,2,3,4,5])
        assert math.isclose(cost, tour_cost(route, dist6), rel_tol=1e-9)

    def test_empty(self, dist4):
        route, cost = nearest_insertion_tsp(dist4, [])
        assert route == [0, 0] and cost == 0.0




class TestDPTSP:
    def test_empty(self, dist4):
        route, cost = dp_tsp_bitmask(dist4, [])
        assert cost == 0.0

    def test_single(self, dist4):
        route, cost = dp_tsp_bitmask(dist4, [3])
        assert math.isclose(cost, dist4[0][3] + dist4[3][0])

    def test_optimal_lte_greedy(self, dist6):
        nodes = [1,2,3,4,5]
        _, g_cost  = greedy_tsp(dist6, nodes)
        _, dp_cost = dp_tsp_bitmask(dist6, nodes)
        assert dp_cost <= g_cost + 1e-9

    def test_route_validity(self, dist6):
        nodes = [1,2,3,4,5]
        route, _ = dp_tsp_bitmask(dist6, nodes)
        assert validate_route(route, nodes, depot=0)

    def test_cost_consistent(self, dist6):
        nodes = [1,2,3,4,5]
        route, cost = dp_tsp_bitmask(dist6, nodes)
        assert math.isclose(cost, tour_cost(route, dist6), rel_tol=1e-9)

    def test_too_large_raises(self):
        big_dist = [[float("inf")] * 25 for _ in range(25)]
        for i in range(25):
            big_dist[i][i] = 0
        with pytest.raises(ValueError):
            dp_tsp_bitmask(big_dist, list(range(1, 22)))




class TestTwoOpt:
    def test_does_not_increase_cost(self, dist6):
        init, g_cost = greedy_tsp(dist6, [1,2,3,4,5])
        _, opt_cost  = two_opt(init[:], dist6)
        assert opt_cost <= g_cost + 1e-9

    def test_depot_preserved(self, dist6):
        init, _ = greedy_tsp(dist6, [1,2,3,4,5])
        route, _ = two_opt(init[:], dist6)
        assert route[0] == 0 and route[-1] == 0

    def test_all_nodes_present(self, dist6):
        nodes = [1,2,3,4,5]
        init, _ = greedy_tsp(dist6, nodes)
        route, _ = two_opt(init[:], dist6)
        assert set(nodes).issubset(set(route))


class TestOrOpt:
    def test_does_not_increase_cost(self, dist6):
        init, g_cost = greedy_tsp(dist6, [1,2,3,4,5])
        init, g_cost = two_opt(init, dist6)
        _, oo_cost   = or_opt(init[:], dist6)
        assert oo_cost <= g_cost + 1e-9

    def test_depot_preserved(self, dist6):
        init, _ = greedy_tsp(dist6, [1,2,3,4,5])
        route, _ = or_opt(init[:], dist6)
        assert route[0] == 0 and route[-1] == 0


class TestFullLocalSearch:
    def test_beats_greedy_or_equal(self, dist6):
        nodes = [1,2,3,4,5]
        _, g_cost  = greedy_tsp(dist6, nodes)
        seed, _    = nearest_insertion_tsp(dist6, nodes)
        _, fl_cost = full_local_search(seed[:], dist6)
        assert fl_cost <= g_cost + 1e-9

    def test_near_optimal(self, dist6):
        nodes = [1,2,3,4,5]
        seed, _    = nearest_insertion_tsp(dist6, nodes)
        _, fl_cost = full_local_search(seed[:], dist6)
        _, dp_cost = dp_tsp_bitmask(dist6, nodes)
        gap = (fl_cost - dp_cost) / dp_cost
        assert gap < 0.10   # within 10 % of optimal




if __name__ == "__main__":
    import unittest


    graph4 = build_adjacency_list(EDGES_4, N4)
    dist4  = build_distance_matrix(graph4, N4)
    graph6 = build_adjacency_list(EDGES_6, N6)
    dist6  = build_distance_matrix(graph6, N6)

    tests_passed = 0
    tests_failed = 0

    def run(name, fn):
        global tests_passed, tests_failed
        try:
            fn()
            print(f"  ✓  {name}")
            tests_passed += 1
        except Exception as e:
            print(f"  ✗  {name}  —  {e}")
            tests_failed += 1

    print("\n── SUDOS Test Suite (standalone) ──\n")

    run("dijkstra self=0",        lambda: assert_(dijkstra(graph4,0,N4)[0]==0))
    run("dijkstra direct edge",   lambda: assert_(dijkstra(graph4,0,N4)[1]==10))
    run("floyd matches dijkstra", lambda: [assert_(math.isclose(floyd_warshall(N4,EDGES_4)[0][i][j], dist4[i][j])) for i in range(N4) for j in range(N4)])
    run("greedy empty",           lambda: assert_(greedy_tsp(dist4,[],0)==([0,0],0.0)))
    run("greedy all visited",     lambda: assert_(set([1,2,3]).issubset(greedy_tsp(dist4,[1,2,3])[0])))
    run("dp optimal<=greedy",     lambda: assert_(dp_tsp_bitmask(dist6,[1,2,3,4,5])[1] <= greedy_tsp(dist6,[1,2,3,4,5])[1]+1e-9))
    run("2-opt no increase",      lambda: assert_(two_opt(greedy_tsp(dist6,[1,2,3,4,5])[0][:],dist6)[1] <= greedy_tsp(dist6,[1,2,3,4,5])[1]+1e-9))
    run("validate route ok",      lambda: assert_(validate_route([0,1,2,3,0],[1,2,3],0)))

    print(f"\n  Passed: {tests_passed}   Failed: {tests_failed}\n")

def assert_(cond):
    if not cond:
        raise AssertionError("condition is False")