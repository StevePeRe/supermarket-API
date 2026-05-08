from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.infrastructure.api.dependencies.repositories import get_user_repo
from app.infrastructure.api.dependencies.auth import get_current_user
from app.domain.repositories.user_repository import UserRepository
from app.domain.entities.user import User
from app.application.dtos.auth_dtos import UserCreateDTO, LoginRequestDTO, TokenDTO, UserResponseDTO
from app.application.commands.auth_commands import RegisterUserCommand, LoginCommand

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponseDTO, status_code=201)
def register(dto: UserCreateDTO, user_repo: UserRepository = Depends(get_user_repo)):
    try:
        user = RegisterUserCommand(user_repo).execute(dto)
        return user
    except ValueError as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=409, detail=str(e))


@router.post("/login", response_model=TokenDTO)
def login(dto: LoginRequestDTO, user_repo: UserRepository = Depends(get_user_repo)):
    try:
        token = LoginCommand(user_repo).execute(dto)
        return token
    except ValueError as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail=str(e))