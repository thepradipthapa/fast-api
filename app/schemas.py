from pydantic import BaseModel
from datetime import datetime

# Define the Post model
class PostBase(BaseModel):
    title: str
    content: str
    published: bool=True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_model=True