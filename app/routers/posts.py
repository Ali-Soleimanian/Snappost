from fastapi import APIRouter, HTTPException
from app.models import Post, PostInput, ViewPost, User
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