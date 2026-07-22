# Healthekit M1 — Endpoint Matrix (living)
> Update this file in the same PR as any endpoint change.

## A. ABDM upstream APIs used (Sandbox)
**Gateway** `https://dev.abdm.gov.in/api/hiecm`
| Purpose | Method & Path |
|---|---|
| Session token | POST /gateway/v3/sessions |
| Certs (JWKS) | GET /gateway/v3/certs |
| Update bridge URL | PATCH /gateway/v3/bridge/url |
| Bridge services | GET /gateway/v3/bridge-services |
| Scan&Share ACK | POST /patient-share/v3/on-share |
| Running token status | POST /patient-share/v3/running-token/status · /on-status |

**Bridge/HRP** `https://facilitysbx.abdm.gov.in` — POST /v1/bridges/MutipleHRPAddUpdateServices

**ABHA** `https://abhasbx.abdm.gov.in/abha/api/v3`
| Flow | Endpoints |
|---|---|
| Public cert | GET /profile/public/certificate |
| Enrol (Aadhaar OTP) | POST /enrollment/request/otp · POST /enrollment/enrol/byAadhaar · POST /enrollment/auth/byAbdm |
| ABHA address | GET /enrollment/enrol/suggestion · POST /enrollment/enrol/abha-address |
| Enrol by document (DL/PAN) | POST /enrollment/enrol/byDocument |
| Face/bio enrol | POST /enrollment/enrol/auth/init · /enrollment/enrol/capturePID · /enrollment/enrol/byAadhaar |
| Login (number/Aadhaar/mobile) | POST /profile/login/request/otp · /profile/login/verify · /profile/login/verify/user · /profile/login/search |
| ABHA search | POST /profile/account/abha/search |
| Profile | GET /profile/account · /profile/account/abha-card · /profile/account/qrCode · PATCH /profile/account |
| Profile OTP updates | POST /profile/account/request/otp · /profile/account/verify · /profile/account/request/emailVerificationLink |
| ABHA address login (PHR web) | POST /phr/web/login/abha/search · /request/otp · /verify · GET /phr/web/login/profile/abha-profile · /profile/abha/phr-card |

## B. Healthekit internal API (`/api/v1`)
| # | Method | Path | Maps to NHA | Status |
|---|---|---|---|---|
| 1 | GET | /healthz, /readyz | — | ✅ bootstrap |
| 2 | POST | /abha/enrollment/aadhaar/request-otp | CRT_ABHA_101–105 | ✅ |
| 3 | POST | /abha/enrollment/aadhaar/enrol | CRT_ABHA_107, 113 | ✅ |
| 4 | POST | /abha/enrollment/mobile/request-otp | CRT_ABHA_108/109 | ✅ |
| 5 | POST | /abha/enrollment/mobile/verify-otp | CRT_ABHA_109 | ✅ |
| 6 | GET | /abha/enrollment/address/suggestions | CRT_ABHA_112 | ✅ |
| 7 | POST | /abha/enrollment/address | CRT_ABHA_112 | ✅ |
| 8 | POST | /abha/login/request-otp | VRFY 101/201/301/401 | ✅ |
| 9 | POST | /abha/login/verify | VRFY 1xx–4xx | ✅ |
| 10 | POST | /abha/login/verify-user | VRFY_303 | ✅ |
| 11 | POST | /abha/address/search·request-otp·verify | VRFY 102/202 | ✅ |
| 12 | GET | /abha/address/profile · /card | VRFY 102/202 | ✅ |
| 13 | GET | /abha/profile · /card · /qr | CRT_ABHA_114 | ✅ |
| 14 | POST | /patients · GET /patients/by-abha/{n} | TAGGING | ✅ |
| 15 | POST | /api/v3/hip/patient/share (callback) | SHARE_701 | ✅ |
| 16 | — | /abha/enrollment/document | CRT_ABHA_4xx | 🔲 placeholder |
| 17 | — | /abha/enrollment/biometric | CRT_ABHA_2xx | 🔲 placeholder |
| 18 | — | /abha/profile updates (mobile/email/photo/re-KYC/delete) | PROF_601–605 | 🔲 placeholder |
