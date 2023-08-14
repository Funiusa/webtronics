from typing import List
from sqlalchemy.orm import Session
from fastapi import status, Depends, Query
from fastapi.routing import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from app import schemas, models, crud
from app.api.api_v1.endpoints.reactions import get_reactions
from app.api import depends

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.Post])
def get_posts(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(depends.get_session),
    current_user: models.User = Depends(depends.get_current_active_user),
) -> List[schemas.Post]:
    if crud.user.is_superuser(current_user):
        posts = crud.post.get_multi(db=session, skip=skip, limit=limit)
    else:
        posts = crud.post.get_multi_by_author(
            db=session, author_id=current_user.id, skip=skip, limit=limit
        )
    return posts


@router.get("/reactions")
def get_user_reaction_posts(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(depends.get_session),
    current_user: models.User = Depends(depends.get_current_active_user),
) -> List[schemas.Post]:
    posts = crud.post.get_multi_by_author_reaction(
        session, author_id=current_user.id, skip=skip, limit=limit
    )
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(
    *,
    post_in: schemas.PostCreate,
    session: Session = Depends(depends.get_session),
    current_user: models.User = Depends(depends.get_current_active_user),
) -> schemas.Post:
    post = crud.post.create_with_author(
        db=session, obj_in=post_in, author_id=current_user.id
    )
    return post


@router.put("/{post_id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
def update_post(
    *,
    post_id: int,
    post_in: schemas.PostUpdate,
    session: Session = Depends(depends.get_session),
    current_user: models.User = Depends(depends.get_current_active_user),
) -> schemas.Post:
    post = crud.post.get(db=session, id=post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    if not crud.user.is_superuser(current_user) and post.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permission"
        )
    updated_post = crud.post.update(session, db_obj=post, obj_in=post_in)
    return updated_post


@router.get("/{post_id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
def retrieve_post(
    *,
    post_id: int,
    session: Session = Depends(depends.get_session),
    current_user: models.User = Depends(depends.get_current_active_user),
) -> schemas.Post:
    post = crud.post.get(session, id=post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    if not crud.user.is_superuser(current_user) and post.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permission"
        )
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_post(
    *,
    post_id: int,
    session: Session = Depends(depends.get_session),
    current_user: models.User = Depends(depends.get_current_active_user),
) -> None:
    post = crud.post.get(session, id=post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    if not crud.user.is_superuser(current_user) and post.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permission"
        )
    crud.post.remove(db=session, id=post_id)
