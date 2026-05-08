from app.domain.entities.inventory import Inventory
from app.domain.repositories.inventory_repository import InventoryRepository


class ListInventoryQuery:
    def __init__(self, inventory_repo: InventoryRepository):
        self.inventory_repo = inventory_repo

    def execute(self) -> list[Inventory]:
        return self.inventory_repo.list_all()


class GetInventoryByProductQuery:
    def __init__(self, inventory_repo: InventoryRepository):
        self.inventory_repo = inventory_repo

    def execute(self, product_id: int) -> Inventory | None:
        return self.inventory_repo.get_by_product_id(product_id)


class GetLowStockAlertsQuery:
    def __init__(self, inventory_repo: InventoryRepository):
        self.inventory_repo = inventory_repo

    def execute(self) -> list[Inventory]:
        return self.inventory_repo.get_low_stock()