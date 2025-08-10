from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
import asyncpg
import os
from .auth import get_current_user, AuthenticatedUser

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@127.0.0.1:54322/postgres")

router = APIRouter(prefix="/users", tags=["users"])

class UpdateProfileRequest(BaseModel):
    name: str | None = None
    avatar_url: str | None = None

@router.get("/me")
async def get_profile(user: AuthenticatedUser = Depends(get_current_user)):
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        row = await conn.fetchrow(
            "SELECT id, email, name, avatar_url, created_at, updated_at FROM users WHERE id = $1",
            user["user_id"],
        )
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return {"user": dict(row)}
    finally:
        await conn.close()

@router.put("/me")
async def update_profile(body: UpdateProfileRequest, user: AuthenticatedUser = Depends(get_current_user)):
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        row = await conn.fetchrow(
            """
            UPDATE users
            SET name = COALESCE($2, name),
                avatar_url = COALESCE($3, avatar_url),
                updated_at = NOW()
            WHERE id = $1
            RETURNING id, email, name, avatar_url, created_at, updated_at
            """,
            user["user_id"], body.name, body.avatar_url
        )
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return {"user": dict(row)}
    finally:
        await conn.close()
