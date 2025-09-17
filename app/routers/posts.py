from fastapi import APIRouter, Query
from app.models import PostInput
from app.dependencies import SessionDep
from app.repositories import PostRepository
from argon2 import PasswordHasher

router = APIRouter(prefix="/post", tags=["Post"])

ph = PasswordHasher()

@router.post("/create", description="post something")
async def write_post(data: PostInput, session: SessionDep):
    repo = PostRepository(session)
    post = await repo.create_post(data)
    return {
        "message": "post created sucsesfuly",
        "post": post
    }


@router.post("/view", description="what post do you want to see")
async def view_post(session: SessionDep, username: str = Query(alias="owner username"), title: str = Query(alias="target post title")):
    repo = PostRepository(session)
    posts = await repo.get_post(username, title)
    return posts
