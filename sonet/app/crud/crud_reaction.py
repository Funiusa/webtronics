from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import select

from typing import Optional
from app.schemas.reaction import ReactionUpdate, ReactionCreate
from app.crud.crud_base import CRUDBase
from app.models.reaction import Reaction


class CRUDReaction(CRUDBase[Reaction, ReactionCreate, ReactionUpdate]):
    def create_reaction_on_post(
        self, db: Session, *, obj_in: ReactionCreate, author_id: int
    ) -> Optional[Reaction]:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, author_id=author_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def get_reaction_by_post_author_id(
        db: Session, *, post_id: int, author_id: int
    ) -> Optional[Reaction]:
        stmt = (
            select(Reaction).filter_by(author_id=author_id).filter_by(post_id=post_id)
        )
        reaction = db.execute(statement=stmt).scalars().first()
        return reaction


reaction = CRUDReaction(Reaction)
