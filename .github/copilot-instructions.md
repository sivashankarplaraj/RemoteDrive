# Copilot usage guide for this repo

This repository documents a Django-based cloud storage PoC that uses presigned S3 URLs so clients upload/download bytes directly to object storage (MinIO). The API handles auth, metadata, and URL generation; the DB stores file/ownership/version records. Use these conventions when adding code or docs so everything stays consistent.

## Architecture in 5 bullets
- Clients (Web UI, CLI) call a Django REST API over HTTP/JSON; API authenticates via JWT for local/dev.
- API generates presigned S3 URLs (PUT for upload, GET for download); file bytes NEVER transit the API server.
- Metadata DB (SQLite locally; Postgres later) stores files, versions, shares; storage holds the bytes.
- Latest version key lives on FILES.key_current; FILE_VERSIONS keeps history.
- Diagrams live in docx/: see architecture-overview.md, sequence-upload.md, data-model.md, deployment.md.

## Key workflows you should follow
- Upload flow (sequence-upload.md):
  1) POST /files/init-upload {filename, size, content_type} -> {key, presigned_put_url}
  2) Client PUTs bytes to presigned_put_url directly
  3) POST /files/commit {key, checksum, size} -> {fileId, version=1}
  - On commit: create/advance FILE and FILE_VERSIONS, set FILES.key_current, verify size/checksum when possible.
  - If bytes upload fails before commit, the object may be orphaned (cleaned later via GC/lifecycle).
- Download flow (from architecture-overview.md):
  - API issues presigned GET URLs for the current or a requested version; clients fetch directly from storage.

## Data model anchors (data-model.md)
- USERS: id, email, display_name, created_at
- FILES: id, user_id, filename, key_current, content_type, size, checksum, created_at, deleted_at
- FILE_VERSIONS: id, file_id, version, key, size, checksum, created_at
- SHARES: id, file_id, owner_user_id, token, expires_at, permissions, created_at

## Implementation conventions
- Do not proxy file bytes through the API; always use presigned S3 URLs.
- Enforce auth first on all API endpoints (JWT in local/dev); then apply per-user ownership checks.
- Treat uploads as pending until commit; only on commit should records become active and key_current update.
- Use immutable, globally unique object keys per version; keep the latest on FILES.key_current. Do not rewrite objects in place.
- Use MinIO SDK for S3 presigning from Django.
- Shares use opaque token + optional expiry + permissions (read|write). Validate token on access and resolve to FILE.

## Integration points
- Object storage: S3-compatible API (MinIO locally). API responsibility is to mint presigned URLs (PUT/GET) and map them to FILE(S)/VERSION(S).
- Database: local dev uses SQLite; production-like uses Postgres. Keep ORM-level writes within commit endpoints.
- Local topology (deployment.md): Django runserver + SQLite locally; MinIO runs in Docker; later: Compose with Postgres and ASGI.

## Object key naming convention
- Goal: keys must be immutable and unique at creation time (init-upload happens before fileId/version exist).
- Recommended pattern for keys minted at init-upload:
  - uploads/YYYY/MM/DD/ULID[-8]-randomsuffix[.ext]
  - Example: uploads/2025/10/14/01JBG2X2B7M8A4S3KPFQ7QZ5T9-ab12cd34
- Notes:
  - Do not include user IDs, file IDs, or version numbers in the key (they may be unknown at init-upload).
  - Store the original filename and content_type in metadata/DB; avoid putting PII in keys.
  - On commit, record the minted key in FILE_VERSIONS and update FILES.key_current; do not move/rename the object.

## JSON shapes (examples)
- Init upload request: {"filename":"notes.pdf","size":12345,"content_type":"application/pdf"}
- Init upload response: {"key":"...","presigned_put_url":"https://minio/..."}
- Commit request: {"key":"...","checksum":"sha256:...","size":12345}
- Commit response: {"fileId":"uuid","version":2}

## Where to look / update alongside code
- Flows: docx/sequence-upload.md
- Architecture: docx/architecture-overview.md
- Schema: docx/data-model.md
- Topology: docx/deployment.md

## Defaults adopted for this repo (dev)
- Auth: JWT (local/dev).
- Presigning: MinIO SDK.
- Object keys: immutable, unique keys as per the convention above; versions link keys via DB.

## Dev workflow status
- Implementation is currently documentation-stage only. Once code exists, add commands for:
  - Starting MinIO (Docker) and seeding credentials.
  - Running Django (manage.py runserver) and setting JWT secrets.
  - A tiny smoke test: init-upload -> PUT -> commit.