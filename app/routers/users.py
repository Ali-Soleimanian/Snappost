from fastapi import APIRouter, HTTPException
from app.dependencies import SessionDep
from app.models import User, LoginInput, RegsiterInput
from sqlalchemy import select
from argon2 import PasswordHasher

router = APIRouter(prefix="/user", tags=["User"])

ph = PasswordHasher()

@router.post("/register")
async def register(credetials: RegsiterInput, session: SessionDep):
    check_username = await session.execute(select(User).where(User.username == credetials.username))
    result = check_username.scalar_one_or_none()
    if result != None:
        raise HTTPException(status_code=402, detail="username already exist")
    else:
        hashed_password = ph.hash(credetials.password)
        user = User(username=credetials.username, password=hashed_password, age=credetials.age)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return {"message": f"hello {user.username} you are registerd successfully",
                "user": user
    }


@router.post("/login")
async def login(data: LoginInput, session: SessionDep):
    result = await session.execute(select(User).where(User.username == data.username))
    user = result.scalar_one_or_none()
    
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    else:
        try:
            ph.verify(user.password, data.password)
        except:
            raise HTTPException(status_code=401, detail="Invalid username or password")
        return {
            "message": f"hello {user.username}, you are logged in successfully",
            "user": user
        }