"""Thin async client over ABHA V3 sandbox APIs used in Milestone 1."""
import uuid
import httpx
import logging
from app.core.config import settings
from app.services.abdm_session import get_gateway_token, _iso_now


async def _headers(extra: dict | None = None) -> dict:
    h = {
        "REQUEST-ID": str(uuid.uuid4()),
        "TIMESTAMP": _iso_now(),
        "X-CM-ID": settings.ABDM_X_CM_ID,
        "Authorization": f"Bearer {await get_gateway_token()}",
        "Content-Type": "application/json",
    }
    if extra:
        h.update(extra)
    return h


async def post(path: str, payload: dict, extra_headers: dict | None = None) -> dict:
    base = settings.ABHA_BASE.rstrip('/')
    logging.info(f"ABHA call: POST {base}{path}")
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(f"{base}{path}", json=payload, headers=await _headers(extra_headers))
        resp.raise_for_status()
        return resp.json()


async def get(path: str, extra_headers: dict | None = None, raw: bool = False):
    base = settings.ABHA_BASE.rstrip('/')
    logging.info(f"ABHA call: GET {base}{path}")
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.get(f"{base}{path}", headers=await _headers(extra_headers))
        resp.raise_for_status()
        return resp.content if raw else resp.json()
