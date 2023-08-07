from __future__ import annotations

from datetime import datetime
from typing import Optional, List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class DbPost(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    post_id: Mapped[int] = mapped_column(nullable=False, index=True)
    title: Mapped[str] = mapped_column(unique=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(default="", nullable=True)
    content: Mapped[Optional[str]] = mapped_column(default="", nullable=True)
    image_url: Mapped[Optional[str]] = mapped_column(default="", nullable=True)
    timestamp: Mapped[datetime] = mapped_column()
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    author: Mapped["DbUser"] = relationship(back_populates="posts")
    reactions: Mapped[List["DbReaction"]] = relationship()
