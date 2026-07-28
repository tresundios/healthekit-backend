"""Healthekit API entrypoint."""
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import configure_logging
from app.api.v1.router import api_router
from app.api.callbacks.router import callback_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    yield


app = FastAPI(
    title="Healthekit API",
    version="0.1.0",
    description="ABDM M1 — ABHA creation & verification. NHA/ABDM compliant.",
    lifespan=lifespan,
    docs_url="/docs" if settings.ENV != "prod" else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthz", tags=["health"])
async def healthz():
    return {"status": "ok", "env": settings.ENV}

@app.get("/readyz", tags=["health"])
async def readyz():
    from sqlalchemy import text
    from app.db.session import engine
    from app.core.redis import get_redis
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        await get_redis().ping()
    except Exception:
        raise HTTPException(status_code=503, detail="dependencies not ready")
    return {"status": "ready"}

app.include_router(api_router, prefix="/api/v1")
# ABDM gateway callbacks (bridge URL points here) — must stay at /api/v3/*
app.include_router(callback_router, prefix="/api/v3")
