from abc import ABC, abstractmethod

from app.domain.entities.product import Category, Product


class ProductRepository(ABC):
    @abstractmethod
    def create_category(self, category: Category) -> Category: ...

    @abstractmethod
    def get_category_by_id(self, category_id: int) -> Category | None: ...

    @abstractmethod
    def list_categories(self) -> list[Category]: ...

    @abstractmethod
    def create_product(self, product: Product) -> Product: ...

    @abstractmethod
    def get_product_by_id(self, product_id: int) -> Product | None: ...

    @abstractmethod
    def list_products(self, category_id: int | None = None) -> list[Product]: ...

    @abstractmethod
    def get_product_by_sku(self, sku: str) -> Product | None: ...

    @abstractmethod
    def update_product(self, product: Product) -> Product: ...