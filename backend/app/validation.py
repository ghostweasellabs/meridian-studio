from typing import Dict, List, Set

from pydantic import BaseModel

from .models import GraphDefinition


class ValidationError(BaseModel):
    location: str
    message: str


class ValidationResponse(BaseModel):
    valid: bool
    errors: List[ValidationError]


def validate_graph(graph: GraphDefinition) -> ValidationResponse:
    errors: List[ValidationError] = []
    node_ids: Set[str] = set()
    for n in graph.nodes:
        if n.id in node_ids:
            errors.append(ValidationError(location=f"node:{n.id}", message="Duplicate node id"))
        node_ids.add(n.id)
    # Edge endpoints exist
    for e in graph.edges:
        if e.source_node not in node_ids:
            errors.append(ValidationError(location=f"edge:{e.id}", message="Missing source node"))
        if e.target_node not in node_ids:
            errors.append(ValidationError(location=f"edge:{e.id}", message="Missing target node"))
    # Acyclicity via DFS (simple)
    adj: Dict[str, List[str]] = {}
    for e in graph.edges:
        adj.setdefault(e.source_node, []).append(e.target_node)
    visiting: Set[str] = set()
    visited: Set[str] = set()

    def dfs(u: str) -> bool:
        if u in visiting:
            return True
        if u in visited:
            return False
        visiting.add(u)
        for v in adj.get(u, []):
            if dfs(v):
                return True
        visiting.remove(u)
        visited.add(u)
        return False

    for n in node_ids:
        if dfs(n):
            errors.append(ValidationError(location="graph", message="Cycle detected"))
            break

    return ValidationResponse(valid=len(errors) == 0, errors=errors)
