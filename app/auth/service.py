from sqlalchemy.orm import Session

from app.auth.models import User
from app.auth.schemas import UserCreate
from app.core.security import hash_password, verify_password, create_access_token


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def register(self, data: UserCreate) -> User:
        existing = self.db.query(User).filter(
            (User.username == data.username) | (User.email == data.email)
        ).first()
        if existing:
            raise ValueError("Username or email already exists")
        user = User(
            username=data.username,
            email=data.email,
            hashed_password=hash_password(data.password),
            full_name=data.full_name,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def authenticate(self, username: str, password: str) -> str:
        user = self.db.query(User).filter(User.username == username).first()
        if not user or not verify_password(password, user.hashed_password):
            raise ValueError("Invalid credentials")
        if not user.is_active:
            raise ValueError("User is inactive")
        return create_access_token({"sub": str(user.id), "role": user.role.value})

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()
