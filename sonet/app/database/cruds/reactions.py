from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status

from app.database import schemas, models
from app.database.cruds.posts import retrieve_post


def get_post_reaction(
    user_id: int, post: models.DbPost, db: Session
) -> models.DbReaction:
    stmt = (
        select(models.DbReaction)
        .filter_by(author_id=user_id)
        .filter_by(post_id=post.id)
    )
    reaction = db.execute(stmt).scalars().first()
    return reaction


def reaction_to_post(
    post_id: int, emoji: schemas.Emoji, user: models.DbUser, db: Session
) -> None:
    post = retrieve_post(user_id=user.id, post_id=post_id, db=db)
    if post.author_id == user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can't leave a reaction to your own post",
        )
    reaction = get_post_reaction(post=post, user_id=user.id, db=db)
    if reaction in post.reactions:
        reaction.emoji = emoji.value
    else:
        reaction = models.DbReaction(
            emoji=emoji.value, author_id=user.id, post_id=post_id
        )
        post.reactions.append(reaction)
    db.add(reaction)
    db.commit()
    db.refresh(reaction)
    db.refresh(post)


def remove_reaction_from_post(post_id: int, user: models.DbUser, db: Session) -> None:
    post = retrieve_post(user_id=user.id, post_id=post_id, db=db)
    reaction = get_post_reaction(post=post, user_id=user.id, db=db)
    if not reaction or reaction not in post.reactions:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can remove only your own reactions",
        )
    db.delete(reaction)
    db.commit()
