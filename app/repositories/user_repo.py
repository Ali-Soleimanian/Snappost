from fastapi import HTTPException
from sqlalchemy import select
from argon2 import PasswordHasher
from app.models import User


class UserRepository:
    def __init__(self, session):
        self.session = session
        self.ph = PasswordHasher()

    async def check_username(self, data):
        check = await self.session.execute(select(User).where(User.username == data.username))
        return  check

    async def create_user(self, data):
        username_existance = await self.check_username(data)
        result =  username_existance.scalars().all()
        if result != None:
            raise HTTPException(status_code=402, detail="username already exist")
        else:
            hashed_password = self.ph.hash(data.password)
            user = User(username=data.username, password=hashed_password, age=data.age)
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
            return user

    async def authenticate_user(self, data):
        username_existance = await self.check_username(data)
        user =  username_existance.scalars().all()
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid username or password")
        else:
            try:
                self.ph.verify(user.password, data.password)
            except:
                raise HTTPException(status_code=401, detail="Invalid username or password")
            return user