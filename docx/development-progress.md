# Development Progress

Track milestones and current status as the PoC evolves from docs to running code.

## Milestones
- [ ] Project scaffolded (Django project/app, settings, dependencies)
- [ ] Data model implemented and migrated
- [ ] Auth (JWT) wired
- [ ] MinIO presign integration
- [ ] Init-upload and commit endpoints
- [ ] Download (presigned GET) endpoints
- [ ] Smoke test passing (init-upload -> PUT -> commit)
- [ ] Shares (read|write)
- [ ] Docker Compose with Postgres and ASGI

## Status log
- 2025-10-14: Initialized project planning docs (todo.md) and progress tracker. Adopted defaults: JWT, MinIO SDK, immutable object keys convention.

## Notes
- Keep docx diagrams and JSON shapes updated if APIs change.
- Record environment variables and commands used for local dev (PowerShell on Windows).
