"""ABHA profile: details, card, QR (post-login, needs X-token from verify)."""
from fastapi import APIRouter, Response
from app.services import abha_client

router = APIRouter()


@router.get("")
async def get_profile(x_token: str):
    return await abha_client.get("/profile/account", extra_headers={"X-token": f"Bearer {x_token}"})


@router.get("/card")
async def get_abha_card(x_token: str):
    content = await abha_client.get("/profile/account/abha-card", extra_headers={"X-token": f"Bearer {x_token}"}, raw=True)
    return Response(content=content, media_type="image/png")


@router.get("/qr")
async def get_qr(x_token: str):
    return await abha_client.get("/profile/account/qrCode", extra_headers={"X-token": f"Bearer {x_token}"})
