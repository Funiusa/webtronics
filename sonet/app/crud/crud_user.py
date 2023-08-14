from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.crud.crud_base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password

from typing import Union, Any, Dict


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    @staticmethod
    def is_active(_user: User) -> bool:
        return _user.is_active

    @staticmethod
    def is_superuser(_user: User) -> bool:
        return _user.is_superuser

    @staticmethod
    def get_by_email(db: Session, *, email: str) -> Optional[User]:
        stmt = select(User).filter_by(email=email)
        return db.execute(statement=stmt).scalars().first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            username=obj_in.username,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            is_superuser=obj_in.is_superuser,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        _user = self.get_by_email(db, email=email)
        if not _user:
            return None
        if not verify_password(password, _user.hashed_password):
            return None
        return _user


user = CRUDUser(User)
