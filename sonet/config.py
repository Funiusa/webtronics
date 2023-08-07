import os

from sqlalchemy import URL
from dotenv import load_dotenv

load_dotenv()

DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_USER = os.getenv("POSTGRES_USER")
DATABASE_PASSWORD = os.getenv("POSTGRES_USER")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")

SU_USER_TELEGRAM = int(os.environ["SU_USER_TELEGRAM"])
SU_USERNAME = os.environ["SU_USERNAME"]
SU_USER_EMAIL = os.environ["SU_USER_EMAIL"]
SU_USER_PASS = os.environ["SU_USER_PASS"]
API_PORT = int(os.environ["API_PORT"])

# async_url = URL.create(
#     "postgresql+asyncpg",
#     username=DATABASE_USER,
#     password=DATABASE_PASSWORD,
#     host=DATABASE_HOST,
#     port=int(DATABASE_PORT),
#     database=DATABASE_NAME,
# )

url = URL.create(
    "postgresql+psycopg2",
    username=DATABASE_USER,
    password=DATABASE_PASSWORD,
    host=DATABASE_HOST,
    port=int(DATABASE_PORT),
    database=DATABASE_NAME,
)
# url = f"postgresql+psycopg2://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
