from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.auth.models import User
from app.orders.schemas import OrderCreate, OrderOut
from app.orders.service import OrderService

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("", response_model=OrderOut, status_code=201)
def create_order(
    body: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = OrderService(db)
    try:
        return service.create_order(user_id=current_user.id, data=body)
    except ValueError as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=list[OrderOut])
def list_orders(
    user_id: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role.value == "admin":
        return OrderService(db).list_orders(user_id)
    return OrderService(db).list_orders(user_id=current_user.id)


@router.get("/{order_id}", response_model=OrderOut)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    order = OrderService(db).get_order(order_id)
    if not order:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Order not found")
    if current_user.role.value != "admin" and order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return order