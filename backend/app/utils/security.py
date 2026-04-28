import base64
import hashlib
import hmac
import secrets


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
    return f"{base64.b64encode(salt).decode()}${base64.b64encode(digest).decode()}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        salt_b64, digest_b64 = hashed_password.split("$", maxsplit=1)
    except ValueError:
        return False
    salt = base64.b64decode(salt_b64.encode())
    expected_digest = base64.b64decode(digest_b64.encode())
    computed_digest = hashlib.pbkdf2_hmac("sha256", plain_password.encode("utf-8"), salt, 100000)
    return hmac.compare_digest(expected_digest, computed_digest)

