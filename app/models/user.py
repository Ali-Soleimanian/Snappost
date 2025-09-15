from sqlmodel import SQLModel, Field
from typing import Optional



class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(min_length=5)
    password: str
    age: int


class RegsiterInput(SQLModel):
    username: str
    password: str
    age: int


class LoginInput(SQLModel):
    username: str
    password: str