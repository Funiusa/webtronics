from __future__ import annotations

from datetime import datetime
from typing import Optional, List, TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base_class import Base

if TYPE_CHECKING:
    from .user import User
    from .reaction import Reaction


class Post(Base):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(unique=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(default="", nullable=True)
    content: Mapped[Optional[str]] = mapped_column(default="", nullable=True)
    creation_date: Mapped[datetime] = mapped_column(default=datetime.utcnow())
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    author: Mapped["User"] = relationship(back_populates="posts")
    reactions: Mapped[List["Reaction"]] = relationship(back_populates="post")
