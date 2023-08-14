from __future__ import annotations
from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from pydantic import ValidationError

from app.core.config import settings
from app.core import security
from app.database.session import SessionLocal
from app import schemas, crud, models
import jwt

oauth2schema = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access_token"
)


def get_session() -> Generator:
    with SessionLocal() as session:
        yield session


def get_current_user(
    db: Session = Depends(get_session), token: str = Depends(oauth2schema)
) -> models.User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.JWT_ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token error")
    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not valid credentials"
        )
    user = crud.user.get(db=db, id=token_data.sub)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not crud.user.is_active(current_user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return current_user


def get_current_active_superuser(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User does not have enough privileges",
        )
    return current_user
