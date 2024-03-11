from pydantic import BaseModel
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
    title:str

class Post(PostBase):
    id: int
    created_at: datetime
    class Config:
        orm_mode=True