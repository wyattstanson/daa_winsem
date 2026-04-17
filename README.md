

# SUDOS — Smart Urban Delivery Optimization System

**DAA Project Kit-01 · Design and Analysis of Algorithms**

> Model a city as a weighted graph. Assign deliveries to agents. Find optimal or near-optimal routes using multiple algorithmic paradigms.

---

## Project Structure

```
sudos/
├── main.py
├── requirements.txt
├── README.md
│
├── core/
│   ├── graph.py
│   └── __init__.py
│
├── algorithms/
│   ├── dijkstra.py
│   ├── floyd_warshall.py
│   ├── greedy_tsp.py
│   ├── dp_tsp.py
│   ├── local_search.py
│   └── __init__.py
│
├── agents/
│   ├── assignment.py
│   └── __init__.py
│
├── utils/
│   ├── benchmark.py
│   └── __init__.py
│
└── tests/
    ├── test_algorithms.py
    └── __init__.py
```

---

## Requirements

* Python 3.8 or higher (tested on 3.12)
* No external packages required to run `main.py`
* Optional packages for testing and visualization

---

## pip Installations

### Minimum (core runs with zero installs)

```bash
python main.py
```

### For running unit tests

```bash
pip install pytest
```

### For graph visualization (future extension)

```bash
pip install matplotlib networkx
```

### Install everything at once

```bash
pip install -r requirements.txt
```

### If using system-managed Python (Ubuntu/Debian)

```bash
pip install pytest matplotlib networkx --break-system-packages

# Recommended:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## How to Run

### 1. Clone / download the project

```bash
git clone https://github.com/<your-username>/sudos.git
cd sudos
```

### 2. Run all demos

```bash
python main.py
```

This runs:

* Demo 1 – Small graph, all algorithms + multi-agent dispatch
* Demo 2 – Medium random graph
* Demo 3 – Large graph (heuristics only)
* Demo 4 – Floyd-Warshall with path reconstruction
* Demo 5 – Euclidean graph

### 3. Run unit tests

```bash
pytest tests/ -v
```

Or:

```bash
python tests/test_algorithms.py
```

### 4. Use as a module

```python
from core.graph import build_adjacency_list, build_distance_matrix
from algorithms.dp_tsp import dp_tsp_bitmask
from algorithms.local_search import full_local_search
from algorithms.greedy_tsp import nearest_insertion_tsp

edges = [(0,1,10), (0,2,15), (1,2,9), (1,3,12), (2,3,10)]
graph = build_adjacency_list(edges, n=4)
dist  = build_distance_matrix(graph, n=4)

route, cost = dp_tsp_bitmask(dist, nodes=[1,2,3], depot=0)
print(route, cost)

route, cost = nearest_insertion_tsp(dist, nodes=[1,2,3], depot=0)
route, cost = full_local_search(route, dist)
print(route, cost)
```

---

## Deployment Options

### Option A — Run Locally

```bash
python main.py
```

### Option B — GitHub Repository

```bash
git init
git add .
git commit -m "initial commit: SUDOS DAA project"
git branch -M main
git remote add origin https://github.com/<your-username>/sudos.git
git push -u origin main
```

### Option C — Streamlit Web App

```bash
pip install streamlit
streamlit run app.py
```

### Option D — Docker

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
```

```bash
docker build -t sudos .
docker run sudos
```

### Option E — Google Colab

```bash
!python main.py
```

---

## Algorithm Reference

| # | Paradigm     | Algorithm         | Time         | Space   | Exact? |
| - | ------------ | ----------------- | ------------ | ------- | ------ |
| 1 | Graph        | Dijkstra          | O((V+E)logV) | O(V)    | Yes    |
| 2 | DP           | Floyd-Warshall    | O(V³)        | O(V²)   | Yes    |
| 3 | Greedy       | Nearest-Neighbour | O(n²)        | O(n)    | No     |
| 4 | Greedy       | Nearest-Insertion | O(n²)        | O(n)    | No     |
| 5 | Local Search | 2-Opt             | O(n²/pass)   | O(n)    | No     |
| 6 | Local Search | Or-Opt            | O(n²/pass)   | O(n)    | No     |
| 7 | Local Search | 3-Opt             | O(n³/pass)   | O(n)    | No     |
| 8 | DP           | Held-Karp         | O(2ⁿ·n²)     | O(2ⁿ·n) | Yes    |
| 9 | VRP          | Clarke-Wright     | O(n²logn)    | O(n²)   | No     |

---

## Continuation Prompt

(unchanged — removed emojis only)

```
PROJECT: SUDOS — Smart Urban Delivery Optimization System (DAA Project Kit-01)

PROBLEM STATEMENT:
Design a system that models a city as a weighted graph, assigns delivery
locations to multiple agents, and computes optimal or near-optimal routes.
The system must apply and compare multiple DAA paradigms.
```

---

## Submission Checklist

* GitHub public repo
* README.md present
* requirements.txt present
* Consistent git commits
* Report (10–15 pages)
* Presentation (10 slides)
* Video demo link

---
