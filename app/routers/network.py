from fastapi import APIRouter, HTTPException
from ..models import GenerateRequest, SaveRequest
from ..utils import generate_random_topology
import os, json, time, uuid

router = APIRouter(prefix="/network", tags=["network"])
SAVED_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "saved_topologies")
os.makedirs(SAVED_DIR, exist_ok=True)

@router.get("/health")
def health():
    return {"ok": True}

@router.post("/generate")
def generate(req: GenerateRequest):
    topo = generate_random_topology(req.nodes, req.density, req.max_weight)
    return {"topology": topo.dict()}

@router.post("/save")
def save(req: SaveRequest):
    if not req.topology:
        raise HTTPException(status_code=400, detail="topology required")
    tid = str(uuid.uuid4())
    entry = {"id": tid, "name": req.name or f"topo-{tid[:6]}", "topology": req.topology.dict(), "created_at": int(time.time())}
    path = os.path.join(SAVED_DIR, f"{tid}.json")
    with open(path, "w") as f:
        json.dump(entry, f, indent=2)
    return {"id": tid}

@router.get("/list")
def list_topologies():
    files = os.listdir(SAVED_DIR)
    out = []
    for fname in files:
        try:
            with open(os.path.join(SAVED_DIR, fname), "r") as f:
                entry = json.load(f)
                out.append({"id": entry["id"], "name": entry.get("name"), "created_at": entry.get("created_at")})
        except:
            continue
    return {"list": out}

@router.get("/load/{tid}")
def load_topology(tid: str):
    path = os.path.join(SAVED_DIR, f"{tid}.json")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="not found")
    with open(path, "r") as f:
        entry = json.load(f)
    return {"topology": entry["topology"], "id": entry["id"], "name": entry.get("name")}
