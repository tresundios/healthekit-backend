# Architecture Rules

1. Layering is strict: `api` (routers) → `services` (ABDM clients, business logic) → `models/db`. Routers never call httpx directly.
2. Every ABDM call goes through `services/abha_client.py` or `services/abdm_session.py`; headers (REQUEST-ID uuid, ISO TIMESTAMP, Bearer gateway token) are set in one place only.
3. Gateway session tokens are cached in Redis with early refresh; never fetch a token per request.
4. Sensitive fields (Aadhaar, OTP) are RSA-OAEP encrypted via `services/abha_crypto.py` before leaving the app. Never log them, never store raw Aadhaar in DB.
5. One ABHA number links to exactly one patient (`uq_abha_number_single_patient`). Check before insert; return 409 with existing patient id.
6. ABDM gateway callbacks stay under `/api/v3/*` (bridge URL contract). Internal product APIs live under `/api/v1/*`.
7. All new tables via Alembic migration — never `create_all` outside tests.
8. Config only via `app/core/config.py` (pydantic-settings). No `os.environ` reads elsewhere. No secrets in code, ever.
9. Placeholders for future milestones are explicit: a stub router + `# M2:`/`# M3:` comment, not dead code.
