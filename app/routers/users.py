from fastapi import APIRouter, Query, HTTPException
from app.db.db_dependencies import SessionDep
from app.models import LoginInput, RegsiterInput
from argon2 import PasswordHasher
from app.repositories import UserRepository, PostRepository
from app.auth import create_access_token
from app.auth.auth_token import SECRET_KEY, ALGORITHM
from jose import jwt, JWTError
from datetime import datetime


router = APIRouter(prefix="/user", tags=["User"])

ph = PasswordHasher()

@router.post("/register")
async def register(data: RegsiterInput, session: SessionDep):
    repo = UserRepository(session)
    user = await repo.create_user(data)
    return {"message": f"hello {user.username} you are registerd successfully",
            "user": user
}


@router.post("/login")
async def login(data: LoginInput, session: SessionDep):
    repo = UserRepository(session)
    user = await repo.authenticate_user(data)
    token = create_access_token({"sub": data.username})
    return {
        "message": f"hello {user.username}, you are logged in successfully",
        "access_token": token,
        "token_type": "bearer",
        "user": user
    }
