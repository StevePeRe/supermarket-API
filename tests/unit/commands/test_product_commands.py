import pytest
from unittest.mock import Mock
from app.application.commands.product_commands import CreateProductCommand, CreateCategoryCommand
from app.application.dtos.product_dtos import ProductCreateDTO, CategoryCreateDTO
from app.domain.entities.product import Product, Category


class TestCreateProductCommand:
    def test_create_product_success(self):
        mock_repo = Mock()
        mock_repo.get_product_by_sku.return_value = None
        mock_repo.create_product.return_value = Product(
            id=1,
            name="Test Product",
            description="Description",
            price=25.99,
            category_id=1,
            sku="TEST-SKU-001",
        )

        command = CreateProductCommand(mock_repo)
        dto = ProductCreateDTO(
            name="Test Product",
            description="Description",
            price=25.99,
            category_id=1,
            sku="TEST-SKU-001",
        )

        result = command.execute(dto)

        assert result.name == "Test Product"
        assert result.sku == "TEST-SKU-001"
        mock_repo.create_product.assert_called_once()

    def test_create_product_duplicate_sku(self):
        mock_repo = Mock()
        mock_repo.get_product_by_sku.return_value = Product(sku="EXISTING-SKU")

        command = CreateProductCommand(mock_repo)
        dto = ProductCreateDTO(
            name="New Product",
            description="Desc",
            price=10.0,
            category_id=1,
            sku="EXISTING-SKU",
        )

        with pytest.raises(ValueError, match="SKU already exists"):
            command.execute(dto)


class TestCreateCategoryCommand:
    def test_create_category_success(self):
        mock_repo = Mock()
        mock_repo.create_category.return_value = Category(
            id=1,
            name="Electronics",
            description="Electronic products",
        )

        command = CreateCategoryCommand(mock_repo)
        dto = CategoryCreateDTO(
            name="Electronics",
            description="Electronic products",
        )

        result = command.execute(dto)

        assert result.name == "Electronics"
        mock_repo.create_category.assert_called_once()
