from __future__ import annotations

from typing import Optional, List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class DbUser(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str] = mapped_column(default="")
    email: Mapped[str] = mapped_column(unique=True, index=True)
    avatar: Mapped[Optional[str]] = mapped_column(default="", nullable=True)
    is_superuser: Mapped[bool] = mapped_column(default=False, index=True)
    is_staff: Mapped[bool] = mapped_column(default=False, index=True)
    is_active: Mapped[bool] = mapped_column(default=False, index=True)

    posts: Mapped[List["DbPost"]] = relationship(cascade="all, delete-orphan")
    reaction: Mapped["DbReaction"] = relationship()


