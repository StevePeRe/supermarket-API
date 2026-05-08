from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.infrastructure.api.dependencies.repositories import get_product_repo, get_user_repo
from app.infrastructure.api.dependencies.auth import get_current_user
from app.domain.repositories.product_repository import ProductRepository
from app.domain.entities.user import User
from app.application.dtos.product_dtos import CategoryCreateDTO, CategoryResponseDTO, ProductCreateDTO, ProductResponseDTO
from app.application.commands.product_commands import CreateCategoryCommand, CreateProductCommand
from app.application.queries.product_queries import ListCategoriesQuery, GetCategoryByIdQuery, ListProductsQuery, GetProductByIdQuery

router = APIRouter(prefix="/products", tags=["products"])


def require_warehouse_or_admin(user: User = Depends(get_current_user)):
    if user.role.value not in ("warehouse", "admin"):
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="Requires warehouse or admin role")
    return user


@router.post("/categories", response_model=CategoryResponseDTO, status_code=201)
def create_category(dto: CategoryCreateDTO, product_repo: ProductRepository = Depends(get_product_repo), _: User = Depends(require_warehouse_or_admin)):
    return CreateCategoryCommand(product_repo).execute(dto)


@router.get("/categories", response_model=list[CategoryResponseDTO])
def list_categories(product_repo: ProductRepository = Depends(get_product_repo)):
    return ListCategoriesQuery(product_repo).execute()


@router.post("", response_model=ProductResponseDTO, status_code=201)
def create_product(dto: ProductCreateDTO, product_repo: ProductRepository = Depends(get_product_repo), _: User = Depends(require_warehouse_or_admin)):
    try:
        return CreateProductCommand(product_repo).execute(dto)
    except ValueError as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=list[ProductResponseDTO])
def list_products(category_id: int | None = None, product_repo: ProductRepository = Depends(get_product_repo)):
    return ListProductsQuery(product_repo).execute(category_id)


@router.get("/{product_id}", response_model=ProductResponseDTO)
def get_product(product_id: int, product_repo: ProductRepository = Depends(get_product_repo)):
    product = GetProductByIdQuery(product_repo).execute(product_id)
    if not product:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Product not found")
    return product