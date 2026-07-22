"""RSA-OAEP(SHA-1) encryption of Aadhaar / OTP with the ABHA public certificate.

ABHA V3 requires sensitive fields (Aadhaar number, OTP) encrypted with the
public key from GET {ABHA_BASE}/profile/public/certificate.
"""
import base64
import httpx
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from app.core.config import settings
from app.core.redis import get_redis

CERT_KEY = "abdm:abha:public_key_pem"


async def _public_key_pem() -> str:
    r = get_redis()
    pem = await r.get(CERT_KEY)
    if pem:
        return pem
    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.get(f"{settings.ABHA_BASE}/profile/public/certificate")
        resp.raise_for_status()
        pem = resp.json()["publicKey"]
    if "BEGIN PUBLIC KEY" not in pem:
        pem = f"-----BEGIN PUBLIC KEY-----\n{pem}\n-----END PUBLIC KEY-----"
    await r.set(CERT_KEY, pem, ex=6 * 3600)
    return pem


async def encrypt_sensitive(value: str) -> str:
    pem = await _public_key_pem()
    key = serialization.load_pem_public_key(pem.encode())
    ct = key.encrypt(
        value.encode(),
        padding.OAEP(mgf=padding.MGF1(hashes.SHA1()), algorithm=hashes.SHA1(), label=None),
    )
    return base64.b64encode(ct).decode()
