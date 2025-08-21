# backend/app/models.py
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class Node(BaseModel):
    id: str
    x: Optional[float] = None
    y: Optional[float] = None
    label: Optional[str] = None

class Edge(BaseModel):
    source: str
    target: str
    weight: float = 1.0

class Graph(BaseModel):
    nodes: List[Node]
    edges: List[Edge]

class GraphRequest(BaseModel):
    nodes: List[Node]
    edges: List[Edge]
    algorithm: str
    source: str
    target: str
    options: Optional[Dict[str, Any]] = None

class ShortestPathResponse(BaseModel):
    path: List[str]
    steps: Optional[List[Dict[str, Any]]] = None
    metrics: Optional[Dict[str, Any]] = None

class SaveRequest(BaseModel):
    id: str
    topology: Graph
