from datetime import datetime

from pydantic import BaseModel, FilePath

from app.schemas.reaction import Reaction


class PostBase(BaseModel):
    title: str | None = None
    description: str | None = None
    content: str | None = None


class PostCreate(PostBase):
    title: str


class PostUpdate(PostBase):
    pass


class PostInDBBase(PostBase):
    id: int
    title: str
    author_id: int
    creation_date: datetime
    reactions: list["Reaction"] | None = None

    class Config:
        orm_mode = True


class Post(PostInDBBase):
    pass


class PostInDB(PostInDBBase):
    pass
