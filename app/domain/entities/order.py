import enum
from dataclasses import dataclass, field
from datetime import datetime


class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    PREPARING = "preparing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


@dataclass
class OrderItem:
    id: int | None = None
    order_id: int | None = None
    product_id: int = 0
    quantity: int = 0
    unit_price: float = 0.0


@dataclass
class Order:
    id: int | None = None
    user_id: int = 0
    status: OrderStatus = OrderStatus.PENDING
    total: float = 0.0
    notes: str | None = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    items: list[OrderItem] = field(default_factory=list)