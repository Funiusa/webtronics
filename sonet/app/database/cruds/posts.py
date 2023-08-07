from datetime import datetime

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from typing import List
from app.database import schemas, models
from app.database.cruds.users import retrieve_user


def get_all_posts(db: Session) -> List[schemas.PostRead]:
    stmt = select(models.DbPost).order_by(models.DbPost.id)
    posts = db.execute(statement=stmt).scalars().all()
    return list(map(schemas.PostRead.from_orm, posts))


def create_post(
        user: models.DbUser, data: dict, db: Session
) -> schemas.PostRead:
    retrieve_user(user_id=user.id, db=db)
    user_posts = get_all_user_posts(user_id=user.id, db=db)
    try:
        post = models.DbPost(**data)
        post.author_id = user.id
        post.post_id = len(user_posts) + 1
        post.timestamp = datetime.now()
        db.add(post)
        db.commit()
        db.refresh(post)
        return schemas.PostRead.from_orm(post)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Integrity error"
        )


def get_all_user_posts(user_id: int, db: Session) -> list[schemas.PostRead]:
    retrieve_user(user_id=user_id, db=db)
    stmt = (
        select(models.DbPost)
        .filter_by(author_id=user_id)
        .order_by(models.DbPost.post_id)
    )
    posts = db.execute(statement=stmt).scalars()
    return list(map(schemas.PostRead.from_orm, posts))


def retrieve_post(user_id: int, post_id: int, db: Session) -> models.DbPost:
    retrieve_user(user_id=user_id, db=db)
    post = db.get(models.DbPost, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User's post {post_id} not found",
        )
    return post


def remove_post(user_id: int, post_id: int, db: Session) -> None:
    post = retrieve_post(user_id=user_id, post_id=post_id, db=db)
    db.delete(post)
    db.commit()
