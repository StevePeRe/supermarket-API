from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.domain.entities.inventory import Inventory
from app.domain.repositories.inventory_repository import InventoryRepository
from app.infrastructure.persistence.models import InventoryModel


class SQLAlchemyInventoryRepository(InventoryRepository):
    def __init__(self, db: Session):
        self.db = db

    def _to_entity(self, model: InventoryModel) -> Inventory:
        return Inventory(
            id=model.id,
            product_id=model.product_id,
            quantity=model.quantity,
            min_stock=model.min_stock,
            updated_at=model.updated_at,
        )

    def _to_model(self, entity: Inventory) -> InventoryModel:
        return InventoryModel(
            id=entity.id,
            product_id=entity.product_id,
            quantity=entity.quantity,
            min_stock=entity.min_stock,
            updated_at=entity.updated_at,
        )

    def create(self, inventory: Inventory) -> Inventory:
        model = self._to_model(inventory)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._to_entity(model)

    def get_by_product_id(self, product_id: int) -> Inventory | None:
        model = self.db.query(InventoryModel).filter(InventoryModel.product_id == product_id).first()
        return self._to_entity(model) if model else None

    def list_all(self) -> list[Inventory]:
        models = self.db.query(InventoryModel).all()
        return [self._to_entity(m) for m in models]

    def update(self, inventory: Inventory) -> Inventory:
        model = self.db.query(InventoryModel).filter(InventoryModel.id == inventory.id).first()
        if model:
            model.quantity = inventory.quantity
            model.min_stock = inventory.min_stock
            model.updated_at = datetime.now(timezone.utc)
            self.db.commit()
            self.db.refresh(model)
        return self._to_entity(model)

    def adjust_stock(self, product_id: int, delta: int) -> Inventory | None:
        model = self.db.query(InventoryModel).filter(InventoryModel.product_id == product_id).first()
        if not model:
            return None
        model.quantity += delta
        if model.quantity < 0:
            model.quantity = 0
        model.updated_at = datetime.now(timezone.utc)
        self.db.commit()
        self.db.refresh(model)
        return self._to_entity(model)

    def get_low_stock(self) -> list[Inventory]:
        models = self.db.query(InventoryModel).filter(InventoryModel.quantity <= InventoryModel.min_stock).all()
        return [self._to_entity(m) for m in models]