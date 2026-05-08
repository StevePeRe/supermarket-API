from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.auth.models import User
from app.reports.service import ReportService

router = APIRouter(prefix="/reports", tags=["reports"])


def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role.value != "admin":
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="Admin only")
    return current_user


@router.get("/top-products")
def top_products(
    limit: int = 10,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    return ReportService(db).top_products(limit)


@router.get("/daily-summary")
def daily_summary(
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    return ReportService(db).daily_summary()