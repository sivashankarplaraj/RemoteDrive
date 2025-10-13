# Deployment / topology (local dev)

```mermaid
flowchart LR
  Dev[Developer Workstation]

  subgraph Docker
    MINIO[(MinIO container)]
  end

  subgraph Local
    DJ[Django runserver]
    DB[(SQLite database)]
  end

  Dev -->|Browser or CLI| DJ
  DJ -->|Presigned URL| MINIO
  DJ -->|ORM| DB
```

Environments
- Local dev: Dockerized MinIO, Django runserver, SQLite DB.
- Later: Docker Compose for MinIO + Postgres; Django served via ASGI (uvicorn/gunicorn).
- Cloud: Replace MinIO with S3 or managed object store, Postgres as managed DB.
