# backend/app/algorithms.py
import heapq, math, time
from typing import List, Dict, Tuple, Any
from .models import Edge, Node

# helpers
def build_adj(nodes: List[Node], edges: List[Edge], directed=False):
    adj = {n.id: [] for n in nodes}
    for e in edges:
        adj[e.source].append((e.target, e.weight))
        if not directed:
            adj[e.target].append((e.source, e.weight))
    return adj

# BFS (unweighted shortest path)
def bfs(nodes, edges, source, target, options):
    adj = build_adj(nodes, edges, directed=options.get("directed", False))
    from collections import deque
    q = deque([(source, [source])])
    visited=set([source])
    steps=[]
    while q:
        v, path = q.popleft()
        steps.append({"visit": v})
        if v==target: return path, steps
        for nb,_ in adj.get(v,[]):
            if nb not in visited:
                visited.add(nb)
                q.append((nb, path+[nb]))
    return [], steps

# Dijkstra
def dijkstra(nodes, edges, source, target, options):
    adj = build_adj(nodes, edges, directed=options.get("directed", False))
    dist = {n.id: math.inf for n in nodes}
    prev = {n.id: None for n in nodes}
    dist[source]=0
    pq=[(0, source)]
    steps=[]
    while pq:
        d,u = heapq.heappop(pq)
        if d>dist[u]: continue
        steps.append({"pop": u, "dist": d})
        if u==target:
            break
        for v,w in adj.get(u,[]):
            nd = d + w
            if nd < dist[v]:
                dist[v]=nd
                prev[v]=u
                heapq.heappush(pq,(nd,v))
    # reconstruct
    path=[]
    cur=target
    while cur is not None:
        path.insert(0, cur)
        cur = prev[cur]
    if path and path[0]==source:
        return path, steps
    return [], steps

# Bellman-Ford
def bellman_ford(nodes, edges, source, target, options):
    ids=[n.id for n in nodes]
    dist = {i: math.inf for i in ids}
    prev = {i: None for i in ids}
    dist[source]=0
    steps=[]
    # relax
    for _ in range(len(ids)-1):
        changed=False
        for e in edges:
            if dist[e.source] + e.weight < dist[e.target]:
                dist[e.target] = dist[e.source] + e.weight
                prev[e.target] = e.source
                changed=True
                steps.append({"update": e.target, "dist": dist[e.target]})
            if dist[e.target] + e.weight < dist[e.source]:
                dist[e.source] = dist[e.target] + e.weight
                prev[e.source] = e.target
                changed=True
                steps.append({"update": e.source, "dist": dist[e.source]})
        if not changed:
            break
    path=[]
    cur=target
    while cur is not None:
        path.insert(0,cur)
        cur=prev[cur]
    if path and path[0]==source:
        return path, steps
    return [], steps

# A* (with optional coordinate heuristic if nodes have x,y)
def a_star(nodes, edges, source, target, options):
    adj = build_adj(nodes, edges, directed=options.get("directed", False))
    coords = {n.id: (n.x or 0, n.y or 0) for n in nodes}
    def h(a,b):
        (ax,ay) = coords.get(a,(0,0))
        (bx,by) = coords.get(b,(0,0))
        return math.hypot(ax-bx, ay-by)
    g={n.id: math.inf for n in nodes}
    g[source]=0
    pq=[(h(source,target), source)]
    prev={n.id: None for n in nodes}
    steps=[]
    while pq:
        f,u = heapq.heappop(pq)
        steps.append({"pop":u,"f":f})
        if u==target:
            break
        for v,w in adj.get(u,[]):
            tentative = g[u] + w
            if tentative < g[v]:
                g[v]=tentative
                prev[v]=u
                heapq.heappush(pq,(tentative + h(v,target), v))
    path=[]
    cur=target
    while cur is not None:
        path.insert(0,cur)
        cur=prev[cur]
    if path and path[0]==source:
        return path, steps
    return [], steps

# Floyd-Warshall
def floyd_warshall(nodes, edges, source, target, options):
    ids=[n.id for n in nodes]
    dist = {i: {j: math.inf for j in ids} for i in ids}
    nextn = {i: {j: None for j in ids} for i in ids}
    for i in ids: dist[i][i]=0
    for e in edges:
        dist[e.source][e.target]=e.weight
        dist[e.target][e.source]=e.weight
        nextn[e.source][e.target]=e.target
        nextn[e.target][e.source]=e.source
    for k in ids:
        for i in ids:
            for j in ids:
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    nextn[i][j] = nextn[i][k]
    if nextn[source][target] is None:
        return [], []
    path=[source]
    u=source
    while u!=target:
        u = nextn[u][target]
        path.append(u)
    return path, []

# runner
def run_algorithm(nodes, edges, algorithm, source, target, options):
    t0=time.time()
    alg = algorithm.strip().lower()
    if alg in ("bfs", "breadth-first", "breadthfirst"):
        path, steps = bfs(nodes, edges, source, target, options)
    elif alg in ("dijkstra",):
        path, steps = dijkstra(nodes, edges, source, target, options)
    elif alg in ("bellman-ford","bellmanford","bellman"):
        path, steps = bellman_ford(nodes, edges, source, target, options)
    elif alg in ("a*","astar","a-star"):
        path, steps = a_star(nodes, edges, source, target, options)
    elif alg in ("floyd","floyd-warshall","floydwarshall"):
        path, steps = floyd_warshall(nodes, edges, source, target, options)
    else:
        # default to dijkstra
        path, steps = dijkstra(nodes, edges, source, target, options)
    t1=time.time()
    metrics = {
        "time_ms": round((t1-t0)*1000,3),
        "hops": max(0, len(path)-1),
        "distance": None
    }
    # compute distance if path exists
    if path:
        idx = {n.id:n for n in nodes}
        dist=0.0
        for i in range(len(path)-1):
            a,b = path[i], path[i+1]
            # find an edge weight
            w = None
            for e in edges:
                if (e.source==a and e.target==b) or (e.source==b and e.target==a):
                    w=e.weight; break
            if w is None: w=1.0
            dist+=w
        metrics["distance"]=dist
    return {"path": path, "steps": steps, "metrics": metrics}
