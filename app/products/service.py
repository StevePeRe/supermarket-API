from sqlalchemy.orm import Session

from app.products.models import Category, Product
from app.products.schemas import CategoryCreate, ProductCreate


class ProductService:
    def __init__(self, db: Session):
        self.db = db

    def create_category(self, data: CategoryCreate) -> Category:
        cat = Category(name=data.name, description=data.description)
        self.db.add(cat)
        self.db.commit()
        self.db.refresh(cat)
        return cat

    def list_categories(self) -> list[Category]:
        return self.db.query(Category).all()

    def create_product(self, data: ProductCreate) -> Product:
        prod = Product(
            name=data.name,
            description=data.description,
            price=data.price,
            category_id=data.category_id,
            sku=data.sku,
        )
        self.db.add(prod)
        self.db.commit()
        self.db.refresh(prod)
        return prod

    def list_products(self, category_id: int | None = None) -> list[Product]:
        q = self.db.query(Product).filter(Product.is_active.is_(True))
        if category_id is not None:
            q = q.filter(Product.category_id == category_id)
        return q.all()

    def get_product(self, product_id: int) -> Product | None:
        return self.db.query(Product).filter(Product.id == product_id).first()
