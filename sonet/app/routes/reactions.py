from fastapi import Depends, responses, status, routing
from sqlalchemy.orm import Session

from app.database.base import get_session
from app.routes.auth import get_current_user
from app.database import cruds, schemas, models

router = routing.APIRouter(
    tags=["Reactions"],
    prefix="/api/posts"
)


@router.put("/{post_id}/reactions", status_code=status.HTTP_202_ACCEPTED)
async def reaction_to_post(
        post_id: int,
        emoji: schemas.Emoji,
        session: Session = Depends(get_session),
        cur_user: models.DbUser = Depends(get_current_user),
):
    cruds.reactions.reaction_to_post(
        post_id=post_id, emoji=emoji, user=cur_user, db=session
    )
    message = f"You just left a reaction to post {post_id}"
    return responses.PlainTextResponse(message, media_type="text/plain")


@router.delete("/{post_id}/reactions", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reaction_from_post(
        post_id: int,
        current_user: models.DbUser = Depends(get_current_user),
        session: Session = Depends(get_session),
):
    cruds.reactions.remove_reaction_from_post(
        post_id=post_id, user=current_user, db=session
    )
