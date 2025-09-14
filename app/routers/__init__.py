from .users import router as user_router
from .posts import router as post_router

__all__ = [
    "user_router",
    "post_router"
    ]