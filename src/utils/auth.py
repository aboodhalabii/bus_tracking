import os
from typing import Any, Dict

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError
import hashlib
import hmac
import secrets
from datetime import datetime, timedelta
import uuid


def _get_jwt_secret() -> str:
    # Prefer a dedicated JWT secret but fall back to SUPABASE_KEY
    return os.getenv("JWT_SECRET") or os.getenv("SUPABASE_KEY") or "dev-secret"

security = HTTPBearer(auto_error=False)


def decode_token(token: str) -> Dict[str, Any]:
    secret = _get_jwt_secret()
    try:
        payload = jwt.decode(token, secret, algorithms=["HS256"])  # type: ignore[arg-type]
        return payload
    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token: {str(e)}")


def create_access_token(data: Dict[str, Any], expires_delta: int | None = None) -> str:
    secret = _get_jwt_secret()
    to_encode = data.copy()
    now = datetime.utcnow()
    to_encode.update({"iat": now, "jti": str(uuid.uuid4())})
    if expires_delta is None:
        expires_delta = int(os.getenv("JWT_EXP_SECONDS", 60 * 60 * 24 * 7))
    expire = now + timedelta(seconds=expires_delta)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, secret, algorithm="HS256")
    return token


def hash_password(password: str) -> str:
    """Hash a password using PBKDF2-HMAC-SHA256 with a random salt.

    Returns a string in the format salt$hash_hex
    """
    salt = secrets.token_hex(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 200_000)
    return f"{salt}${dk.hex()}"


def verify_password(plain_password: str, stored: str) -> bool:
    try:
        salt, hash_hex = stored.split("$", 1)
    except Exception:
        return False
    dk = hashlib.pbkdf2_hmac("sha256", plain_password.encode("utf-8"), salt.encode("utf-8"), 200_000)
    return hmac.compare_digest(dk.hex(), hash_hex)


def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)) -> Dict[str, Any]:
    if not credentials or not credentials.credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing authorization token")
    token = credentials.credentials
    return decode_token(token)


def require_role(role: str):
    def _dependency(user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
        # Supabase stores roles in a few possible places depending on setup.
        # Check common claims for role information.
        user_role = None
        if isinstance(user.get("role"), str):
            user_role = user.get("role")
        elif isinstance(user.get("app_metadata"), dict):
            user_role = user.get("app_metadata", {}).get("role")
        elif isinstance(user.get("user_metadata"), dict):
            user_role = user.get("user_metadata", {}).get("role")

        if not user_role:
            # Some projects store a custom claim like `x-hasura-role` or `role`
            user_role = user.get("x-hasura-role") or user.get("role")

        if not user_role or user_role.lower() != role.lower():
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient role")
        return user

    return _dependency


require_admin = require_role("admin")
require_driver = require_role("driver")
require_student = require_role("student")
