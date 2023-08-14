from app.api.api_v1.endpoints import users, login, posts, reactions
from fastapi.routing import APIRouter

api_router = APIRouter()

api_router.include_router(router=login.router, tags=["Login"])
api_router.include_router(router=users.router, tags=["Users"], prefix="/users")
api_router.include_router(router=posts.router, tags=["Posts"], prefix="/posts")
api_router.include_router(
    router=reactions.router, tags=["Reactions"], prefix="/reactions"
)
