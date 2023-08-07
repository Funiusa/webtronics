from datetime import datetime

from pydantic import BaseModel, FilePath, Field

from app.database.schemas.reaction import Reaction


class PostBase(BaseModel):
    title: str
    description: str
    content: str

    class Config:
        orm_mode = True


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class PostRead(PostBase):
    post_id: int
    image_url: FilePath
    timestamp: datetime
    author_id: int
    reactions: list["Reaction"] = Field(default=[])
