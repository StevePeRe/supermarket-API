from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.schemas import LoginRequest, Token, UserCreate, UserOut
from app.auth.service import AuthService
from app.core.database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut, status_code=201)
def register(body: UserCreate, db: Session = Depends(get_db)):
    service = AuthService(db)
    try:
        user = service.register(body)
        return user
    except ValueError as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=409, detail=str(e))


@router.post("/login", response_model=Token)
def login(body: LoginRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    try:
        token = service.authenticate(body.username, body.password)
        return Token(access_token=token)
    except ValueError as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail=str(e))
