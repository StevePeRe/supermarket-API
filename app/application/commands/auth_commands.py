from app.application.dtos.auth_dtos import UserCreateDTO, LoginRequestDTO, TokenDTO, UserResponseDTO
from app.domain.entities.user import User, UserRole
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.auth.jwt_handler import create_access_token
from app.infrastructure.auth.password_handler import hash_password, verify_password


class RegisterUserCommand:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def execute(self, dto: UserCreateDTO) -> UserResponseDTO:
        existing = self.user_repo.get_by_username(dto.username)
        if existing:
            raise ValueError("Username already exists")
        existing_email = self.user_repo.get_by_email(dto.email)
        if existing_email:
            raise ValueError("Email already exists")

        user = User(
            username=dto.username,
            email=dto.email,
            hashed_password=hash_password(dto.password),
            full_name=dto.full_name,
            role=UserRole.WAREHOUSE,
        )
        created = self.user_repo.create(user)
        return UserResponseDTO(**created.to_dict())


class LoginCommand:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def execute(self, dto: LoginRequestDTO) -> TokenDTO:
        user = self.user_repo.get_by_username(dto.username)
        if not user or not verify_password(dto.password, user.hashed_password):
            raise ValueError("Invalid credentials")
        if not user.is_active:
            raise ValueError("User is inactive")
        token = create_access_token({"sub": str(user.id), "role": user.role.value})
        return TokenDTO(access_token=token)