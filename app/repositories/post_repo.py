from app.exeptions import *
from sqlalchemy import select
from argon2 import PasswordHasher
from app.models import Post
from app.repositories import UserRepository


class PostRepository:
    def __init__(self, session):
        self.session = session
        self.ph = PasswordHasher()
        self.user_repo = UserRepository(self.session)

    async def create_post(self, title: str, text: str, owner_id: int, username: str, filename: str):
        check = await self.session.execute(select(Post).where(Post.username == username, Post.title == title))
        result = check.scalar_one_or_none()
        if result:
            raise PostTitleAlreadyExsist 
        post = Post(title=title, text=text, owner_id=owner_id, username=username, filename=filename)
        self.session.add(post)
        await self.session.commit()
        await self.session.refresh(post)
        return post

    async def get_post(self, username, title):
        check = await self.session.execute(select(Post).where(Post.username == username, Post.title == title))
        post = check.scalar_one_or_none()
        if not post:
            raise PostNotFound
        else:
            post.views += 1
            self.session.add(post)
        await self.session.commit()
        return post

    async def update_post_filename(self, post_id: int, filename: str):
        check = await self.session.execute(select(Post).where(Post.id == post_id))
        post = check.scalar_one_or_none()
        if not post:
            raise PostNotFound
        post.filename = filename
        self.session.add(post)
        await self.session.commit()
        await self.session.refresh(post)
        return post
