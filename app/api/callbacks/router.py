"""ABDM gateway callbacks. Bridge URL must point at this app over valid HTTPS.

Scan & Share flow: patient scans facility QR in PHR app -> gateway POSTs
profile to /api/v3/hip/patient/share -> we ACK via /patient-share/v3/on-share
with a token number (30 min validity).
"""
import uuid
import httpx
from fastapi import APIRouter, Request, BackgroundTasks
from app.core.config import settings
from app.core.redis import get_redis
from app.services.abdm_session import get_gateway_token, gateway_headers

callback_router = APIRouter()


async def _ack_on_share(request_id: str, abha_address: str) -> None:
    r = get_redis()
    token_no = await r.incr("scan_share:running_token")
    headers = gateway_headers()
    headers["Authorization"] = f"Bearer {await get_gateway_token()}"
    payload = {
        "acknowledgement": {
            "status": "SUCCESS",
            "abhaAddress": abha_address,
            "profile": {"context": "1", "tokenNumber": str(token_no).zfill(2), "expiry": 1800},
        },
        "response": {"requestId": request_id},
    }
    async with httpx.AsyncClient(timeout=15) as client:
        await client.post(f"{settings.ABDM_GATEWAY_BASE}/patient-share/v3/on-share", json=payload, headers=headers)


@callback_router.post("/hip/patient/share", tags=["ABDM Callbacks"])
async def patient_share(request: Request, background: BackgroundTasks):
    body = await request.json()
    request_id = request.headers.get("REQUEST-ID", str(uuid.uuid4()))
    profile = body.get("profile", {}).get("patient", {})
    # TODO: persist shared profile, create/match patient, show token on registration desk screen
    background.add_task(_ack_on_share, request_id, profile.get("abhaAddress", ""))
    return {"status": "ACCEPTED"}
