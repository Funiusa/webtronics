from sqlalchemy.orm import Session
from app import crud, schemas
from app.core.config import settings
from app.database.session import SessionLocal, engine
from app.database.base_class import Base


def init_db(db: Session) -> None:
    # Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER_EMAIL)
    if not user:
        user_in = schemas.UserCreate(
            username=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            email=settings.FIRST_SUPERUSER_EMAIL,
            is_superuser=True,
        )
        user = crud.user.create(db, obj_in=user_in)


def init() -> None:
    db = SessionLocal()
    init_db(db)
