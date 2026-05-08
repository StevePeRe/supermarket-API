from pydantic import BaseModel, EmailStr


class UserCreateDTO(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: str


class LoginRequestDTO(BaseModel):
    username: str
    password: str


class TokenDTO(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponseDTO(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    role: str
    is_active: bool