# Git & CI/CD Rules

- Branches: `main` (prod), `uat`, `qa`, `develop` (dev). Feature branches `feat/<ticket>` off `develop`, PR back with review.
- Promotion is by merging upward develop → qa → uat → main; Jenkins deploys the merged branch to its env. Prod deploys are manual-approval.
- Docker tags are immutable: `<env>-<build>-<gitsha>`; `latest` only mirrors prod.
- Jenkinsfile stages must stay: Lint&Test → Build → Push → Deploy → Smoke. A red smoke test rolls back (`docker compose up -d api` with previous tag).
- Never deploy from a laptop. Never `docker push` by hand except break-glass, documented in docs/RUNBOOK notes.
