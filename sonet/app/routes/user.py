import random
import shutil
import string
from typing import List, Annotated

from fastapi.routing import APIRouter
from fastapi import (
    Depends,
    status,
    exceptions,
    UploadFile,
    Form
)
from sqlalchemy.orm import Session

from app.database.base import get_session
from app.database import schemas, cruds, models
from app.routes.auth import get_current_user

router = APIRouter(
    tags=["Users"],
    prefix="/api/users",
)


@router.post("/images")
async def upload_image(
        image: UploadFile,
):
    letters = string.ascii_letters
    random_name = "".join(random.choice(letters) for _ in range(5))
    new = f"_{random_name}."
    filename = new.join(image.filename.rsplit(".", 1))
    path = f"images/{filename}"
    with open(path, "w+b") as buffer:
        shutil.copyfileobj(image.file, buffer)
    return path


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
        username: str = Form(...),
        email: str = Form(...),
        password: str = Form(...),
        session: Session = Depends(get_session),
) -> schemas.UserRead:
    user_data = schemas.UserCreate(
        username=username.lower(), email=email, password=password
    )
    new_user = cruds.users.create_user(user_data=user_data, db=session)
    return new_user


@router.get("/")
async def get_all_users(
        session: Session = Depends(get_session),
) -> list[schemas.UserRead]:
    users = cruds.users.get_users(db=session)
    return users


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def retrieve_user(
        user_id: int, session: Session = Depends(get_session)
) -> schemas.UserRead:
    user = cruds.users.retrieve_user(user_id=user_id, db=session)
    return schemas.UserRead.from_orm(user)


@router.put("/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(
        user_id: int, user_data: schemas.UserUpdate,
        session: Session = Depends(get_session)
) -> schemas.UserRead:
    user = cruds.users.update_user(user_id, data=user_data, db=session)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_404_NOT_FOUND)
async def remove_user(
        user_id: int,
        session: Session = Depends(get_session),
        current_user: models.DbUser = Depends(get_current_user),
) -> None:
    if not current_user.is_superuser:
        raise exceptions.HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only superuser can remove a user",
        )
    cruds.users.remove_user(user_id=user_id, db=session)
