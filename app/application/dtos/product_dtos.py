from pydantic import BaseModel


class CategoryCreateDTO(BaseModel):
    name: str
    description: str | None = None


class CategoryResponseDTO(BaseModel):
    id: int
    name: str
    description: str | None


class ProductCreateDTO(BaseModel):
    name: str
    description: str | None = None
    price: float
    category_id: int
    sku: str


class ProductResponseDTO(BaseModel):
    id: int
    name: str
    description: str | None
    price: float
    category_id: int
    sku: str
    is_active: bool