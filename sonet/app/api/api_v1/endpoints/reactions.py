from typing import List, Any

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi import status, Depends, Body
from fastapi.routing import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from app import schemas, models, crud
from app.api import depends

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[schemas.Reaction])
def get_reactions(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(depends.get_session),
    current_user: models.User = Depends(depends.get_current_active_user),
) -> List[schemas.Reaction]:
    reactions = crud.reaction.get_multi(session, skip=skip, limit=limit)
    return reactions


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_reaction(
    *,
    post_id: int,
    emoji: schemas.Emoji = schemas.Emoji.ok,
    session: Session = Depends(depends.get_session),
    current_user=Depends(depends.get_current_active_user),
) -> schemas.Reaction:
    post = crud.post.get(session, id=post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    if post.author_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can't leave a reaction on your own post",
        )
    reaction = crud.reaction.get_reaction_by_post_author_id(
        session, post_id=post_id, author_id=current_user.id
    )
    if reaction:
        reaction_in = schemas.ReactionUpdate(emoji=emoji.value)
        reaction = crud.reaction.update(session, db_obj=reaction, obj_in=reaction_in)
    else:
        reaction_in = schemas.ReactionCreate(
            post_id=post_id, author_id=current_user.id, emoji=emoji.value
        )
        reaction = crud.reaction.create(db=session, obj_in=reaction_in)

    return reaction


@router.put(
    "/{reaction_id}", status_code=status.HTTP_200_OK, response_model=schemas.Reaction
)
def update_reaction(
    *,
    reaction_id: int,
    reaction_in: schemas.ReactionUpdate,
    session: Session = Depends(depends.get_session),
    current_user: models.User = Depends(depends.get_current_active_user),
) -> schemas.Reaction:
    reaction = crud.reaction.get(session, id=reaction_id)
    if not reaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Reaction not found"
        )
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permission"
        )
    updated_reaction = crud.reaction.update(
        session, db_obj=reaction, obj_in=reaction_in
    )
    return updated_reaction


@router.get(
    "/{reaction_id}", status_code=status.HTTP_200_OK, response_model=schemas.Reaction
)
def retrieve_reaction(
    *,
    reaction_id: int,
    session: Session = Depends(depends.get_session),
    current_user: models.User = Depends(depends.get_current_active_user),
) -> schemas.Reaction:
    reaction = crud.reaction.get(session, id=reaction_id)
    if not reaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Reaction not found"
        )
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permission"
        )
    return reaction


@router.delete("/{reaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_reaction(
    *,
    reaction_id: int,
    session: Session = Depends(depends.get_session),
    current_user: models.User = Depends(depends.get_current_active_user),
) -> None:
    reaction = crud.reaction.get(session, id=reaction_id)
    if not reaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Reaction not found"
        )
    if (
        not crud.user.is_superuser(current_user)
        and current_user.id != reaction.author_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can remove only your own reaction",
        )
    crud.reaction.remove(db=session, id=reaction_id)
