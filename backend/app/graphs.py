import json
import os
from typing import List, Optional

import asyncpg
from fastapi import APIRouter, Depends, HTTPException, status

from .auth import AuthenticatedUser, get_current_user
from .models import GraphDefinition

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@127.0.0.1:54322/postgres")

router = APIRouter(prefix="/graphs", tags=["graphs"])


@router.get("/", response_model=List[GraphDefinition])
async def list_graphs(
    user: AuthenticatedUser = Depends(get_current_user),
    search: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
):
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        if search:
            pattern = f"%{search}%"
            rows = await conn.fetch(
                """
                SELECT id, user_id, name, COALESCE(description,'') as description,
                       definition, is_public, tags, created_at, updated_at
                FROM graphs
                WHERE user_id = $1
                  AND (name ILIKE $2 OR description ILIKE $2)
                ORDER BY created_at DESC
                LIMIT $3 OFFSET $4
                """,
                user["user_id"],
                pattern,
                limit,
                offset,
            )
        else:
            rows = await conn.fetch(
                """
                SELECT id, user_id, name, COALESCE(description,'') as description,
                       definition, is_public, tags, created_at, updated_at
                FROM graphs
                WHERE user_id = $1
                ORDER BY created_at DESC
                LIMIT $2 OFFSET $3
                """,
                user["user_id"],
                limit,
                offset,
            )
        result: List[GraphDefinition] = []
        for r in rows:
            import json as _json

            d = (
                r["definition"]
                if isinstance(r["definition"], dict)
                else _json.loads(r["definition"]) if r["definition"] else {}
            )
            result.append(
                GraphDefinition(
                    id=str(r["id"]),
                    user_id=str(r["user_id"]),
                    name=r["name"],
                    description=r["description"],
                    nodes=d.get("nodes", []),
                    edges=d.get("edges", []),
                    metadata=d.get("metadata", {}),
                    is_public=r["is_public"],
                    tags=r["tags"] or [],
                    created_at=r["created_at"],
                    updated_at=r["updated_at"],
                )
            )
        return result
    finally:
        await conn.close()


@router.post("/", response_model=GraphDefinition, status_code=201)
async def create_graph(body: GraphDefinition, user: AuthenticatedUser = Depends(get_current_user)):
    if body.user_id != user["user_id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid owner")
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        await conn.execute(
            """
            INSERT INTO graphs (id, user_id, name, description, definition, is_public, tags)
            VALUES ($1, $2, $3, $4, $5::jsonb, $6, COALESCE($7::text[], ARRAY[]::text[]))
            """,
            body.id,
            body.user_id,
            body.name,
            body.description,
            json.dumps(
                {
                    "nodes": [n.model_dump() for n in body.nodes],
                    "edges": [e.model_dump() for e in body.edges],
                    "metadata": body.metadata,
                }
            ),
            body.is_public,
            body.tags,
        )
        row = await conn.fetchrow(
            "SELECT created_at, updated_at FROM graphs WHERE id = $1 AND user_id = $2",
            body.id,
            body.user_id,
        )
        body.created_at = row["created_at"]
        body.updated_at = row["updated_at"]
        return body
    finally:
        await conn.close()


@router.get("/{graph_id}", response_model=GraphDefinition)
async def get_graph(graph_id: str, user: AuthenticatedUser = Depends(get_current_user)):
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        r = await conn.fetchrow(
            """
            SELECT id, user_id, name, COALESCE(description,'') as description,
                   definition, is_public, tags, created_at, updated_at
            FROM graphs
            WHERE id = $1 AND user_id = $2
            """,
            graph_id,
            user["user_id"],
        )
        if not r:
            raise HTTPException(status_code=404, detail="Graph not found")
        import json as _json

        d = (
            r["definition"]
            if isinstance(r["definition"], dict)
            else _json.loads(r["definition"]) if r["definition"] else {}
        )
        return GraphDefinition(
            id=str(r["id"]),
            user_id=str(r["user_id"]),
            name=r["name"],
            description=r["description"],
            nodes=d.get("nodes", []),
            edges=d.get("edges", []),
            metadata=d.get("metadata", {}),
            is_public=r["is_public"],
            tags=r["tags"] or [],
            created_at=r["created_at"],
            updated_at=r["updated_at"],
        )
    finally:
        await conn.close()


@router.put("/{graph_id}", response_model=GraphDefinition)
async def update_graph(
    graph_id: str, body: GraphDefinition, user: AuthenticatedUser = Depends(get_current_user)
):
    if body.user_id != user["user_id"] or body.id != graph_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Mismatched ids")
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        r = await conn.fetchrow(
            """
            UPDATE graphs
            SET name = $3,
                description = $4,
                definition = $5,
                is_public = $6,
                tags = $7,
                updated_at = NOW()
            WHERE id = $1 AND user_id = $2
            RETURNING created_at, updated_at
            """,
            body.id,
            body.user_id,
            body.name,
            body.description,
            json.dumps(
                {
                    "nodes": [n.model_dump() for n in body.nodes],
                    "edges": [e.model_dump() for e in body.edges],
                    "metadata": body.metadata,
                }
            ),
            body.is_public,
            body.tags,
        )
        if not r:
            raise HTTPException(status_code=404, detail="Graph not found")
        body.created_at = r["created_at"]
        body.updated_at = r["updated_at"]
        return body
    finally:
        await conn.close()


@router.delete("/{graph_id}", status_code=204)
async def delete_graph(graph_id: str, user: AuthenticatedUser = Depends(get_current_user)):
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        res = await conn.execute(
            "DELETE FROM graphs WHERE id = $1 AND user_id = $2",
            graph_id,
            user["user_id"],
        )
        if res.split(" ")[-1] == "0":
            raise HTTPException(status_code=404, detail="Graph not found")
        return None
    finally:
        await conn.close()
