"""ABDM gateway session token — cached in Redis, refreshed before expiry."""
import httpx
import uuid
from datetime import datetime, timezone
from tenacity import retry, stop_after_attempt, wait_exponential
from app.core.config import settings
from app.core.redis import get_redis

TOKEN_KEY = "abdm:gateway:token"


def _iso_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def gateway_headers() -> dict:
    return {
        "REQUEST-ID": str(uuid.uuid4()),
        "TIMESTAMP": _iso_now(),
        "X-CM-ID": settings.ABDM_X_CM_ID,
        "Content-Type": "application/json",
    }


@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=8))
async def get_gateway_token() -> str:
    r = get_redis()
    token = await r.get(TOKEN_KEY)
    if token:
        return token
    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.post(
            f"{settings.ABDM_GATEWAY_BASE}/gateway/v3/sessions",
            headers=gateway_headers(),
            json={
                "clientId": settings.ABDM_CLIENT_ID,
                "clientSecret": settings.ABDM_CLIENT_SECRET,
                "grantType": "client_credentials",
            },
        )
        resp.raise_for_status()
        data = resp.json()
    token = data["accessToken"]
    ttl = max(int(data.get("expiresIn", 1200)) - 120, 60)   # refresh 2 min early
    await r.set(TOKEN_KEY, token, ex=ttl)
    return token
