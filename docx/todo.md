# Implementation TODO (micro-tasks)

Derived from the current docs (architecture-overview.md, sequence-upload.md, data-model.md, deployment.md). Ordered to get a working PoC locally.

## 0) Repo and environment bootstrap
- [ ] Create Python virtualenv and pin dependencies (Django, djangorestframework, PyJWT, minio, ulid-py).
- [ ] Add settings module with env var config (MINIO_* creds/endpoint/bucket, JWT secret, DEBUG, DB URL).
- [ ] Create a minimal Django project `remotedrive` and app `files`.
- [ ] Configure SQLite DB for dev; prepare settings switch for Postgres later.

## 1) Data model and migrations
- [ ] Implement models from data-model.md: USERS, FILES, FILE_VERSIONS, SHARES (simplify USERS for PoC if desired).
- [ ] Add indices: (FILES.user_id, created_at), (FILE_VERSIONS.file_id, version), SHARES.token unique.
- [ ] Create and run initial migrations.
- [ ] Register models in Django admin for quick inspection.

## 2) Auth (JWT) and permissions
- [ ] Add middleware/auth class to validate JWT from Authorization: Bearer <token>.
- [ ] Provide a local helper command to mint a dev JWT for testing.
- [ ] Per-object ownership checks: filter by current user on FILES and enforce on endpoints.

## 3) Object storage integration (MinIO)
- [ ] Add MinIO client wiring (SDK) and bucket bootstrap utility (create if missing).
- [ ] Implement presign helpers: PUT (init-upload), GET (download), with configurable expiry.
- [ ] Implement object key generator using convention: uploads/YYYY/MM/DD/ULID[-8]-suffix[.ext].

## 4) REST API (Django REST Framework)
- [ ] Endpoint: POST /files/init-upload {filename, size, content_type} -> {key, presigned_put_url}.
- [ ] Client flow note: Client PUTs bytes directly to presigned URL; API never proxies file bytes.
- [ ] Endpoint: POST /files/commit {key, checksum, size} -> {fileId, version}.
- [ ] Optional: GET /files/{id}/download (current) and /files/{id}/versions/{v}/download -> presigned GET URL.
- [ ] Serialize FILES and FILE_VERSIONS for listing and detail views (owner-scoped).

## 5) Validation and edge cases
- [ ] On commit: verify size/checksum if feasible, ensure key exists, create FILE_VERSIONS, update FILES.key_current.
- [ ] Handle duplicate commits gracefully (idempotency on same key/version where possible).
- [ ] Orphan cleanup plan (document lifecycle/GC; job later).

## 6) Local dev and smoke tests
- [ ] Add a Docker-based MinIO start script/docs for Windows PowerShell.
- [ ] Add manage.py runserver instructions; set JWT secret via env.
- [ ] Smoke test script or docs: init-upload -> PUT -> commit via curl or httpie.

## 7) Shares (read|write) [stretch]
- [ ] Create/validate share tokens with optional expiry and permissions.
- [ ] Download via share token -> presigned GET.

## 8) Postgres & ASGI readiness [later]
- [ ] Docker Compose: MinIO + Postgres; Django via ASGI (uvicorn/gunicorn).
- [ ] Migrate settings to use DATABASE_URL and production config.

## 9) Docs and diagrams sync
- [ ] Update docx/sequence-upload.md and architecture-overview.md if endpoint shapes evolve.
- [ ] Ensure this todo.md stays aligned with implementation status.
