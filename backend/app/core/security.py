from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from app.config import settings

# Prefer pbkdf2_sha256 to avoid hard runtime dependency on bcrypt backends.
# bcrypt is kept for backward compatibility when verifying existing hashes.
pwd_context = CryptContext(
    schemes=["pbkdf2_sha256", "bcrypt"],
    deprecated="auto",
)

ALGORITHM = "HS256"


# -----------------------------
# Password Hashing
# -----------------------------
def hash_password(password: str) -> str:
    try:
        return pwd_context.hash(password, scheme="pbkdf2_sha256")
    except Exception as exc:
        raise RuntimeError("Password hashing backend unavailable") from exc


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False


# -----------------------------
# JWT Token
# -----------------------------
def create_access_token(data: dict, expires_delta: timedelta = None):

    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt
