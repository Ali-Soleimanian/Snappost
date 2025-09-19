from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional



class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    title: str
    text: str
    date: datetime = Field(default_factory=datetime.utcnow)
    owner_id: int
    views: int = Field(default=0)
