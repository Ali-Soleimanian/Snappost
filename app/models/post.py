from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional



class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(default="no title")
    text: str
    date: datetime
    view: int = Field(default=0)
