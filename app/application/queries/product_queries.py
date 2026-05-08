from app.domain.entities.product import Category, Product
from app.domain.repositories.product_repository import ProductRepository


class ListCategoriesQuery:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    def execute(self) -> list[Category]:
        return self.product_repo.list_categories()


class GetCategoryByIdQuery:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    def execute(self, category_id: int) -> Category | None:
        return self.product_repo.get_category_by_id(category_id)


class ListProductsQuery:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    def execute(self, category_id: int | None = None) -> list[Product]:
        return self.product_repo.list_products(category_id)


class GetProductByIdQuery:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    def execute(self, product_id: int) -> Product | None:
        return self.product_repo.get_product_by_id(product_id)