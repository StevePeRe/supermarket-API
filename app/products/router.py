from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.auth.models import User
from app.products.schemas import CategoryCreate, CategoryOut, ProductCreate, ProductOut
from app.products.service import ProductService

router = APIRouter(prefix="/products", tags=["products"])


def require_warehouse_or_admin(current_user: User = Depends(get_current_user)):
    if current_user.role.value not in ("warehouse", "admin"):
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="Requires warehouse or admin role")
    return current_user


@router.post("/categories", response_model=CategoryOut, status_code=201)
def create_category(
    body: CategoryCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_warehouse_or_admin),
):
    return ProductService(db).create_category(body)


@router.get("/categories", response_model=list[CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return ProductService(db).list_categories()


@router.post("", response_model=ProductOut, status_code=201)
def create_product(
    body: ProductCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_warehouse_or_admin),
):
    return ProductService(db).create_product(body)


@router.get("", response_model=list[ProductOut])
def list_products(category_id: int | None = None, db: Session = Depends(get_db)):
    return ProductService(db).list_products(category_id)


@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    prod = ProductService(db).get_product(product_id)
    if not prod:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Product not found")
    return prod