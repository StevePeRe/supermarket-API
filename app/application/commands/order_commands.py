from app.application.dtos.order_dtos import OrderCreateDTO
from app.domain.entities.order import Order, OrderItem
from app.domain.repositories.order_repository import OrderRepository
from app.domain.repositories.product_repository import ProductRepository


class CreateOrderCommand:
    def __init__(self, order_repo: OrderRepository, product_repo: ProductRepository):
        self.order_repo = order_repo
        self.product_repo = product_repo

    def execute(self, user_id: int, dto: OrderCreateDTO) -> Order:
        total = 0.0
        items = []
        for item_dto in dto.items:
            product = self.product_repo.get_product_by_id(item_dto.product_id)
            if not product:
                raise ValueError(f"Product {item_dto.product_id} not found")
            subtotal = product.price * item_dto.quantity
            total += subtotal
            items.append(OrderItem(
                product_id=item_dto.product_id,
                quantity=item_dto.quantity,
                unit_price=product.price,
            ))
        order = Order(user_id=user_id, total=total, notes=dto.notes, items=items)
        return self.order_repo.create_order(order)