from pydantic import BaseModel


class InventoryCreateDTO(BaseModel):
    product_id: int
    quantity: int = 0
    min_stock: int = 10


class InventoryResponseDTO(BaseModel):
    id: int
    product_id: int
    quantity: int
    min_stock: int


class StockAdjustDTO(BaseModel):
    quantity: int