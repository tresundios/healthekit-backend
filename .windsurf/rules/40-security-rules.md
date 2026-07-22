# Security Rules

- Secrets only in `.env` (untracked), Jenkins credentials, or AWS SSM Parameter Store. If a secret is ever committed, rotate it immediately.
- HTTPS everywhere; bridge URL must have a valid public cert (Let's Encrypt for dev/qa/uat, ACM at ALB for prod).
- JWT for our own sessions (HS256, 60 min); ABDM X-token/T-token are pass-through, held client-side or Redis with TTL, never in Postgres.
- Rate-limit OTP endpoints (Redis counter: 3/min/mobile) to prevent abuse.
- CORS locked to the env's own web origin.
- Dependencies pinned; run `pip audit` / `npm audit` in CI.
- DB backups nightly (pg_dump to S3, 30-day retention); test restore quarterly.
