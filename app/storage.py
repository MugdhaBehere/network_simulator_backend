# backend/app/storage.py
import json, os
BASE_DIR = os.path.dirname(__file__)
SAVE_DIR = os.path.join(BASE_DIR, "..", "saved_topologies")
os.makedirs(SAVE_DIR, exist_ok=True)

def save_topology(tid, topology):
    path = os.path.join(SAVE_DIR, f"{tid}.json")
    with open(path, "w") as f:
        json.dump(topology, f)

def load_topology(tid):
    path = os.path.join(SAVE_DIR, f"{tid}.json")
    if not os.path.exists(path): return None
    with open(path) as f:
        return json.load(f)

def list_topologies():
    files = []
    for fname in os.listdir(SAVE_DIR):
        if fname.endswith(".json"):
            files.append(fname[:-5])
    return files
