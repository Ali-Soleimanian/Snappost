from fastapi import FastAPI
from app.routers import user_router, post_router


app = FastAPI(title="snappost",
            description="a basic social network API for learning and test",
            version="1.0.0")


# include user and post router
app.include_router(user_router)
app.include_router(post_router)

