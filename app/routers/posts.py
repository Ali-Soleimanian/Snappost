import uuid
from app.exeptions import *
from app.models import User
from app.db import SessionDep
from app.services import MediaService
from fastapi.responses import StreamingResponse
from app.repositories import PostRepository
from app.auth.auth_dependencies import get_current_user
from fastapi import APIRouter, Query, Depends, UploadFile, File
from app.conf.settings import ALLOWED_IMAGE_TYPES, ALLOWED_VIDEO_TYPES, MAX_FILE_SIZE

router = APIRouter(prefix="/post", tags=["Post"])


@router.post("/create", description="Create a new post with optional media")
async def write_post(
    session: SessionDep,
    current_user: User = Depends(get_current_user),
    title: str = Query(alias="Title", description="What is your post title?"),
    text: str = Query(alias="Text", description="What is your post text?"),
    media: UploadFile = File()
):
    if media.content_type not in ALLOWED_IMAGE_TYPES + ALLOWED_VIDEO_TYPES:
        raise InvalidMediaType
    
    if not media.filename:
        raise NoFilenameProvided
    
    content = await media.read()
    if len(content) > MAX_FILE_SIZE:
        raise FileTooLarge

    old_filename = media.filename
    new_filename = f"{current_user.id}_{uuid.uuid4().hex}_{old_filename}"

    media.filename = new_filename
    media_service = MediaService("post-media")
    upload_success = media_service.upload_media(media)
    
    if not upload_success:
        raise FailedToUploadMedia
    
    repo = PostRepository(session)
    post = await repo.create_post(title=title, text=text, owner_id=current_user.id, username=current_user.username, filename=media.filename)
    return {
        "message": "Post created successfully",
        "username": post.username,
        "title": post.title,
        "text": post.text,
        "views": post.views,
        "filename": post.filename
    }


@router.get("/view", description="View a post by username and title")
async def view_post(
    session: SessionDep,
    username: str = Query(alias="owner_username", description="owner username"),
    title: str = Query(alias="target_post_title", description="target post title"),
):
    repo = PostRepository(session)
    post = await repo.get_post(username, title)
    media_link = f"/post/download/{post.filename}"
    return {
        "username": post.username,
        "title": post.title,
        "text": post.text,
        "views": post.views,
        "filename": post.filename,
        "media_link": media_link
    }

@router.get("/download/{filename}")
async def download_media(filename: str):
    media_service = MediaService("post-media")
    download = media_service.download_media(filename)
    if not download:
        raise MediaNotFound
    return StreamingResponse(
        download,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
