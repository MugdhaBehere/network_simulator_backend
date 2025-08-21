# backend/app/storage.py
import json, os
BASE_DIR = os.path.dirname(__file__)
SAVE_DIR = os.path.join(BASE_DIR, "..", "saved_topologies")
os.makedirs(SAVE_DIR, exist_ok=True)

def save_topology(tid, topology):
    path = os.path.join(SAVE_DIR, f"{tid}.json")
    with open(path, "w") as f:
        json.dump(topology, f)

def load_topology(self):
    with self.client.get("/get_topologies", catch_response=True) as response:
        if response.status_code == 200:
            topologies = response.json()
            
            # if it's a dict, convert to list of values
            if isinstance(topologies, dict):
                topologies = list(topologies.values())
            
            if not topologies:
                response.failure("No topologies available")
                return None
            
            topology = random.choice(topologies)
            return topology
        else:
            response.failure(f"Failed to fetch topologies: {response.status_code}")
            return None


def list_topologies():
    files = []
    for fname in os.listdir(SAVE_DIR):
        if fname.endswith(".json"):
            files.append(fname[:-5])
    return files
