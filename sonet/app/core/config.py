import os

from sqlalchemy import URL
from dotenv import load_dotenv
from pydantic import BaseSettings, AnyHttpUrl, validator, HttpUrl, PostgresDsn
from typing import List, Any, Union, Optional, Dict
import secrets

load_dotenv()


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SERVER_NAME: str = ""
    SERVER_HOST: AnyHttpUrl
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @classmethod
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str]]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.strip(",")]
        elif isinstance(v, (list, str)):
            return v
        else:
            raise ValueError(v)

    PROJECT_NAME: str
    # SENTRY_DSN: Optional[HttpUrl] = None
    #
    # @validator("SENTRY_DSN", pre=True)
    # def sentry_dsn_can_be_black(cls, v: str) -> Optional[str]:
    #     if len(v) == 0:
    #         return None
    #     return v

    POSTGRES_HOST: str = ""
    POSTGRES_USER: str = ""
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = ""
    POSTGRES_DB_PORT = 5432
    SQLALCHEMY_DATABASE_URI: Optional[str] = "postgresql+psycopg2"

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    postgres_url = URL.create(
        "postgresql+psycopg2",
        username=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=int(POSTGRES_DB_PORT),
        database=POSTGRES_DB,
    )

    EMAIL_TEST_USER: str = "test@example.com"
    FIRST_SUPERUSER: str = "admin"
    FIRST_SUPERUSER_EMAIL: str = "admin@gmail.com"
    FIRST_SUPERUSER_PASSWORD: str = "pass"
    USERS_OPEN_REGISTRATION: bool = True

    class Config:
        case_sensitive = True


settings = Settings()

settings.PROJECT_NAME = os.getenv("PROJECT_NAME")
settings.SERVER_HOST = os.getenv("SERVER_HOST")

settings.POSTGRES_USER = os.getenv("POSTGRES_USER")
settings.POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
settings.POSTGRES_HOST = os.getenv("DATABASE_HOST")
settings.POSTGRES_DB = os.getenv("DATABASE_NAME")
settings.POSTGRES_DB_PORT = os.getenv("DATABASE_PORT")

settings.FIRST_SUPERUSER = os.environ["SU_USERNAME"]
settings.FIRST_SUPERUSER_EMAIL = os.environ["SU_USER_EMAIL"]
settings.FIRST_SUPERUSER_PASSWORD = os.environ["SU_USER_PASS"]

API_PORT = int(os.environ["API_PORT"])

DATABASE_USER = os.getenv("DATABASE_NAME")
DATABASE_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_NAME = os.getenv("DATABASE_NAME")


url = URL.create(
    "postgresql+psycopg2",
    username=DATABASE_USER,
    password=DATABASE_PASSWORD,
    host=DATABASE_HOST,
    port=int(DATABASE_PORT),
    database=DATABASE_NAME,
)
