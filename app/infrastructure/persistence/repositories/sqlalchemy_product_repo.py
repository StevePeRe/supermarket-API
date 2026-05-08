from sqlalchemy.orm import Session

from app.domain.entities.product import Category, Product
from app.domain.repositories.product_repository import ProductRepository
from app.infrastructure.persistence.models import CategoryModel, ProductModel


class SQLAlchemyProductRepository(ProductRepository):
    def __init__(self, db: Session):
        self.db = db

    def _to_category_entity(self, model: CategoryModel) -> Category:
        return Category(id=model.id, name=model.name, description=model.description)

    def _to_category_model(self, entity: Category) -> CategoryModel:
        return CategoryModel(id=entity.id, name=entity.name, description=entity.description)

    def _to_product_entity(self, model: ProductModel) -> Product:
        return Product(
            id=model.id,
            name=model.name,
            description=model.description,
            price=model.price,
            category_id=model.category_id,
            sku=model.sku,
            is_active=model.is_active,
            category=self._to_category_entity(model.category) if model.category else None,
        )

    def _to_product_model(self, entity: Product) -> ProductModel:
        return ProductModel(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            price=entity.price,
            category_id=entity.category_id,
            sku=entity.sku,
            is_active=entity.is_active,
        )

    def create_category(self, category: Category) -> Category:
        model = self._to_category_model(category)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._to_category_entity(model)

    def get_category_by_id(self, category_id: int) -> Category | None:
        model = self.db.query(CategoryModel).filter(CategoryModel.id == category_id).first()
        return self._to_category_entity(model) if model else None

    def list_categories(self) -> list[Category]:
        models = self.db.query(CategoryModel).all()
        return [self._to_category_entity(m) for m in models]

    def create_product(self, product: Product) -> Product:
        model = self._to_product_model(product)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._to_product_entity(model)

    def get_product_by_id(self, product_id: int) -> Product | None:
        model = self.db.query(ProductModel).filter(ProductModel.id == product_id).first()
        return self._to_product_entity(model) if model else None

    def list_products(self, category_id: int | None = None) -> list[Product]:
        q = self.db.query(ProductModel).filter(ProductModel.is_active.is_(True))
        if category_id:
            q = q.filter(ProductModel.category_id == category_id)
        models = q.all()
        return [self._to_product_entity(m) for m in models]

    def get_product_by_sku(self, sku: str) -> Product | None:
        model = self.db.query(ProductModel).filter(ProductModel.sku == sku).first()
        return self._to_product_entity(model) if model else None

    def update_product(self, product: Product) -> Product:
        model = self.db.query(ProductModel).filter(ProductModel.id == product.id).first()
        if model:
            model.name = product.name
            model.description = product.description
            model.price = product.price
            model.category_id = product.category_id
            model.is_active = product.is_active
            self.db.commit()
            self.db.refresh(model)
        return self._to_product_entity(model)