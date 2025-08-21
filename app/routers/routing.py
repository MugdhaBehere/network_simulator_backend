from fastapi import APIRouter, HTTPException
from ..models import RouteRequest
from ..utils import dijkstra, bellman_ford, astar, bfs
import time

router = APIRouter(prefix="/route", tags=["route"])

ALGO_MAP = {
    "dijkstra": dijkstra,
    "bellman-ford": bellman_ford,
    "bellmanford": bellman_ford,
    "astar": astar,
    "a*": astar,
    "bfs": bfs
}

@router.post("/shortest")
def shortest(req: RouteRequest):
    if not req.topology or not req.topology.nodes:
        raise HTTPException(status_code=400, detail="topology required")
    node_ids = {n.id for n in req.topology.nodes}
    if req.source not in node_ids or req.target not in node_ids:
        raise HTTPException(status_code=400, detail="source/target must be in topology")
    algorithm = (req.algorithm or "dijkstra").lower()
    fn = ALGO_MAP.get(algorithm)
    if not fn:
        raise HTTPException(status_code=400, detail=f"unknown algorithm {algorithm}")
    start = time.time()
    try:
        res = fn(req.topology, req.source, req.target)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    elapsed_ms = int((time.time() - start) * 1000)
    return {"algorithm": algorithm, "time_ms": elapsed_ms, "result": res}
