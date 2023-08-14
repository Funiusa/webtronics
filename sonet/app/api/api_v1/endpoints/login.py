from datetime import timedelta
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException
from fastapi import Depends, status
from sqlalchemy.orm import Session
from app import schemas, crud
from app.api.depends import get_session
from app.core.config import settings
from app.core import security

router = APIRouter()


@router.post("/login/access_token", response_model=schemas.Token)
def login_access_token(
    db: Session = Depends(get_session), form_data: OAuth2PasswordRequestForm = Depends()
):
    user = crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid username or password",
        )
    elif not crud.user.is_active(user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            subject=user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }
