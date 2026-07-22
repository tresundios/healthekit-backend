# Healthekit Backend (FastAPI) — ABDM M1

Healthcare SaaS backend for **healthekit.in** by Tresundios Software.
Milestone 1: ABHA creation & verification (ABDM Sandbox, NHA compliant).

- Docs: see `docs/` (PRD, SRS, Architecture, Endpoints, Setup — living documents)
- Agent rules: `.windsurf/rules/` (Windsurf/Devin/Claude must read these first)
- Sandbox bridge ID: `SBXID_043801` (secret NEVER committed — env/Jenkins credentials only)

## Quickstart (local Mac)
```bash
cp envs/.env.local .env
docker compose -f deploy/docker-compose.local.yml up -d postgres redis
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

```
docker compose -f deploy/docker-compose.local-full.yml up --build
```

OpenAPI: http://localhost:8000/docs
