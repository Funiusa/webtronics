from __future__ import annotations

from fastapi import Depends, exceptions, status, routing
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.auth.auth import PasswordHash, create_access_token, get_user_access
from app.database.base import get_session
from sqlalchemy import select
from app.database import schemas, models

url_prefix = "/login"

router = routing.APIRouter(prefix=url_prefix, tags=["Authentication"])

oauth2schema = OAuth2PasswordBearer(tokenUrl=url_prefix)


def get_current_user(
    token: str = Depends(oauth2schema), session: Session = Depends(get_session)
) -> schemas.UserRead:
    user = get_user_access(token=token, db=session)
    return user


@router.post("/")
async def get_generated_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    stmt = select(models.DbUser).filter_by(username=form_data.username)
    user = session.execute(statement=stmt).scalars().first()
    phash = PasswordHash()
    if not user:
        raise exceptions.HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Authentication error"
        )
    if not phash.verify_password(
        password=form_data.password, hashed_password=user.password
    ):
        raise exceptions.HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password"
        )
    user_token_data = schemas.UserRead.from_orm(user)
    token = create_access_token(data=user_token_data.dict())
    return {
        "user_id": user.id,
        "username": user.username,
        "token": "bearer",
        "access_token": token,
    }
