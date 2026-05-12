import pytest
from app.domain.entities.product import Product, Category


class TestCategory:
    def test_category_creation(self):
        category = Category(
            id=1,
            name="Electronics",
            description="Electronic products",
        )

        assert category.id == 1
        assert category.name == "Electronics"
        assert category.description == "Electronic products"

    def test_category_creation_without_description(self):
        category = Category(name="Books")

        assert category.name == "Books"
        assert category.description is None


class TestProduct:
    def test_product_creation(self):
        product = Product(
            name="Test Product",
            description="A test product",
            price=29.99,
            category_id=1,
            sku="TEST-001",
            is_active=True,
        )

        assert product.name == "Test Product"
        assert product.price == 29.99
        assert product.sku == "TEST-001"
        assert product.is_active is True

    def test_product_creation_with_defaults(self):
        product = Product(
            name="Simple Product",
            price=10.0,
            category_id=1,
            sku="SIMPLE-001",
        )

        assert product.description is None
        assert product.is_active is True
        assert product.category is None

    def test_product_creation_with_category(self):
        category = Category(id=1, name="Electronics")
        product = Product(
            name="Laptop",
            price=999.99,
            category_id=1,
            sku="LAPTOP-001",
            category=category,
        )

        assert product.category is not None
        assert product.category.name == "Electronics"
