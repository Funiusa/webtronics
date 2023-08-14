from typing import List, Any
from fastapi import Depends, status, Body
from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import schemas, models, crud
from app.api import depends
from app.core.config import settings

router = APIRouter()


@router.get("/", response_model=List[schemas.User])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(depends.get_session),
) -> list[schemas.User]:
    users = crud.user.get_multi(db=session, skip=skip, limit=limit)
    return users


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
async def create_user(
    *,
    db: Session = Depends(depends.get_session),
    user_in: schemas.UserCreate,
    current_user: models.User = Depends(depends.get_current_active_superuser),
) -> Any:
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )
    user = crud.user.create(db, obj_in=user_in)
    return user


@router.put("/me", status_code=status.HTTP_200_OK, response_model=schemas.User)
async def update_user_me(
    *,
    password: str = Body(None),
    full_name: str = Body(None),
    email: str = Body(None),
    session: Session = Depends(depends.get_session),
    current_user: models.User = Depends(depends.get_current_active_user),
) -> schemas.User:
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdate(**current_user_data)
    if password:
        user_in.password = password
    if email:
        user_in.email = email
    if full_name:
        user_in.full_name = full_name
    updated_user = crud.user.update(db=session, db_obj=current_user, obj_in=user_in)
    return updated_user


@router.get("/me", status_code=status.HTTP_200_OK, response_model=schemas.User)
async def retrieve_current_user(
    session: Session = Depends(depends.get_session),
    current_user: models.User = Depends(depends.get_current_active_user),
) -> schemas.User:
    return current_user


@router.post("/open", response_model=schemas.User)
def create_user_open(
    *,
    session: Session = Depends(depends.get_session),
    email: str = Body(...),
    username: str = Body(...),
    password: str = Body(...),
    full_name: str = Body(None),
) -> Any:
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Open user registration is forbidden on this server",
        )
    user = crud.user.get_by_email(db=session, email=email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )
    user_in = schemas.UserCreate(
        username=username, email=email, password=password, full_name=full_name
    )
    user = crud.user.create(db=session, obj_in=user_in)
    return user


@router.get("/{user_id}", response_model=schemas.User)
def get_user_by_id(
    user_id: int,
    current_user: models.User = Depends(depends.get_current_active_user),
    session: Session = Depends(depends.get_session),
) -> schemas.User:
    user = crud.user.get(db=session, id=user_id)
    if current_user == user:
        return user
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges",
        )
    return user


@router.put("/{user_id}", response_model=schemas.User)
def update_user_by_id(
    user_id: int,
    user_in: schemas.UserUpdate,
    current_user: models.User = Depends(depends.get_current_active_user),
    session: Session = Depends(depends.get_session),
) -> schemas.User:
    user = crud.user.get(db=session, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User doesn't exists"
        )
    updated_user = crud.user.update(session, db_obj=current_user, obj_in=user_in)
    return updated_user
