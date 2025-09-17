from fastapi import APIRouter
from app.dependencies import SessionDep
from app.models import LoginInput, RegsiterInput
from argon2 import PasswordHasher
from app.repositories import UserRepository

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
    return {
        "message": f"hello {user.username}, you are logged in successfully",
        "user": user
    }