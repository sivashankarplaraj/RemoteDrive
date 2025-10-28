from datetime import datetime
import secrets
import ulid


def object_key_for(filename: str | None = None) -> str:
    """Generate immutable unique object key per convention: uploads/YYYY/MM/DD/ULID[-8]-suffix[.ext]
    """
    now = datetime.utcnow()
    date_path = now.strftime("%Y/%m/%d")
    u = ulid.new()
    short = str(u)[-8:]
    suffix = secrets.token_hex(4)
    ext = ''
    if filename and '.' in filename:
        ext = '.' + filename.split('.')[-1].lower()
    return f"uploads/{date_path}/{u}-{short}-{suffix}{ext}"
