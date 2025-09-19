from fastapi import Depends
from app.db import get_session
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer

SessionDep = Annotated[AsyncSession, Depends(get_session)]
