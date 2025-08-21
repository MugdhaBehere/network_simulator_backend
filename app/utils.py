"""
graph_utils.py
Graph algorithms & helpers: Dijkstra, Bellman-Ford, A*, BFS, random generator.
"""

import random, time, math
from typing import Dict, List, Tuple, Optional
from .models import Topology, Node, Edge

def topology_to_adj(topology: Topology) -> Dict[str, List[Tuple[str, float, Optional[str]]]]:
    adj: Dict[str, List[Tuple[str, float, Optional[str]]]] = {}
    for n in topology.nodes:
        adj[n.id] = []
    for e in topology.edges:
        if e.source not in adj:
            adj[e.source] = []
        adj[e.source].append((e.target, float(e.weight), e.id))
    return adj

def reconstruct_path(prev: Dict[str, Optional[str]], source: str, target: str) -> Optional[List[str]]:
    path = []
    cur = target
    while cur is not None:
        path.append(cur)
        cur = prev.get(cur, None)
    path.reverse()
    if not path or path[0] != source:
        return None
    return path

# Dijkstra
def dijkstra(topology: Topology, source: str, target: str):
    adj = topology_to_adj(topology)
    nodes = list(adj.keys())
    import heapq
    dist = {v: float("inf") for v in nodes}
    prev: Dict[str, Optional[str]] = {v: None for v in nodes}
    dist[source] = 0.0
    heap = [(0.0, source)]
    visited_order = []
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        visited_order.append(u)
        if u == target:
            break
        for (v, w, eid) in adj.get(u, []):
            alt = dist[u] + w
            if alt < dist.get(v, float("inf")):
                dist[v] = alt
                prev[v] = u
                heapq.heappush(heap, (alt, v))
    path = reconstruct_path(prev, source, target)
    return {"path": path, "dist": dist, "prev": prev, "visited_order": visited_order}

# Bellman-Ford
def bellman_ford(topology: Topology, source: str, target: str):
    adj = topology_to_adj(topology)
    nodes = list(adj.keys())
    dist = {v: float("inf") for v in nodes}
    prev: Dict[str, Optional[str]] = {v: None for v in nodes}
    dist[source] = 0.0
    edges_list: List[Tuple[str, str, float]] = []
    for u in adj:
        for v, w, eid in adj[u]:
            edges_list.append((u, v, float(w)))
    for _ in range(len(nodes) - 1):
        changed = False
        for (u, v, w) in edges_list:
            if dist[u] != float("inf") and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u
                changed = True
        if not changed:
            break
    for (u, v, w) in edges_list:
        if dist[u] != float("inf") and dist[u] + w < dist[v]:
            raise ValueError("Negative weight cycle detected")
    path = reconstruct_path(prev, source, target)
    return {"path": path, "dist": dist, "prev": prev, "visited_order": []}

# BFS (unweighted)
from collections import deque
def bfs(topology: Topology, source: str, target: str):
    adj = topology_to_adj(topology)
    prev: Dict[str, Optional[str]] = {v: None for v in adj}
    q = deque([source])
    visited = set([source])
    visited_order = []
    while q:
        u = q.popleft()
        visited_order.append(u)
        if u == target:
            break
        for (v, w, eid) in adj.get(u, []):
            if v not in visited:
                visited.add(v)
                prev[v] = u
                q.append(v)
    path = reconstruct_path(prev, source, target)
    return {"path": path, "dist": {}, "prev": prev, "visited_order": visited_order}

# A* (Euclidean heuristic if x,y present)
def heuristic(a: str, b: str, topology: Topology) -> float:
    pos = {n.id: (n.x, n.y) for n in topology.nodes}
    pa = pos.get(a); pb = pos.get(b)
    if not pa or not pb or pa[0] is None or pb[0] is None:
        return 0.0
    dx = pa[0] - pb[0]; dy = pa[1] - pb[1]
    return math.hypot(dx, dy)

def astar(topology: Topology, source: str, target: str):
    adj = topology_to_adj(topology)
    nodes = list(adj.keys())
    import heapq
    gscore = {v: float("inf") for v in nodes}
    fscore = {v: float("inf") for v in nodes}
    prev: Dict[str, Optional[str]] = {v: None for v in nodes}
    gscore[source] = 0.0
    fscore[source] = heuristic(source, target, topology)
    heap = [(fscore[source], source)]
    visited_order = []
    while heap:
        f, u = heapq.heappop(heap)
        visited_order.append(u)
        if u == target:
            break
        for (v, w, eid) in adj.get(u, []):
            tentative_g = gscore[u] + w
            if tentative_g < gscore.get(v, float("inf")):
                prev[v] = u
                gscore[v] = tentative_g
                fscore[v] = tentative_g + heuristic(v, target, topology)
                heapq.heappush(heap, (fscore[v], v))
    path = reconstruct_path(prev, source, target)
    return {"path": path, "dist": gscore, "prev": prev, "visited_order": visited_order}

# Random generator
def generate_random_topology(num_nodes: int = 20, density: float = 0.1, max_weight: float = 10.0) -> Topology:
    nodes: List[Node] = []
    edges: List[Edge] = []
    for i in range(num_nodes):
        nid = f"n{i}"
        nodes.append(Node(id=nid, label=nid, x=random.uniform(50, 900), y=random.uniform(50, 600)))
    for i in range(num_nodes):
        for j in range(num_nodes):
            if i == j: continue
            if random.random() < density:
                weight = round(random.uniform(1.0, max_weight), 2)
                edges.append(Edge(id=f"e{i}_{j}_{int(time.time()*1000)}_{random.randint(0,999)}", source=f"n{i}", target=f"n{j}", weight=weight))
    return Topology(nodes=nodes, edges=edges)
