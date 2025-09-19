from fastapi import APIRouter, Query, Depends
from app.models import User
from app.db import SessionDep
from app.auth.auth_dependencies import get_current_user
from app.repositories import PostRepository

router = APIRouter(prefix="/post", tags=["Post"])

@router.post("/create", description="post something")
async def write_post(
    session: SessionDep,
    current_user: User = Depends(get_current_user),
    title: str = Query(alias="Title", description="Whats your post title"),
    text: str = Query(alias="Text", description="Whats your post text"),
):

    repo = PostRepository(session)
    post = await repo.create_post(title=title, text=text, owner_id=current_user.id, username=current_user.username)
    return {
        "message": "Post created successfully",
        "post": post
    }


@router.post("/view", description="what post do you want to see")
async def view_post(
    session: SessionDep,
    username: str = Query(alias="owner_username", description="owner username"),
    title: str = Query(alias="target_post_title", description="target post title"),
):
    repo = PostRepository(session)
    posts = await repo.get_post(username, title)
    return posts
