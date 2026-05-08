from pydantic import BaseModel


class InventoryCreate(BaseModel):
    product_id: int
    quantity: int = 0
    min_stock: int = 10


class InventoryOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    min_stock: int
    low_stock: bool = False

    model_config = {"from_attributes": True}


class StockAdjust(BaseModel):
    quantity: int
