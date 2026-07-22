"""ABHA verification (VRFY_ABHA_1xx–4xx): ABHA number / Aadhaar / mobile OTP login."""
from fastapi import APIRouter
from app.schemas.abha import LoginOtpRequest, LoginVerify
from app.services import abha_client
from app.services.abha_crypto import encrypt_sensitive

router = APIRouter()

_SCOPE = {
    ("abha-number", "aadhaar"): ["abha-login", "aadhaar-verify"],
    ("abha-number", "abdm"): ["abha-login", "mobile-verify"],
    ("aadhaar", "aadhaar"): ["abha-login", "aadhaar-verify"],
    ("mobile", "abdm"): ["abha-login", "mobile-verify"],
}


@router.post("/request-otp")
async def login_request_otp(body: LoginOtpRequest):
    payload = {
        "scope": _SCOPE.get((body.login_hint, body.otp_system), ["abha-login"]),
        "loginHint": body.login_hint,
        "loginId": await encrypt_sensitive(body.value),
        "otpSystem": body.otp_system,
    }
    return await abha_client.post("/profile/login/request/otp", payload)


@router.post("/verify")
async def login_verify(body: LoginVerify):
    payload = {
        "scope": ["abha-login"],
        "authData": {"authMethods": ["otp"], "otp": {"txnId": body.txn_id, "otpValue": await encrypt_sensitive(body.otp)}},
    }
    return await abha_client.post("/profile/login/verify", payload)


@router.post("/verify-user")
async def login_verify_user(txn_id: str, abha_number: str, t_token: str):
    """Mobile-login flow: pick one ABHA from the list linked to the mobile."""
    payload = {"ABHANumber": abha_number, "txnId": txn_id}
    return await abha_client.post("/profile/login/verify/user", payload, extra_headers={"T-token": f"Bearer {t_token}"})
