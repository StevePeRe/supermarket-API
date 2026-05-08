from app.application.dtos.product_dtos import CategoryCreateDTO, ProductCreateDTO
from app.domain.entities.product import Category, Product
from app.domain.repositories.product_repository import ProductRepository


class CreateCategoryCommand:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    def execute(self, dto: CategoryCreateDTO) -> Category:
        category = Category(name=dto.name, description=dto.description)
        return self.product_repo.create_category(category)


class CreateProductCommand:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    def execute(self, dto: ProductCreateDTO) -> Product:
        existing = self.product_repo.get_product_by_sku(dto.sku)
        if existing:
            raise ValueError("SKU already exists")
        product = Product(
            name=dto.name,
            description=dto.description,
            price=dto.price,
            category_id=dto.category_id,
            sku=dto.sku,
        )
        return self.product_repo.create_product(product)