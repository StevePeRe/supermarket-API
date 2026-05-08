from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.auth.models import User
from app.inventory.schemas import InventoryCreate, InventoryOut, StockAdjust
from app.inventory.service import InventoryService

router = APIRouter(prefix="/inventory", tags=["inventory"])


def require_warehouse_or_admin(current_user: User = Depends(get_current_user)):
    if current_user.role.value not in ("warehouse", "admin"):
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="Requires warehouse or admin role")
    return current_user


@router.post("", response_model=InventoryOut, status_code=201)
def create_inventory(
    body: InventoryCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_warehouse_or_admin),
):
    return InventoryService(db).create(body)


@router.get("", response_model=list[InventoryOut])
def list_inventory(
    db: Session = Depends(get_db),
    _: User = Depends(require_warehouse_or_admin),
):
    records = InventoryService(db).list_all()
    return records


@router.get("/alerts", response_model=list[InventoryOut])
def low_stock_alerts(
    db: Session = Depends(get_db),
    _: User = Depends(require_warehouse_or_admin),
):
    records = InventoryService(db).low_stock_alerts()
    return records


@router.get("/{product_id}", response_model=InventoryOut)
def get_inventory(
    product_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_warehouse_or_admin),
):
    inv = InventoryService(db).get_by_product(product_id)
    if not inv:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Inventory not found")
    return inv


@router.patch("/{product_id}", response_model=InventoryOut)
def adjust_stock(
    product_id: int,
    body: StockAdjust,
    db: Session = Depends(get_db),
    _: User = Depends(require_warehouse_or_admin),
):
    service = InventoryService(db)
    try:
        return service.adjust_stock(product_id, body.quantity)
    except ValueError as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=str(e))