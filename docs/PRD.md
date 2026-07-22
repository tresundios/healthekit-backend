# Healthekit — Product Requirements Document (PRD)
> **Living document** — update Revision History on every change.

| Field | Value |
|---|---|
| Product | Healthekit.in — Healthcare SaaS |
| Company | Tresundios Software |
| Version | 0.1 (M1 scope) |
| Owner | Navis Michael Bearly |
| Status | Draft — M1 |

## Revision History
| Date | Version | Author | Change |
|---|---|---|---|
| 2026-07-22 | 0.1 | Bootstrap | Initial M1 PRD |

## 1. Vision
Healthekit is an ABDM-compliant healthcare SaaS for Indian healthcare providers. It lets facilities register patients with verified digital health identities (ABHA), and — in later milestones — link, share, and consume longitudinal health records over the ABDM network. Full product feature set is **not yet finalized**; this PRD grows milestone by milestone.

## 2. Goals (M1)
1. Pass NHA Milestone 1 functional testing: ABHA creation & verification.
2. Establish the ABDM sandbox bridge (SBXID_043801) with a public HTTPS endpoint.
3. Ship the platform skeleton (auth, patient registry, audit, consent logging) reusable for M2–M4.

## 3. Non-Goals (M1)
- HIP care-context linking (M2), consent manager / HIU flows (M3), advanced HIMS features (billing, OPD queue, EMR) — placeholders only.
- Aadhaar biometric capture via RD devices (stub only; needs registered devices).

## 4. Users & Personas
| Persona | Description | M1 needs |
|---|---|---|
| Front-desk operator | Facility registration desk | Create/verify ABHA, tag to patient MRN, show Scan & Share token |
| Patient / beneficiary | Person seeking care | Consent, OTP entry, view/download ABHA card |
| Facility admin (placeholder) | Manages facility, users | Post-M1 |
| Tresundios ops | Runs the SaaS | Health checks, logs, deploys |

## 5. M1 Feature List (traceable to NHA test sheet)
| # | Feature | NHA IDs | Priority |
|---|---|---|---|
| F1 | ABHA creation via Aadhaar OTP (consent → Aadhaar → OTP → mobile verify → address selection → ABHA display) | CRT_ABHA_101–113 | P0 |
| F2 | ABHA card view/download | CRT_ABHA_114 | P0 |
| F3 | ABHA verification via ABHA number (Aadhaar OTP / ABHA OTP) | VRFY_ABHA_101, 201 | P0 |
| F4 | ABHA address verification (PHR web login) | VRFY_ABHA_102, 202 | P0 |
| F5 | Verification via mobile → list ABHAs → verify-user | VRFY_ABHA_301–305 | P0 |
| F6 | Verification via Aadhaar number | VRFY_ABHA_401–405 | P0 |
| F7 | ABHA↔patient tagging, uniqueness enforced | TAGGING | P0 |
| F8 | Scan & Share: facility QR, profile callback, token issue | SHARE_701 | P0 |
| F9 | Enrol via DL/PAN document | CRT_ABHA_401–411 | P1 (stub) |
| F10 | Biometric enrol/verify (finger/face/iris) | CRT_ABHA_2xx, VRFY_ABHA_5xx | P2 (stub) |
| F11 | Profile updates (mobile/email/photo, re-KYC, delete) | PROF_ABHA_601–605 | P1 |

## 6. UX Requirements (from NHA sheet)
- Consent screen with ABDM-published text, versioned, multilingual-ready, explicit "I agree".
- OTP: 6 digits, resend ≤2 times after 60 s, masked mobile hints.
- ABHA address picker: ≥3 suggestions + custom entry with validation rules displayed.
- Post-KYC name/DOB/gender read-only.
- Errors verbatim where NHA specifies (e.g., "Aadhaar Number is not valid").

## 7. Success Metrics
- NHA M1 sign-off obtained.
- ABHA creation E2E < 90 s median; OTP failure UX matches spec.
- Zero PHI/secret leakage incidents.

## 8. Future placeholders (M2–M4)
- M2: HIP — discovery, care-context link, health record push (FHIR bundles).
- M3: HIU — consent request, data fetch, viewer.
- M4: full compliance hardening + production access (switch base URLs, X-CM-ID `abdm`).
- SaaS platform: multi-tenant facilities, RBAC, billing — **TBD**.
