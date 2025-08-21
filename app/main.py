from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import GraphRequest, ShortestPathResponse, SaveRequest
from .algorithms import run_algorithm
from .storage import save_topology, load_topology, list_topologies

app = FastAPI(title="Network Routing Simulator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/shortest-path", response_model=ShortestPathResponse)
def shortest_path(req: GraphRequest):
    # Validate minimal
    if req.source is None or req.target is None:
        raise HTTPException(status_code=400, detail="source and target required")
    result = run_algorithm(req.nodes, req.edges, req.algorithm, req.source, req.target, req.options or {})
    return result

@app.post("/api/save")
def save(req: SaveRequest):
    save_topology(req.id, req.topology)
    return {"status": "ok", "id": req.id}

@app.get("/api/load/{topo_id}")
def load(topo_id: str):
    topo = load_topology(topo_id)
    if topo is None:
        raise HTTPException(status_code=404, detail="not found")
    return {"topology": topo}

@app.get("/api/list")
def list_saved():
    return {"list": list_topologies()}
