# Backend Coding Standards

- Python 3.12, full type hints, `ruff` clean, `mypy` clean before commit.
- Async everywhere on the request path (`async def`, httpx.AsyncClient, SQLAlchemy async session).
- Pydantic v2 schemas for every request/response body; validation rules mirror NHA test cases (Aadhaar 12 digits, OTP 6 digits, ABHA address 8–18 chars with dot/underscore rules).
- Errors: raise `HTTPException` with machine-readable `detail.code`; map upstream ABDM errors to user-friendly messages listed in docs/ENDPOINTS.md.
- structlog JSON logging; include request-id; NEVER log Aadhaar, OTP, tokens, or full profile payloads.
- Tests: pytest per router + service; mock ABDM with `respx`. Target ≥80% on `app/services` and `app/api`.
- Conventional Commits (`feat:`, `fix:`, `docs:`...). One feature per PR.
