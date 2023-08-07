from enum import Enum

from pydantic import BaseModel, Field


class Emoji(Enum):
    ok = "👍"
    funny = "😄"


class ReactionBase(BaseModel):
    emoji: str


class ReactionCreate(ReactionBase):
    emoji: str = Field(default=Emoji.ok)
    post_id: int


class Reaction(ReactionBase):
    id: int
    author_id: int
    post_id: int

    class Config:
        orm_mode = True
