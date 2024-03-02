from pydantic import BaseModel, EmailStr, conint
from datetime import  datetime
from typing import Optional, Union




class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class Userout(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True



class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: Userout

    class Config:
        from_attributes = True


class PostOut(BaseModel):
    Post: Post
    vote: int

    class Config:
        from_attributes = True



class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


class Vote(BaseModel):
    post_id: int
    dir: int = conint(ge=0, le=1)
