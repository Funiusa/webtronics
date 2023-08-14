from __future__ import annotations

from typing import List, TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base_class import Base

if TYPE_CHECKING:
    from .post import Post


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    full_name: Mapped[str] = mapped_column(nullable=True, index=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    is_superuser: Mapped[bool] = mapped_column(default=False, index=True)
    is_active: Mapped[bool] = mapped_column(default=True, index=True)

    posts: Mapped[List["Post"]] = relationship(cascade="all, delete-orphan")
