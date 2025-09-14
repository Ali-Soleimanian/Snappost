from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional



class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    text: str
    date: datetime = Field(default_factory=datetime.utcnow)
    owner_id: int


class PostInput(SQLModel):
    username: str
    password: str
    title: str
    text: str


class ViewPost(SQLModel):
    owner_username: str
    title: str