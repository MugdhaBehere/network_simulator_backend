from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from .models import GraphRequest, ShortestPathResponse, SaveRequest, Graph, Node
from .algorithms import run_algorithm
from .storage import save_topology, load_topology, list_topologies

app = FastAPI(title="Network Routing Simulator API")

origins = [
    "https://netsimulator.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,   
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok", "message": "Network Simulator API is running"}




@app.post("/api/shortest-path", response_model=ShortestPathResponse)
def shortest_path(req: GraphRequest):
    if req.source is None or req.target is None:
        raise HTTPException(status_code=400, detail="source and target required")
    return run_algorithm(req.nodes, req.edges, req.algorithm, req.source, req.target, req.options or {})

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

# Router section
router = APIRouter()
current_graph: Graph = Graph(nodes=[], edges=[])

@router.get("/fetch-nodes", response_model=List[Node])
def fetch_nodes():
    if not current_graph.nodes:
        raise HTTPException(status_code=404, detail="No nodes found in the graph")
    return current_graph.nodes

app.include_router(router, prefix="/api")
