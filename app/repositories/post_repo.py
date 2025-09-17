from fastapi import HTTPException
from sqlalchemy import select
from argon2 import PasswordHasher
from app.models import User, Post


class PostRepository:
    def __init__(self, session):
        self.session = session
        self.ph = PasswordHasher()

    async def check_username(self, data):
        check = await self.session.execute(select(User).where(User.username == data.username))
        return  check

    async def create_post(self, data):
        post = Post(**data.dict())
        username_existance = await self.check_username(data)
        result = username_existance.scalar_one_or_none()
        if result == None:
            raise HTTPException(status_code=401, detail="Invalid username or password")
        else:
            try:
                self.ph.verify(result.password, data.password)
            except:
                raise HTTPException(status_code=401, detail="Invalid username or password")
            post.owner_id = result.id
            self.session.add(post)
            await self.session.commit()
            await self.session.refresh(post)
        return post

    async def get_post(self, username, title):
        check = await self.session.execute(select(Post).where(Post.username == username, Post.title == title))
        posts = check.scalars().all()
        if not posts:
            raise HTTPException(status_code=403, detail="post not found")
        else:
            for post in posts:
                post.views += 1
                self.session.add(post)
            await self.session.commit()
            return posts
