from dataclasses import dataclass
from datetime import datetime


@dataclass
class Inventory:
    id: int | None = None
    product_id: int = 0
    quantity: int = 0
    min_stock: int = 10
    updated_at: datetime = None