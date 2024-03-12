from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

# class Post extends BaseModel
# schima


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostPatch(BaseModel):
    title: str


class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class UsersBase(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

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
