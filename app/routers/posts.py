from fastapi import APIRouter


router = APIRouter(prefix="/post", tags=["Post"])

@router.get("/", description="post something")
async def post():
    return {"coming soon"}