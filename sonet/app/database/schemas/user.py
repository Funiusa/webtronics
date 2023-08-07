from pydantic import BaseModel, Field
from .post import PostRead


class UserBase(BaseModel):
    username: str = Field(default="exampleuser")
    email: str = Field(default="example@mail.com")

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    username: str
    email: str
    avatar: str = ""


class UserRead(UserBase):
    id: int
    posts: list["PostRead"] = []
