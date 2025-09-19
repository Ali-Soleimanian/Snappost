from app.exeptions import *
from sqlalchemy import select
from argon2 import PasswordHasher
from app.models import User, Post
from app.repositories import UserRepository


class PostRepository:
    def __init__(self, session):
        self.session = session
        self.ph = PasswordHasher()
        self.user_repo = UserRepository(self.session)

    async def create_post(self, title: str, text: str, owner_id: int, username: str):
        post = Post(title=title, text=text, owner_id=owner_id, username=username)
        self.session.add(post)
        await self.session.commit()
        await self.session.refresh(post)
        return post

    async def get_post(self, username, title):
        check = await self.session.execute(select(Post).where(Post.username == username, Post.title == title))
        posts = check.scalars().all()
        if not posts:
            raise PostNotFound
        else:
            for post in posts:
                post.views += 1
                self.session.add(post)
            await self.session.commit()
            return posts
