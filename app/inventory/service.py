from sqlalchemy.orm import Session

from app.inventory.models import Inventory
from app.inventory.schemas import InventoryCreate


class InventoryService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: InventoryCreate) -> Inventory:
        inv = Inventory(product_id=data.product_id, quantity=data.quantity, min_stock=data.min_stock)
        self.db.add(inv)
        self.db.commit()
        self.db.refresh(inv)
        return inv

    def get_by_product(self, product_id: int) -> Inventory | None:
        return self.db.query(Inventory).filter(Inventory.product_id == product_id).first()

    def list_all(self) -> list[Inventory]:
        return self.db.query(Inventory).all()

    def adjust_stock(self, product_id: int, delta: int) -> Inventory:
        inv = self.get_by_product(product_id)
        if not inv:
            raise ValueError("Inventory record not found")
        inv.quantity += delta
        if inv.quantity < 0:
            inv.quantity = 0
        self.db.commit()
        self.db.refresh(inv)
        return inv

    def low_stock_alerts(self) -> list[Inventory]:
        return self.db.query(Inventory).filter(Inventory.quantity <= Inventory.min_stock).all()
