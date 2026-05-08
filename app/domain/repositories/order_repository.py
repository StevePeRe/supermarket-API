from abc import ABC, abstractmethod

from app.domain.entities.order import Order, OrderItem, OrderStatus


class OrderRepository(ABC):
    @abstractmethod
    def create_order(self, order: Order) -> Order: ...

    @abstractmethod
    def get_order_by_id(self, order_id: int) -> Order | None: ...

    @abstractmethod
    def list_orders(self, user_id: int | None = None) -> list[Order]: ...

    @abstractmethod
    def update_order_status(self, order_id: int, status: OrderStatus) -> Order | None: ...

    @abstractmethod
    def add_order_item(self, item: OrderItem) -> OrderItem: ...

    @abstractmethod
    def get_order_items(self, order_id: int) -> list[OrderItem]: ...