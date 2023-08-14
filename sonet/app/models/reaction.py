from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base_class import Base

if TYPE_CHECKING:
    from .post import Post


class Reaction(Base):
    __tablename__ = "reaction"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    emoji: Mapped[str] = mapped_column(nullable=False, unique=True)
    author_id: Mapped[int] = mapped_column(nullable=False, index=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)
    post: Mapped["Post"] = relationship(back_populates="reactions")
    # author_id: Mapped[int] = mapped_column(ForeignKey("author.id"), nullable=False),
