"""ABHA creation via Aadhaar OTP (CRT_ABHA_1xx) + address selection."""
from fastapi import APIRouter
from app.schemas.abha import AadhaarOtpRequest, EnrolByAadhaarRequest, MobileOtpVerify, AbhaAddressCreate
from app.services import abha_client
from app.services.abha_crypto import encrypt_sensitive

router = APIRouter()


@router.post("/aadhaar/request-otp")
async def request_aadhaar_otp(body: AadhaarOtpRequest):
    """Step 1 — send OTP to Aadhaar-linked mobile. Also logs consent (TODO persist ConsentLog)."""
    payload = {
        "txnId": "",
        "scope": ["abha-enrol"],
        "loginHint": "aadhaar",
        "loginId": await encrypt_sensitive(body.aadhaar),
        "otpSystem": "aadhaar",
    }
    return await abha_client.post("/enrollment/request/otp", payload)


@router.post("/aadhaar/enrol")
async def enrol_by_aadhaar(body: EnrolByAadhaarRequest):
    """Step 2 — verify OTP, create ABHA."""
    payload = {
        "authData": {
            "authMethods": ["otp"],
            "otp": {"txnId": body.txn_id, "otpValue": await encrypt_sensitive(body.otp), "mobile": body.mobile},
        },
        "consent": {"code": "abha-enrollment", "version": "1.4"},
    }
    return await abha_client.post("/enrollment/enrol/byAadhaar", payload)


@router.post("/mobile/request-otp")
async def request_mobile_otp(txn_id: str, mobile: str):
    """Communication-mobile verification when it differs from Aadhaar mobile."""
    payload = {
        "txnId": txn_id,
        "scope": ["abha-enrol", "mobile-verify"],
        "loginHint": "mobile",
        "loginId": await encrypt_sensitive(mobile),
        "otpSystem": "abdm",
    }
    return await abha_client.post("/enrollment/request/otp", payload)


@router.post("/mobile/verify-otp")
async def verify_mobile_otp(body: MobileOtpVerify):
    payload = {
        "scope": ["abha-enrol", "mobile-verify"],
        "authData": {"authMethods": ["otp"], "otp": {"txnId": body.txn_id, "otpValue": await encrypt_sensitive(body.otp)}},
    }
    return await abha_client.post("/enrollment/auth/byAbdm", payload)


@router.get("/address/suggestions")
async def abha_address_suggestions(txn_id: str):
    return await abha_client.get("/enrollment/enrol/suggestion", extra_headers={"TRANSACTION_ID": txn_id})


@router.post("/address")
async def set_abha_address(body: AbhaAddressCreate):
    payload = {"txnId": body.txn_id, "abhaAddress": body.abha_address, "preferred": body.preferred}
    return await abha_client.post("/enrollment/enrol/abha-address", payload)


# Placeholder — M1 optional flows to be wired later:
#   POST /document           (enrol byDocument — DL/PAN)
#   POST /biometric/enrol    (byAadhaar with fingerprint/face/iris PID block)
