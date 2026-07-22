# Testing & Living Docs Rules

- Every NHA test-case ID implemented (CRT_ABHA_1xx, VRFY_ABHA_xxx, SHARE_701, TAGGING) gets: backend test + frontend flow + row updated in docs/ENDPOINTS.md traceability table.
- When adding/changing an endpoint: update docs/ENDPOINTS.md and docs/SRS.md in the same PR ("docs-with-code").
- PRD.md/SRS.md are living: mark changes with a dated entry in their Revision History table.
- Postman: keep `docs/postman/` exports in sync with reality before each milestone submission.
