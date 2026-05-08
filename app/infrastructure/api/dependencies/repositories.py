from fastapi import Depends
from sqlalchemy.orm import Session

from app.infrastructure.persistence.database import get_db
from app.infrastructure.persistence.repositories.sqlalchemy_user_repo import SQLAlchemyUserRepository
from app.infrastructure.persistence.repositories.sqlalchemy_product_repo import SQLAlchemyProductRepository
from app.infrastructure.persistence.repositories.sqlalchemy_order_repo import SQLAlchemyOrderRepository
from app.infrastructure.persistence.repositories.sqlalchemy_inventory_repo import SQLAlchemyInventoryRepository
from app.domain.repositories.user_repository import UserRepository
from app.domain.repositories.product_repository import ProductRepository
from app.domain.repositories.order_repository import OrderRepository
from app.domain.repositories.inventory_repository import InventoryRepository


def get_user_repo(db: Session = Depends(get_db)) -> UserRepository:
    return SQLAlchemyUserRepository(db)


def get_product_repo(db: Session = Depends(get_db)) -> ProductRepository:
    return SQLAlchemyProductRepository(db)


def get_order_repo(db: Session = Depends(get_db)) -> OrderRepository:
    return SQLAlchemyOrderRepository(db)


def get_inventory_repo(db: Session = Depends(get_db)) -> InventoryRepository:
    return SQLAlchemyInventoryRepository(db)