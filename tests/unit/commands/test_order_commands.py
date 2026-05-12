import pytest
from unittest.mock import Mock
from app.application.commands.order_commands import CreateOrderCommand
from app.application.dtos.order_dtos import OrderCreateDTO, OrderItemCreateDTO
from app.domain.entities.order import Order, OrderItem
from app.domain.entities.product import Product


class TestCreateOrderCommand:
    def test_create_order_success(self):
        mock_order_repo = Mock()
        mock_product_repo = Mock()

        product1 = Product(id=1, name="Product 1", price=10.0, sku="SKU1", category_id=1)
        product2 = Product(id=2, name="Product 2", price=20.0, sku="SKU2", category_id=1)

        mock_product_repo.get_product_by_id.side_effect = lambda id: {
            1: product1,
            2: product2,
        }.get(id)

        mock_order_repo.create_order.return_value = Order(
            id=1,
            user_id=1,
            total=50.0,
            items=[
                OrderItem(product_id=1, quantity=2, unit_price=10.0),
                OrderItem(product_id=2, quantity=1, unit_price=20.0),
            ],
        )

        command = CreateOrderCommand(mock_order_repo, mock_product_repo)
        dto = OrderCreateDTO(
            items=[
                OrderItemCreateDTO(product_id=1, quantity=2),
                OrderItemCreateDTO(product_id=2, quantity=1),
            ],
            notes="Test order",
        )

        result = command.execute(user_id=1, dto=dto)

        assert result.total == 50.0
        assert len(result.items) == 2
        mock_order_repo.create_order.assert_called_once()

    def test_create_order_product_not_found(self):
        mock_order_repo = Mock()
        mock_product_repo = Mock()
        mock_product_repo.get_product_by_id.return_value = None

        command = CreateOrderCommand(mock_order_repo, mock_product_repo)
        dto = OrderCreateDTO(
            items=[OrderItemCreateDTO(product_id=999, quantity=1)],
        )

        with pytest.raises(ValueError, match="Product 999 not found"):
            command.execute(user_id=1, dto=dto)
