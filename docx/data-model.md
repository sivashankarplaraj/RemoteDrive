# Data model (ER)

```mermaid
erDiagram
    USERS ||--o{ FILES : owns
    FILES ||--o{ FILE_VERSIONS : has
    USERS ||--o{ SHARES : creates
    FILES ||--o{ SHARES : target

    USERS {
        uuid id PK
        string email
        string display_name
        datetime created_at
    }

    FILES {
        uuid id PK
        uuid user_id FK
        string filename
        string key_current
        string content_type
        long size
        string checksum
        datetime created_at
        datetime deleted_at
    }

    FILE_VERSIONS {
        uuid id PK
        uuid file_id FK
        int version
        string key
        long size
        string checksum
        datetime created_at
    }

    SHARES {
        uuid id PK
        uuid file_id FK
        uuid owner_user_id FK
        string token
        datetime expires_at
        string permissions // read|write
        datetime created_at
    }
```

Notes
- For PoC, `USERS` can be simplified or replaced with a single tenant or API key table.
- `key_current` tracks latest version object key for quick reads; versions keep history.
