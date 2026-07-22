# Healthekit — Project Context (read first)

- Product: **Healthekit.in** — Healthcare SaaS by Tresundios Software, integrating with India's ABDM (Ayushman Bharat Digital Mission) under NHA guidelines.
- Current goal: **Milestone 1 (M1)** — ABHA creation & verification against ABDM Sandbox. M2 (HIP link/care contexts), M3 (HIU consent+fetch), M4 come later; design for extension, implement only M1.
- Stack: FastAPI (Python 3.12) · PostgreSQL 16 · Redis 7 · React 18 + TypeScript + Vite · Docker · Jenkins · Docker Hub (`navistresundios/*`) · AWS EC2.
- Environments: local (Mac) → dev → qa → uat → prod. Domains: `api.<env>.healthekit.in` / `<env>.healthekit.in`; prod: `api.healthekit.in` / `healthekit.in`.
- Sandbox: gateway `https://dev.abdm.gov.in/api/hiecm`, ABHA `https://abhasbx.abdm.gov.in/abha/api/v3`, X-CM-ID `sbx`, client id `SBXID_043801`. The client secret exists only in `.env` (untracked) and Jenkins credentials.
- Living docs live in `docs/` — update PRD/SRS/ENDPOINTS when behavior changes. Full product feature set is NOT final; keep modules pluggable with clear placeholders.
