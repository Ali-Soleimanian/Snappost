from fastapi import HTTPException

UsernameAlreadyExist = HTTPException(status_code=409, detail="Username already exists")

InvalidUsernameOrPassword = HTTPException(status_code=401, detail="Invalid username or password")

PostNotFound = HTTPException(status_code=404, detail="Post not found")

InvalidToken = HTTPException(status_code=401, detail="Invalid token")

TokenNotFound = HTTPException(status_code=404, detail="please login first")

UserNotFound = HTTPException(status_code=404, detail="User Not Found")
