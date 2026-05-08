from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.infrastructure.api.dependencies.repositories import get_order_repo, get_user_repo
from app.infrastructure.api.dependencies.auth import get_current_user
from app.domain.entities.user import User
from app.domain.repositories.order_repository import OrderRepository
from app.infrastructure.persistence.database import get_db

router = APIRouter(prefix="/reports", tags=["reports"])


def require_admin(user: User = Depends(get_current_user)):
    if user.role.value != "admin":
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="Admin only")
    return user


@router.get("/top-products")
def top_products(limit: int = 10, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    from app.infrastructure.persistence.models import OrderModel, OrderItemModel, ProductModel
    results = (
        db.query(ProductModel.id, ProductModel.name, func.sum(OrderItemModel.quantity).label("total"))
        .join(OrderItemModel, OrderItemModel.product_id == ProductModel.id)
        .join(OrderModel, OrderModel.id == OrderItemModel.order_id)
        .filter(OrderModel.status.in_(["delivered", "shipped"]))
        .group_by(ProductModel.id, ProductModel.name)
        .order_by(func.sum(OrderItemModel.quantity).desc())
        .limit(limit)
        .all()
    )
    return [{"product_id": r.id, "product_name": r.name, "total_sold": int(r.total)} for r in results]


@router.get("/daily-summary")
def daily_summary(db: Session = Depends(get_db), _: User = Depends(require_admin)):
    from app.infrastructure.persistence.models import OrderModel
    results = (
        db.query(
            func.date(OrderModel.created_at).label("date"),
            func.count(OrderModel.id).label("total_orders"),
            func.sum(OrderModel.total).label("total_revenue"),
        )
        .filter(OrderModel.status.in_(["delivered", "shipped"]))
        .group_by(func.date(OrderModel.created_at))
        .order_by(func.date(OrderModel.created_at).desc())
        .all()
    )
    return [{"date": str(r.date), "total_orders": int(r.total_orders), "total_revenue": float(r.total_revenue or 0)} for r in results]