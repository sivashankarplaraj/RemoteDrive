# Architecture overview

```mermaid
flowchart TB
  subgraph Clients
    WUI[Web UI]
    CLI[CLI]
  end

  subgraph Backend[Backend - Django API]
    API[REST API]
    Auth[Auth / API Key or JWT]
  end

  subgraph Storage[Object Storage]
    MINIO[(MinIO S3)]
  end

  subgraph DB[Metadata DB]
    SQLite[(SQLite / Postgres later)]
  end

  WUI -->|HTTP/JSON| API
  CLI -->|HTTP/JSON| API

  API -->|Presigned URL (PUT/GET)| MINIO
  API -->|Read/Write metadata| SQLite

  classDef svc fill:#eef,stroke:#446,stroke-width:1px;
  class API,Auth,MINIO,SQLite svc;
```

Key points
- Data path uses presigned URLs so file bytes go directly between client and MinIO.
- Django API handles authentication, authorization, metadata, and generating presigned URLs.
- DB stores file records, versions, and ownership; storage holds the actual bytes.
