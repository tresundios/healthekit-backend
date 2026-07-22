"""ABHA *address* verification via PHR web login (VRFY_ABHA_102 / 202)."""
from fastapi import APIRouter
from app.services import abha_client
from app.services.abha_crypto import encrypt_sensitive

router = APIRouter()


@router.post("/search")
async def search_auth_methods(abha_address: str):
    return await abha_client.post("/phr/web/login/abha/search", {"abhaAddress": abha_address})


@router.post("/request-otp")
async def address_request_otp(abha_address: str, otp_system: str = "aadhaar"):
    scope = ["abha-address-login", "aadhaar-verify" if otp_system == "aadhaar" else "mobile-verify"]
    payload = {
        "scope": scope,
        "loginHint": "abha-address",
        "loginId": await encrypt_sensitive(abha_address),
        "otpSystem": otp_system,
    }
    return await abha_client.post("/phr/web/login/abha/request/otp", payload)


@router.post("/verify")
async def address_verify(txn_id: str, otp: str):
    payload = {
        "scope": ["abha-address-login"],
        "authData": {"authMethods": ["otp"], "otp": {"txnId": txn_id, "otpValue": await encrypt_sensitive(otp)}},
    }
    return await abha_client.post("/phr/web/login/abha/verify", payload)


@router.get("/profile")
async def address_profile(x_token: str):
    return await abha_client.get("/phr/web/login/profile/abha-profile", extra_headers={"X-token": f"Bearer {x_token}"})


@router.get("/card")
async def phr_card(x_token: str):
    return await abha_client.get("/phr/web/login/profile/abha/phr-card", extra_headers={"X-token": f"Bearer {x_token}"}, raw=True)
