import asyncio

import respx
from httpx import Response

from app.services import abha_client


def test_login_request_otp_sends_x_cm_id_and_required_headers(monkeypatch):
    """Regression: abha_client must include the mandatory ABDM X-CM-ID header."""

    async def _fake_token() -> str:
        return "dummy-token"

    monkeypatch.setattr(abha_client, "get_gateway_token", _fake_token)
    monkeypatch.setattr(abha_client, "_iso_now", lambda: "2024-01-01T00:00:00.000Z")

    payload = {
        "scope": ["abha-login"],
        "loginHint": "abha-number",
        "loginId": "encrypted-abha",
        "otpSystem": "abdm",
    }

    with respx.mock:
        route = respx.post(
            "https://abhasbx.abdm.gov.in/abha/api/v3/profile/login/request/otp"
        ).mock(return_value=Response(200, json={"txnId": "txn-123"}))

        result = asyncio.run(
            abha_client.post("/profile/login/request/otp", payload)
        )

        assert result["txnId"] == "txn-123"
        assert route.call_count == 1
        request = route.calls[0].request
        assert request.headers["X-CM-ID"] == "sbx"
        assert request.headers["Authorization"] == "Bearer dummy-token"
        assert request.headers["Content-Type"] == "application/json"
        assert "REQUEST-ID" in request.headers
        assert "TIMESTAMP" in request.headers
