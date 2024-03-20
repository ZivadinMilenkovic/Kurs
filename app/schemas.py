from typing import Optional
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from enum import IntEnum

# class Post extends BaseModel
# schima

class TypeEnum(IntEnum):
    post=1
    story=2

class PostBase(BaseModel):
    title: str
    type_of_post: TypeEnum = TypeEnum.post
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostPatch(BaseModel):
    title: str


class UsersBase(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class Post(PostBase):
    id: int
    created_at: datetime
    type_of_post:str
    owner_id: int
    owner: UserOut

    class Config:
        from_attributes = True


class Login(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


class Vote(BaseModel):
    post_id: int
    dir: bool


class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        from_attributes = True
