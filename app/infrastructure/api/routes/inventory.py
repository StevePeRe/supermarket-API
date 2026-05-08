from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.infrastructure.api.dependencies.repositories import get_inventory_repo, get_user_repo
from app.infrastructure.api.dependencies.auth import get_current_user
from app.domain.repositories.inventory_repository import InventoryRepository
from app.domain.entities.user import User
from app.application.dtos.inventory_dtos import InventoryCreateDTO, InventoryResponseDTO, StockAdjustDTO
from app.application.commands.inventory_commands import CreateInventoryCommand, AdjustStockCommand
from app.application.queries.inventory_queries import ListInventoryQuery, GetInventoryByProductQuery, GetLowStockAlertsQuery

router = APIRouter(prefix="/inventory", tags=["inventory"])


def require_warehouse_or_admin(user: User = Depends(get_current_user)):
    if user.role.value not in ("warehouse", "admin"):
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="Requires warehouse or admin role")
    return user


@router.post("", response_model=InventoryResponseDTO, status_code=201)
def create_inventory(dto: InventoryCreateDTO, inventory_repo: InventoryRepository = Depends(get_inventory_repo), _: User = Depends(require_warehouse_or_admin)):
    try:
        inv = CreateInventoryCommand(inventory_repo).execute(dto)
        return InventoryResponseDTO(id=inv.id, product_id=inv.product_id, quantity=inv.quantity, min_stock=inv.min_stock)
    except ValueError as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=list[InventoryResponseDTO])
def list_inventory(inventory_repo: InventoryRepository = Depends(get_inventory_repo), _: User = Depends(require_warehouse_or_admin)):
    return ListInventoryQuery(inventory_repo).execute()


@router.get("/alerts", response_model=list[InventoryResponseDTO])
def low_stock_alerts(inventory_repo: InventoryRepository = Depends(get_inventory_repo), _: User = Depends(require_warehouse_or_admin)):
    return GetLowStockAlertsQuery(inventory_repo).execute()


@router.get("/{product_id}", response_model=InventoryResponseDTO)
def get_inventory(product_id: int, inventory_repo: InventoryRepository = Depends(get_inventory_repo), _: User = Depends(require_warehouse_or_admin)):
    inv = GetInventoryByProductQuery(inventory_repo).execute(product_id)
    if not inv:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Inventory not found")
    return inv


@router.patch("/{product_id}", response_model=InventoryResponseDTO)
def adjust_stock(product_id: int, dto: StockAdjustDTO, inventory_repo: InventoryRepository = Depends(get_inventory_repo), _: User = Depends(require_warehouse_or_admin)):
    try:
        inv = AdjustStockCommand(inventory_repo).execute(product_id, dto.quantity)
        return InventoryResponseDTO(id=inv.id, product_id=inv.product_id, quantity=inv.quantity, min_stock=inv.min_stock)
    except ValueError as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=str(e))