from fastapi import Depends
from app.db import get_session
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession


SessionDep = Annotated[AsyncSession, Depends(get_session)]
