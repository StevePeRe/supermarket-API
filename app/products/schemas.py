from pydantic import BaseModel


class CategoryCreate(BaseModel):
    name: str
    description: str | None = None


class CategoryOut(BaseModel):
    id: int
    name: str
    description: str | None

    model_config = {"from_attributes": True}


class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: float
    category_id: int
    sku: str


class ProductOut(BaseModel):
    id: int
    name: str
    description: str | None
    price: float
    category_id: int
    sku: str
    is_active: bool

    model_config = {"from_attributes": True}
