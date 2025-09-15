from fastapi import APIRouter, HTTPException, Query
from app.models import Post, PostInput, User
from app.dependencies import SessionDep
from sqlalchemy import select

router = APIRouter(prefix="/post", tags=["Post"])

@router.post("/create", description="post something")
async def create_post(data: PostInput, session: SessionDep):
    post = Post(**data.dict())
    check_user = await session.execute(select(User).where(User.username == data.username, User.password == data.password))
    result = check_user.scalar_one_or_none()
    if result == None:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    else:
        post.owner_id = result.id
        session.add(post)
        await session.commit()
        await session.refresh(post)
        return {
            "message": "post created sucsesfuly",
            "post": post
        }


@router.post("/view", description="what post do you want to see")
async def view_post(session: SessionDep, username: str = Query(alias="owner username"), title: str = Query(alias="target post title")):
    check = await session.execute(select(Post).where(Post.username == username, Post.title == title))
    posts = check.scalars().all()
    if not posts:
        raise HTTPException(status_code=403, detail="post not found")
    else:
        return posts
