from datetime import datetime

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import List, Optional, Dict
from app.crud.crud_base import CRUDBase
from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate
from app.models.user import User


class CRUDPost(CRUDBase[Post, PostCreate, PostUpdate]):
    def create_with_author(
        self, db: Session, *, obj_in: PostCreate, author_id: int
    ) -> Post:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, author_id=author_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_author(
        self, db: Session, *, author_id: int, skip: int = 0, limit: int = 100
    ) -> List[Post]:
        stmt = (
            select(self.model).filter_by(author_id=author_id).offset(skip).limit(limit)
        )
        return db.execute(statement=stmt).scalars().all()

    def get_multi_by_author_reaction(
        self, db: Session, *, author_id: int, skip: int = 0, limit: int = 100
    ) -> List[Post]:
        stmt = (
            select(self.model)
            .join(self.model.reactions)
            .filter_by(author_id=author_id)
            .offset(skip)
            .limit(limit)
        )
        return db.execute(statement=stmt).scalars().all()


post = CRUDPost(Post)
