from fastapi import Depends
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from app.auth.auth_token import SECRET_KEY, ALGORITHM
from app.exeptions import *
from typing import Annotated
from app.models import User
from app.db.db_dependencies import SessionDep
from sqlalchemy import select
from fastapi import Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

bearer_scheme = HTTPBearer()

TokenDep = OAuth2PasswordBearer(tokenUrl="/user/login")

async def get_current_user(session: SessionDep, credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise TokenNotFound
    except JWTError:
        raise InvalidToken

    result = await session.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()
    if user is None:
        raise UserNotFound
    return user
