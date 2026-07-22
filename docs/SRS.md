# Healthekit — Software Requirements Specification (SRS)
> **Living document.** IEEE-830-lite structure. Update with every behavioral change.

## Revision History
| Date | Version | Change |
|---|---|---|
| 2026-07-22 | 0.1 | Initial M1 SRS |

## 1. Introduction
**Purpose:** Define functional & non-functional requirements for Healthekit M1 (ABHA creation & verification) integrating ABDM Sandbox V3 APIs.
**Scope:** Backend (FastAPI), Frontend (React TS), infra (AWS EC2, Docker, Jenkins). Excludes M2–M4 behavior.
**References:** ABDM ABHA V3 Integrator Guide v1.4 (31-07-2025); NHA M1 test sheet (ABHA Creation & Verification v1.1); Milestone 1 Postman collection (18-08-2025); Scan & Share collection (14-08-2025).

## 2. Overall Description
Healthekit backend is a stateless FastAPI service that (a) proxies/orchestrates ABHA V3 APIs with gateway session auth + RSA field encryption, (b) maintains a patient registry with ABHA tagging, consent and audit logs in PostgreSQL, (c) receives ABDM gateway callbacks at the registered bridge URL, (d) serves a React SPA. Redis caches gateway tokens, ABHA public certs, OTP rate counters and Scan & Share running tokens.

## 3. Functional Requirements
### FR-1 ABDM Session
- FR-1.1 Obtain gateway token via POST /gateway/v3/sessions with clientId/secret; cache in Redis; refresh 120 s before expiry.
- FR-1.2 All ABDM calls carry REQUEST-ID (uuid v4), TIMESTAMP (ISO-8601 UTC), Authorization Bearer; enrolment/profile calls to abhasbx host.

### FR-2 ABHA Enrollment (Aadhaar OTP)
- FR-2.1 POST /api/v1/abha/enrollment/aadhaar/request-otp — validate Aadhaar (12 digits), record consent, call enrollment/request/otp with RSA-encrypted Aadhaar. Error: "Aadhaar Number is not valid".
- FR-2.2 POST …/aadhaar/enrol — verify 6-digit OTP (encrypted) + communication mobile via enrollment/enrol/byAadhaar; returns ABHA profile + tokens.
- FR-2.3 Mobile differs from Aadhaar mobile → …/mobile/request-otp + …/mobile/verify-otp (auth/byAbdm).
- FR-2.4 GET …/address/suggestions (TRANSACTION_ID header); POST …/address sets ABHA address (validation: 8–18, ≤1 dot, ≤1 underscore, not edge).
- FR-2.5 Resend OTP allowed max 2×, 60 s cooldown (Redis-enforced).

### FR-3 ABHA Verification
- FR-3.1 Login OTP: POST /api/v1/abha/login/request-otp with loginHint ∈ {abha-number, aadhaar, mobile}, otpSystem ∈ {aadhaar, abdm}; verify via …/login/verify.
- FR-3.2 Mobile flow: after verify, list linked ABHAs; POST …/login/verify-user with chosen ABHANumber + T-token.
- FR-3.3 ABHA address verification via /api/v1/abha/address/* (phr web login search/request-otp/verify/profile/card).
- FR-3.4 On success fetch profile (X-token), persist/patch patient, link ABHA.

### FR-4 Profile
- FR-4.1 GET /api/v1/abha/profile, /card (PNG), /qr with X-token pass-through.
- FR-4.2 Name/DOB/gender immutable in Healthekit UI & API.

### FR-5 Patient Registry & Tagging
- FR-5.1 POST /api/v1/patients creates patient (auto MRN HEKxxxxxxxx) and optional ABHA link.
- FR-5.2 Unique constraint on abha_number; duplicate → 409 ABHA_ALREADY_LINKED with existing patient id.
- FR-5.3 GET /api/v1/patients/by-abha/{n}.

### FR-6 Scan & Share (bridge callbacks)
- FR-6.1 POST /api/v3/hip/patient/share (bridge URL) — accept profile, ACK 202-style immediately.
- FR-6.2 Background ACK to /patient-share/v3/on-share with SUCCESS, incrementing tokenNumber (Redis), expiry 1800 s.
- FR-6.3 GET running-token status endpoints (on-status responder) — placeholder for counter display.

### FR-7 Consent & Audit
- FR-7.1 ConsentLog row (purpose, version, language, timestamp) before any Aadhaar/ABHA operation.
- FR-7.2 AuditLog for create/verify/link/share actions.

## 4. Non-Functional Requirements
| ID | Requirement |
|---|---|
| NFR-1 | All traffic HTTPS; bridge URL valid public cert |
| NFR-2 | PHI at rest in ap-south-1 only; encrypted EBS/RDS; no raw Aadhaar stored |
| NFR-3 | P95 API latency (excl. ABDM upstream) < 300 ms |
| NFR-4 | OTP endpoints rate-limited 3/min per identifier |
| NFR-5 | JSON structured logs, request-id correlation; no PII in logs |
| NFR-6 | 99.5% availability target prod; health/readiness probes |
| NFR-7 | Backups nightly, RPO 24 h, RTO 4 h (M1) |
| NFR-8 | OWASP ASVS L1; dependency audit in CI |

## 5. Data Model (M1)
patients(id, mrn✻, full_name, gender, dob, mobile, address, created_at) · abha_links(id, patient_id→patients, abha_number✻unique, abha_address, kyc_verified, linked_at) · consent_logs(id, patient_id?, purpose, consent_version, language, accepted_at) · audit_logs(id, actor, action, entity, detail, at)

## 6. External Interfaces
See docs/ENDPOINTS.md for the full upstream/internal endpoint matrix (living).

## 7. Traceability
Every FR maps to NHA test IDs listed in PRD §5; ENDPOINTS.md carries the row-level mapping.
