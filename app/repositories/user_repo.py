from app.exeptions import *
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
        result = username_existance.scalar_one_or_none()
        if result != None:
            raise UsernameAlreadyExist
        else:
            hashed_password = self.ph.hash(data.password)
            user = User(username=data.username, password=hashed_password, age=data.age)
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
            return user

    async def authenticate_user(self, data):
        username_existance = await self.check_username(data)
        user =  username_existance.scalar_one_or_none()
        if user is None:
            raise InvalidUsernameOrPassword
        else:
            try:
                self.ph.verify(user.password, data.password)
            except:
                raise InvalidUsernameOrPassword
            return user