# Claude / Devin Prompting Playbook for Healthekit

## Session opener (paste first in every session)
> You are working on Healthekit (ABDM M1). Read `.windsurf/rules/*` and `docs/ENDPOINTS.md` before any change. Strict layering (api→services→db), no secrets, docs-with-code. Confirm the rules you'll apply, then proceed.

## Feature prompt template
> Implement <FR-x / NHA id> per docs/SRS.md §<n>. Constraints: async, pydantic v2 schemas, respx-mocked tests, update ENDPOINTS.md. Show plan → diff → tests. Do not touch unrelated files.

## Good task-sized prompts (examples)
- "Wire ConsentLog persistence into /abha/enrollment/aadhaar/request-otp per FR-7.1; add migration; tests for consent row creation."
- "Add Redis rate limit 3/min to all *request-otp* endpoints (NFR-4) as a FastAPI dependency; unit tests with fakeredis."
- "Build frontend Aadhaar OTP wizard (steps: consent → aadhaar → otp → mobile → address → success) using the existing api client; follow NHA UX rules in .windsurf/rules/30."

## Review prompt
> Review this diff against .windsurf/rules 10/20/30/40. List violations with file:line, then fix.

## Anti-patterns to forbid in prompts
Don't let the agent: call httpx in routers, log OTP/Aadhaar, create tables without Alembic, invent ABDM payloads (always cite the Postman collection / Integrator Guide v1.4).
