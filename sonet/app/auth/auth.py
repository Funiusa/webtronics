from __future__ import annotations

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from fastapi import HTTPException, status
from app.database import cruds

from datetime import datetime, timedelta
from typing import Optional
import secrets
import jwt

url_prefix = "/auth"

JWT_SECRET = secrets.token_hex(16)
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXP_MIN = 30


def create_access_token(data: dict, expire_delta: Optional[timedelta] = None):
    payload = {"user": data}
    if expire_delta:
        expire = datetime.utcnow() + expire_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXP_MIN)

    payload.update({"exp": expire})
    encoded_jwt = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def get_decode_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM, verify=False)
        expiration_time = payload.get("exp")
        current_time = datetime.utcnow()
        if current_time < datetime.fromtimestamp(expiration_time):
            return payload.get("user")
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.exceptions.InvalidTokenError as er:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{er}",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_user_access(token, db: Session):
    user_payload = get_decode_token(token=token)
    print(f"\n\n\n{user_payload}\n\n")
    if user_payload:
        user_id = user_payload.get("id")
        user = cruds.users.retrieve_user(user_id=user_id, db=db)
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )


class PasswordHash:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def set_hashed_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, password, hashed_password):
        return self.pwd_context.verify(password, hashed_password)
