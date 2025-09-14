from fastapi import APIRouter, HTTPException
from app.dependencies import SessionDep
from app.models import User, LoginInput
from sqlalchemy import select


router = APIRouter(prefix="/user", tags=["User"])

@router.post("/register", tags=["register"])
async def register(user: User, session: SessionDep):
    session.add(user)
    await session.commit()
    await session.refresh(user)

    return {"message": f"hello {user.username} you are registerd successfully",
            "user": user
}


@router.post("/login")
async def login(data: LoginInput, session: SessionDep):
    result = await session.execute(
        select(User).where(User.username == data.username)
    )
    user = result.scalar_one_or_none()
    
    if user is None or data.password != user.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    return {
        "message": f"hello {user.username}, you are logged in successfully",
        "user": user
    }