import time
from fastapi import FastAPI, staticfiles, Request
from fastapi.middleware.cors import CORSMiddleware

from .database.base import create_database, drop_database
from app.routes import auth, user, post, reactions

app = FastAPI(
    title="My api",
    description="Small social network",
    debug=True,
)

app.include_router(router=auth.router)
app.include_router(router=user.router)
app.include_router(router=post.router)
app.include_router(router=reactions.router)


@app.on_event("startup")
def on_startup():
    # drop_database()
    create_database()
    # create_superuser()


origins = [
    "http://0.0.0.0:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", staticfiles.StaticFiles(directory="./static"), name="static")
app.mount("/images", staticfiles.StaticFiles(directory="./images"), name="images")


@app.middleware("http")
async def add_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    response.headers["duration"] = str(duration)
    return response
