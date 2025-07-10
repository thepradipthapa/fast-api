from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Annotated
from pydantic.types import conint
# Define the Post model

class User(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True 

class PostBase(BaseModel):
    title: str
    content: str
    published: bool=True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: User

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    
    class Config:
            orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]=None


class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, conint(le=1)]