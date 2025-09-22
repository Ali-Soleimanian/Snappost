from jose import jwt
from datetime import datetime, timedelta
from app.conf.settings import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY


def create_access_token(data: dict):
    credentials = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    credentials.update({"exp": expire})
    token = jwt.encode(credentials, SECRET_KEY, algorithm=ALGORITHM)
    return token
