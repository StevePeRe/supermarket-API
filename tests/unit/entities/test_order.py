import pytest
from app.domain.entities.order import Order, OrderItem, OrderStatus


class TestOrderItem:
    def test_order_item_creation(self):
        item = OrderItem(
            product_id=1,
            quantity=3,
            unit_price=15.50,
        )

        assert item.product_id == 1
        assert item.quantity == 3
        assert item.unit_price == 15.50
        assert item.id is None
        assert item.order_id is None


class TestOrder:
    def test_order_creation_with_defaults(self):
        order = Order(user_id=1)

        assert order.user_id == 1
        assert order.status == OrderStatus.PENDING
        assert order.total == 0.0
        assert order.items == []

    def test_order_creation_with_items(self):
        items = [
            OrderItem(product_id=1, quantity=2, unit_price=10.0),
            OrderItem(product_id=2, quantity=1, unit_price=25.0),
        ]
        order = Order(user_id=1, total=45.0, items=items)

        assert len(order.items) == 2
        assert order.total == 45.0


class TestOrderStatus:
    def test_order_status_values(self):
        assert OrderStatus.PENDING.value == "pending"
        assert OrderStatus.PREPARING.value == "preparing"
        assert OrderStatus.SHIPPED.value == "shipped"
        assert OrderStatus.DELIVERED.value == "delivered"
        assert OrderStatus.CANCELLED.value == "cancelled"

    def test_order_status_transitions(self):
        assert OrderStatus.PENDING == "pending"
        assert OrderStatus.SHIPPED == "shipped"
