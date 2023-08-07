import shutil
from fastapi import Depends, responses, File, UploadFile, status
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from app.database.base import get_session
from app.database import cruds, schemas, models
from app.routes.auth import get_current_user
from app.routes.user import upload_image

router = APIRouter(tags=["Posts"], prefix="/api/posts")


@router.get("/")
async def get_all_posts(
        session: Session = Depends(get_session)
) -> list[schemas.PostRead]:
    posts = cruds.posts.get_all_posts(db=session)
    return posts


@router.get("/{user_id}/posts")
async def get_all_user_posts(
        user_id: int, session: Session = Depends(get_session)
) -> list[schemas.PostRead]:
    user_posts = cruds.posts.get_all_user_posts(user_id=user_id, db=session)
    return user_posts


@router.post("/{user_id}/posts", description="Create new user's post")
async def create_post(
        title: str,
        description: str,
        content: str,
        image: str = Depends(upload_image),
        session: Session = Depends(get_session),
        current_user: models.DbUser = Depends(get_current_user),
) -> schemas.PostRead:
    data = {
        "title": title,
        "description": description,
        "content": content,
        "image_url": image,
    }
    post = cruds.posts.create_post(user=current_user, data=data, db=session)
    return post


@router.get(
    "/{user_id}/posts/{post_id}",
    responses={
        404: {
            "content": {
                "application/json": {"example": {"detail": "User's post 0 not found"}}
            }
        }
    },
    description="Retrieve user's post",
)
async def retrieve_post(
        user_id: int, post_id: int, session: Session = Depends(get_session)
) -> schemas.PostRead:
    post = cruds.posts.retrieve_post(user_id=user_id, post_id=post_id, db=session)
    return schemas.PostRead.from_orm(post)


@router.delete("/{user_id}/post/{post_id}", status_code=status.HTTP_404_NOT_FOUND)
async def remove_post(
        user_id: int, post_id: int, session: Session = Depends(get_session)
) -> None:
    cruds.posts.remove_post(user_id=user_id, post_id=post_id, db=session)
