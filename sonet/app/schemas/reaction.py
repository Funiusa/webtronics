from enum import Enum

from pydantic import BaseModel, Field


class Emoji(Enum):
    ok = "👍"
    funny = "😄"


class ReactionBase(BaseModel):
    emoji: str = Field(default=Emoji.ok)


class ReactionCreate(ReactionBase):
    author_id: int
    post_id: int


class ReactionUpdate(ReactionBase):
    emoji: str = None


class ReactionInDBBase(ReactionBase):
    id: int
    author_id: int
    post_id: int

    class Config:
        orm_mode = True


class Reaction(ReactionInDBBase):
    pass


class ReactionInDB(ReactionInDBBase):
    pass
