from datetime import datetime
from typing import Any, Dict, List

from pydantic import BaseModel, Field


class Position(BaseModel):
    x: float
    y: float


class NodeDefinition(BaseModel):
    id: str
    type: str
    name: str
    position: Position
    properties: Dict[str, Any] = Field(default_factory=dict)


class EdgeDefinition(BaseModel):
    id: str
    source_node: str
    source_port: str
    target_node: str
    target_port: str
    capacity: int = 1024
    policy: str = "BLOCK"
    priority: int = 0


class GraphDefinition(BaseModel):
    id: str
    name: str
    description: str
    nodes: List[NodeDefinition]
    edges: List[EdgeDefinition]
    metadata: Dict[str, Any] = Field(default_factory=dict)
    user_id: str
    is_public: bool = False
    tags: List[str] = Field(default_factory=list)
    created_at: datetime | None = None
    updated_at: datetime | None = None
