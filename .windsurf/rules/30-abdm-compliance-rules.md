# ABDM / NHA Compliance Rules (M1)

- Consent: before Aadhaar OTP request, the ABDM-published consent text (versioned) must be accepted; persist a `ConsentLog` row. UI must support multilingual consent (i18n keys, English default).
- OTP UX per NHA test sheet: 6-digit OTP, resend max 2 times after 60s cooldown, masked mobile hint ("OTP sent to ******XXXX").
- Aadhaar validation: 12 digits with friendly error "Aadhaar Number is not valid".
- ABHA address rules: 8–18 chars, alphanumeric, at most one dot and one underscore, not at start/end; offer ≥3 suggestions from the suggestion API.
- Profile fields name/DOB/gender are read-only post-KYC; address/email/mobile editable.
- Display 14-digit ABHA number + ABHA address after creation; provide ABHA card view/download.
- Data residency: all PHI stays in India (ap-south-1). Follow the Health Data Management Policy: minimal collection, purpose limitation, audit every access (AuditLog).
- Scan & Share: on `patient/share` callback, ACK on-share within SLA with token number, 30-min validity.
- Do not implement biometric (RD service) capture in web without checking; it requires registered devices — keep as stub for M1 unless asked.
