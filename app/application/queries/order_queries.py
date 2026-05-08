from app.domain.entities.order import Order
from app.domain.repositories.order_repository import OrderRepository


class ListOrdersQuery:
    def __init__(self, order_repo: OrderRepository):
        self.order_repo = order_repo

    def execute(self, user_id: int | None = None) -> list[Order]:
        return self.order_repo.list_orders(user_id)


class GetOrderByIdQuery:
    def __init__(self, order_repo: OrderRepository):
        self.order_repo = order_repo

    def execute(self, order_id: int) -> Order | None:
        return self.order_repo.get_order_by_id(order_id)