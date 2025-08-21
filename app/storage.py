# backend/app/storage.py

import json
import os
from typing import Any, Dict, List, Optional

BASE_DIR = os.path.dirname(__file__)
SAVE_DIR = os.path.join(BASE_DIR, "..", "saved_topologies")
os.makedirs(SAVE_DIR, exist_ok=True)


def save_topology(tid: str, topology: Dict[str, Any]) -> None:
    """
    Save a topology to a JSON file.

    Args:
        tid: Topology ID (used as filename).
        topology: Dictionary representing the topology.
    """
    path = os.path.join(SAVE_DIR, f"{tid}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(topology, f, indent=2)


def load_topology(tid: str) -> Optional[Dict[str, Any]]:
    """
    Load a topology by ID from storage.

    Args:
        tid: Topology ID (filename without .json extension).

    Returns:
        The topology dictionary if found, otherwise None.
    """
    path = os.path.join(SAVE_DIR, f"{tid}.json")
    if not os.path.exists(path):
        return None

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def list_topologies() -> List[str]:
    """
    List all saved topology IDs.

    Returns:
        A list of topology IDs (filenames without .json).
    """
    return [
        fname[:-5]
        for fname in os.listdir(SAVE_DIR)
        if fname.endswith(".json")
    ]
