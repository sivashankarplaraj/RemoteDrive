# Upload flow (sequence)

```mermaid
sequenceDiagram
    autonumber
    participant U as User - Web and CLI
    participant A as Django API
    participant S3 as MinIO S3
    participant DB as Metadata DB

    U->>A: POST /files/init-upload (filename, size, content-type)
    A->>S3: Generate presigned PUT URL for object key
    A-->>U: 200 {key, presigned_put_url}

    U->>S3: PUT object bytes using presigned URL
    Note over U,S3: Client streams file directly to object storage

    U->>A: POST /files/commit {key, checksum, size}
    A->>DB: Insert file record (pending->committed)
    A-->>U: 201 {fileId, version=1}
```

Edge cases
- If upload fails before commit, the object is orphaned; later GC/lifecycle can clean up.
- Server verifies checksum/size on commit when possible and rejects mismatches.
