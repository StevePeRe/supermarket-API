from sqlalchemy.orm import Session

from app.domain.entities.user import User, UserRole
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.persistence.models import UserModel


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, db: Session):
        self.db = db

    def _to_entity(self, model: UserModel) -> User:
        return User(
            id=model.id,
            username=model.username,
            email=model.email,
            hashed_password=model.hashed_password,
            full_name=model.full_name,
            role=UserRole(model.role),
            is_active=model.is_active,
        )

    def _to_model(self, entity: User) -> UserModel:
        return UserModel(
            id=entity.id,
            username=entity.username,
            email=entity.email,
            hashed_password=entity.hashed_password,
            full_name=entity.full_name,
            role=entity.role.value,
            is_active=entity.is_active,
        )

    def create(self, user: User) -> User:
        model = self._to_model(user)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._to_entity(model)

    def get_by_id(self, user_id: int) -> User | None:
        model = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        return self._to_entity(model) if model else None

    def get_by_username(self, username: str) -> User | None:
        model = self.db.query(UserModel).filter(UserModel.username == username).first()
        return self._to_entity(model) if model else None

    def get_by_email(self, email: str) -> User | None:
        model = self.db.query(UserModel).filter(UserModel.email == email).first()
        return self._to_entity(model) if model else None

    def update(self, user: User) -> User:
        model = self.db.query(UserModel).filter(UserModel.id == user.id).first()
        if model:
            model.username = user.username
            model.email = user.email
            model.full_name = user.full_name
            model.role = user.role.value
            model.is_active = user.is_active
            self.db.commit()
            self.db.refresh(model)
        return self._to_entity(model)

    def delete(self, user_id: int) -> None:
        model = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if model:
            self.db.delete(model)
            self.db.commit()