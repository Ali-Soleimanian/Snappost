from fastapi import HTTPException

UsernameAlreadyExist = HTTPException(status_code=409, detail="Username already exists")

InvalidUsernameOrPassword = HTTPException(status_code=401, detail="Invalid username or password")

PostNotFound = HTTPException(status_code=404, detail="Post not found")

InvalidToken = HTTPException(status_code=401, detail="Invalid token")

TokenNotFound = HTTPException(status_code=404, detail="please login first")

UserNotFound = HTTPException(status_code=404, detail="User Not Found")

InvalidMediaType = HTTPException(status_code=400, detail="Invalid media type. Allowed types are gif, png, jpeg, mp4, avi, mov, mkv")

MediaNotFound = HTTPException(status_code=404, detail="Media Not Found")

NoFilenameProvided = HTTPException(status_code=400, detail="No filename provided")

FailedToUploadMedia = HTTPException(status_code=500, detail="Failed to upload media file")

PostTitleAlreadyExsist = HTTPException(status_code=409, detail="Post title with this username already exists")

FileTooLarge  = HTTPException(status_code=413, detail="File is to large. the largest file size is 10mb")
