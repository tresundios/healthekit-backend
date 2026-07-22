# Setup Guide (step by step)

## 0. Accounts & prerequisites
AWS account (region **ap-south-1 Mumbai** — data residency), Docker Hub `navistresundios`, GitHub org, hioxindia DNS panel for healthekit.in, ABDM sandbox login.

## 1. Local Mac
1. Install: Docker Desktop, Python 3.12, Node 20 (nvm), git.
2. `git clone` both repos; backend: `cp envs/.env.local .env`, put the real ABDM secret in `.env` only.
3. `docker compose -f deploy/docker-compose.local.yml up -d` (postgres+redis) → `alembic upgrade head` → `uvicorn app.main:app --reload`.
4. Frontend: `npm i && npm run dev` → http://localhost:5173 (proxy to :8000 configured in vite.config.ts).

## 2. AWS baseline (once)
1. VPC (default ok for dev/qa), key pair `healthekit-ops`, security groups: `sg-web` (80/443 from 0.0.0.0), `sg-ssh` (22 from office IP), `sg-db` (5432/6379 from app SG only).
2. Elastic IPs: one per env app box + Jenkins.
3. EC2 Ubuntu 24.04: jenkins t3.medium/30GB; dev t3.medium/30GB; qa t3.medium; uat-app t3.medium + uat-db t3.small; prod later (ALB+2×app+RDS).
4. Run `deploy/scripts/provision-ec2.sh` on each app box.

## 3. DNS on hioxindia (see blueprint HTML §7 for both options)
Add A records → Elastic IPs: dev, api.dev, qa, api.qa, uat, api.uat, ci. Prod later: ALB alias (needs Route 53 delegation or CNAME on www + redirect).

## 4. TLS
Lower envs: `sudo certbot certonly --standalone -d api.dev.healthekit.in -d dev.healthekit.in` (repeat per env box; auto-renew via systemd timer). Prod: ACM cert `*.healthekit.in` + `healthekit.in` attached to ALB.

## 5. Jenkins
1. Install plugins: Docker Pipeline, SSH Agent, Git, Credentials Binding, Blue Ocean.
2. Credentials: `dockerhub-navistresundios` (user/pass), `healthekit-<env>-ssh` (SSH key), `abdm-client-secret` (secret text), GitHub app/token.
3. Multibranch pipeline per repo pointing at the Jenkinsfile; host files `/var/jenkins_home/hosts/<env>-app.host` contain each env IP.

## 6. ABDM sandbox wiring
1. Session: POST /gateway/v3/sessions with SBXID_043801 + secret.
2. Set bridge URL: PATCH /gateway/v3/bridge/url → `https://api.dev.healthekit.in`.
3. Register HIP/HIU services: POST facilitysbx …/MutipleHRPAddUpdateServices (choose ids e.g. `HEK_HIP`, `HEK_HIU`).
4. Verify: GET /gateway/v3/bridge-services. Reply to integration.support@nha.gov.in to close ticket.

## 7. Deploy order per env
Backend image → migrate (`docker compose run api alembic upgrade head`) → frontend image → smoke `https://api.<env>.healthekit.in/healthz`.

## 8. M1 submission
Record functional test evidence against the NHA sheet on **qa**, submit demo URLs `https://qa.healthekit.in` + bridge at `https://api.dev.healthekit.in` (or move bridge to qa), export updated Postman env, submit via sandbox portal → Milestone_one docs page.
