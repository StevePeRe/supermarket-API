from sqlalchemy.orm import Session

from app.orders.models import Order, OrderItem, OrderStatus
from app.orders.schemas import OrderCreate
from app.products.models import Product


class OrderService:
    def __init__(self, db: Session):
        self.db = db

    def create_order(self, user_id: int, data: OrderCreate) -> Order:
        total = 0.0
        items: list[OrderItem] = []
        for item_data in data.items:
            product = self.db.query(Product).filter(Product.id == item_data.product_id).first()
            if not product:
                raise ValueError(f"Product {item_data.product_id} not found")
            subtotal = float(product.price) * item_data.quantity
            total += subtotal
            items.append(OrderItem(
                product_id=item_data.product_id,
                quantity=item_data.quantity,
                unit_price=float(product.price),
            ))
        order = Order(user_id=user_id, total=total, notes=data.notes, items=items)
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order

    def list_orders(self, user_id: int | None = None) -> list[Order]:
        q = self.db.query(Order)
        if user_id is not None:
            q = q.filter(Order.user_id == user_id)
        return q.order_by(Order.created_at.desc()).all()

    def get_order(self, order_id: int) -> Order | None:
        return self.db.query(Order).filter(Order.id == order_id).first()

    def update_status(self, order_id: int, status: OrderStatus) -> Order:
        order = self.get_order(order_id)
        if not order:
            raise ValueError("Order not found")
        order.status = status
        self.db.commit()
        self.db.refresh(order)
        return order
