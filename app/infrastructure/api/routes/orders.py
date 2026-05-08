from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.infrastructure.api.dependencies.repositories import get_order_repo, get_product_repo, get_user_repo
from app.infrastructure.api.dependencies.auth import get_current_user
from app.domain.repositories.order_repository import OrderRepository
from app.domain.repositories.product_repository import ProductRepository
from app.domain.entities.user import User
from app.application.dtos.order_dtos import OrderCreateDTO, OrderResponseDTO
from app.application.commands.order_commands import CreateOrderCommand
from app.application.queries.order_queries import ListOrdersQuery, GetOrderByIdQuery

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("", response_model=OrderResponseDTO, status_code=201)
def create_order(dto: OrderCreateDTO, order_repo: OrderRepository = Depends(get_order_repo), product_repo: ProductRepository = Depends(get_product_repo), current_user: User = Depends(get_current_user)):
    try:
        order = CreateOrderCommand(order_repo, product_repo).execute(current_user.id, dto)
        return OrderResponseDTO(
            id=order.id,
            user_id=order.user_id,
            status=order.status.value,
            total=order.total,
            notes=order.notes,
            items=[{"id": i.id, "product_id": i.product_id, "quantity": i.quantity, "unit_price": i.unit_price} for i in order.items],
            created_at=order.created_at.isoformat(),
            updated_at=order.updated_at.isoformat(),
        )
    except ValueError as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=list[OrderResponseDTO])
def list_orders(order_repo: OrderRepository = Depends(get_order_repo), current_user: User = Depends(get_current_user)):
    user_id = current_user.id if current_user.role.value != "admin" else None
    orders = ListOrdersQuery(order_repo).execute(user_id)
    return [OrderResponseDTO(
        id=o.id,
        user_id=o.user_id,
        status=o.status.value,
        total=o.total,
        notes=o.notes,
        items=[{"id": i.id, "product_id": i.product_id, "quantity": i.quantity, "unit_price": i.unit_price} for i in o.items],
        created_at=o.created_at.isoformat(),
        updated_at=o.updated_at.isoformat(),
    ) for o in orders]


@router.get("/{order_id}", response_model=OrderResponseDTO)
def get_order(order_id: int, order_repo: OrderRepository = Depends(get_order_repo), current_user: User = Depends(get_current_user)):
    order = GetOrderByIdQuery(order_repo).execute(order_id)
    if not order:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Order not found")
    if current_user.role.value != "admin" and order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return OrderResponseDTO(
        id=order.id,
        user_id=order.user_id,
        status=order.status.value,
        total=order.total,
        notes=order.notes,
        items=[{"id": i.id, "product_id": i.product_id, "quantity": i.quantity, "unit_price": i.unit_price} for i in order.items],
        created_at=order.created_at.isoformat(),
        updated_at=order.updated_at.isoformat(),
    )