from pydantic import BaseModel, Field
from .post import Post


class UserBase(BaseModel):
    username: str = Field(default="example")
    email: str = Field(default="example@mail.com")
    is_active: bool | None = True
    is_superuser: bool = False
    full_name: str | None = None


class UserCreate(UserBase):
    email: str
    username: str
    password: str


class UserUpdate(UserBase):
    password: str | None = None


class UserInDBBase(UserBase):
    id: int | None = None

    class Config:
        orm_mode = True


class User(UserInDBBase):
    posts: list[Post] = None


class UserInDB(UserInDBBase):
    hashed_password: str
