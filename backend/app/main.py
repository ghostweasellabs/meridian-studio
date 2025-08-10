import os

import asyncpg
import redis.asyncio as aioredis
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .auth import AuthenticatedUser, get_current_user
from .graphs import router as graphs_router
from .models import GraphDefinition
from .sharing import router as sharing_router
from .users import router as users_router
from .validation import ValidationResponse, validate_graph

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@127.0.0.1:54322/postgres")
REDIS_URL = os.getenv("REDIS_URL", "redis://127.0.0.1:6379")

app = FastAPI(title="Meridian Studio API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/health/db")
async def health_db():
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        try:
            val = await conn.fetchval("SELECT 1")
        finally:
            await conn.close()
        return {"status": "ok", "db": True, "val": val}
    except Exception as exc:  # noqa: BLE001
        return {"status": "error", "db": False, "error": str(exc)}


@app.get("/health/redis")
async def health_redis():
    try:
        client = aioredis.from_url(REDIS_URL)
        pong = await client.ping()
        await client.close()
        return {"status": "ok", "redis": pong}
    except Exception as exc:  # noqa: BLE001
        return {"status": "error", "redis": False, "error": str(exc)}


@app.get("/me")
async def me(user: AuthenticatedUser = Depends(get_current_user)):
    return {"user": user}


app.include_router(users_router)
app.include_router(graphs_router)
app.include_router(sharing_router)


@app.post("/graphs/validate", response_model=ValidationResponse)
async def validate(graph: GraphDefinition):
    return validate_graph(graph)
