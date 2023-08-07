from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException
from fastapi import status

from app.database import schemas, base, models
from app.auth import auth

from typing import List


def create_superuser(db: Session = base.LocalSession) -> None:
    superuser_data = {
        "username": "admin",
        "email": "admin@gmail.com",
        "password": "pass",
        "is_superuser": True,
        "is_staff": True,
        "is_active": True,
    }
    superuser = models.DbUser(**superuser_data)
    phash = auth.PasswordHash()
    superuser.password = phash.set_hashed_password(superuser.password)
    db.add(superuser)
    db.commit()
    db.refresh(superuser)


def create_user(user_data: schemas.UserCreate, db: Session) -> schemas.UserRead:
    try:
        new_user = models.DbUser(**user_data.dict())
        phash = auth.PasswordHash()
        new_user.password = phash.set_hashed_password(user_data.password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        raise HTTPException(status_code=403, detail=f"Username or email already exists")
    return schemas.UserRead.from_orm(new_user)


def get_users(db: Session) -> List[schemas.UserRead]:
    stmt = select(models.DbUser)
    users = db.execute(statement=stmt).scalars()
    return list(map(schemas.UserRead.from_orm, users))


def retrieve_user(user_id: int, db: Session) -> models.DbUser:
    user = db.get(models.DbUser, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} not found."
        )
    return user


def retrieve_user_by_username(username: str, db: Session) -> models.DbUser:
    stmt = select(models.DbUser).filter_by(username=username)
    user = db.execute(statement=stmt).scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User {username} not found."
        )
    return user


def update_user(
        user_id: int, data: schemas.UserUpdate, db: Session
) -> schemas.UserRead:
    user = retrieve_user(user_id=user_id, db=db)
    try:
        user.username = data.username
        user.email = data.email
        db.add(user)
        db.commit()
        db.refresh(user)
        return schemas.UserRead.from_orm(user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Integrity error"
        )


def remove_user(user_id: int, db: Session) -> None:
    user = retrieve_user(user_id=user_id, db=db)
    db.delete(user)
    db.commit()
