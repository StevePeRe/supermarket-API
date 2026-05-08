from pydantic import BaseModel


class OrderItemCreateDTO(BaseModel):
    product_id: int
    quantity: int


class OrderCreateDTO(BaseModel):
    notes: str | None = None
    items: list[OrderItemCreateDTO]


class OrderItemResponseDTO(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: float


class OrderResponseDTO(BaseModel):
    id: int
    user_id: int
    status: str
    total: float
    notes: str | None
    items: list[OrderItemResponseDTO]
    created_at: str
    updated_at: str