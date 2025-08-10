import os
from typing import Optional

import asyncpg
from fastapi import APIRouter, Depends, HTTPException

from .auth import AuthenticatedUser, get_current_user

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@127.0.0.1:54322/postgres")

router = APIRouter(prefix="/sharing", tags=["sharing"])


@router.post("/graphs/{graph_id}/public", status_code=204)
async def make_public(graph_id: str, user: AuthenticatedUser = Depends(get_current_user)):
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        res = await conn.execute(
            "UPDATE graphs SET is_public = TRUE WHERE id = $1 AND user_id = $2",
            graph_id,
            user["user_id"],
        )
        if res.split(" ")[-1] == "0":
            raise HTTPException(status_code=404, detail="Graph not found")
        return None
    finally:
        await conn.close()


@router.post("/graphs/{graph_id}/private", status_code=204)
async def make_private(graph_id: str, user: AuthenticatedUser = Depends(get_current_user)):
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        res = await conn.execute(
            "UPDATE graphs SET is_public = FALSE WHERE id = $1 AND user_id = $2",
            graph_id,
            user["user_id"],
        )
        if res.split(" ")[-1] == "0":
            raise HTTPException(status_code=404, detail="Graph not found")
        return None
    finally:
        await conn.close()


@router.post("/graphs/{graph_id}/share", status_code=201)
async def share_graph(
    graph_id: str,
    shared_with: Optional[str] = None,
    permissions: str = "read",
    user: AuthenticatedUser = Depends(get_current_user),
):
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        # Ensure owner
        exists = await conn.fetchval(
            "SELECT 1 FROM graphs WHERE id = $1 AND user_id = $2", graph_id, user["user_id"]
        )
        if not exists:
            raise HTTPException(status_code=404, detail="Graph not found")
        await conn.execute(
            """
            INSERT INTO shared_graphs (graph_id, shared_by, shared_with, permissions)
            VALUES ($1, $2, $3, $4)
            """,
            graph_id,
            user["user_id"],
            shared_with,
            permissions,
        )
        return {"status": "ok"}
    finally:
        await conn.close()


@router.get("/graphs/{graph_id}")
async def list_shares(graph_id: str, user: AuthenticatedUser = Depends(get_current_user)):
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        rows = await conn.fetch(
            """
            SELECT id, shared_with, permissions, expires_at, created_at
            FROM shared_graphs
            WHERE graph_id = $1 AND shared_by = $2
            ORDER BY created_at DESC
            """,
            graph_id,
            user["user_id"],
        )
        return [dict(r) for r in rows]
    finally:
        await conn.close()


@router.get("/public")
async def list_public(search: Optional[str] = None, limit: int = 20, offset: int = 0):
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        if search:
            pattern = f"%{search}%"
            rows = await conn.fetch(
                """
                SELECT g.id, g.name, COALESCE(g.description,'') AS description,
                       g.tags, g.created_at, u.name AS owner_name, u.email AS owner_email
                FROM graphs g
                LEFT JOIN users u ON u.id = g.user_id
                WHERE g.is_public = TRUE
                  AND (g.name ILIKE $1 OR g.description ILIKE $1)
                ORDER BY g.created_at DESC
                LIMIT $2 OFFSET $3
                """,
                pattern,
                limit,
                offset,
            )
        else:
            rows = await conn.fetch(
                """
                SELECT g.id, g.name, COALESCE(g.description,'') AS description,
                       g.tags, g.created_at, u.name AS owner_name, u.email AS owner_email
                FROM graphs g
                LEFT JOIN users u ON u.id = g.user_id
                WHERE g.is_public = TRUE
                ORDER BY g.created_at DESC
                LIMIT $1 OFFSET $2
                """,
                limit,
                offset,
            )
        return [dict(r) for r in rows]
    finally:
        await conn.close()
