import time
import logging
from fastapi import FastAPI, staticfiles, Request
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.database.init_db import init
from tenacity import retry, stop_after_attempt, after_log, before_log, wait_fixed
from app.api.api_v1.api import api_router

description = """
## A simple RESTful API using FastAPI for a social networking application
### Functional requirements:

#### There should be some form of authentication and registration (JWT, Oauth, Oauth 2.0, etc..)
* **As a user can signup and login**
* **As a user can create, edit, delete and view posts**
* **As a user you can like or dislike other users’ posts but not your own**

"""

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=description,
    debug=True,
    version="0.0.1",
    contact={"name": "Denis", "email": "funiusa@gmail.com"},
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger=logger, log_level=logging.INFO),
    after=after_log(logger=logger, log_level=logging.WARN),
)
@app.on_event("startup")
def on_startup():
    try:
        logger.info("Initializing service")
        init()
        logger.info("Service finished initialize")
    except Exception as e:
        logger.error(e)
        raise e


if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
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


app.include_router(api_router, prefix=settings.API_V1_STR)
