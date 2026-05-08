from app.application.dtos.inventory_dtos import InventoryCreateDTO
from app.domain.entities.inventory import Inventory
from app.domain.repositories.inventory_repository import InventoryRepository


class CreateInventoryCommand:
    def __init__(self, inventory_repo: InventoryRepository):
        self.inventory_repo = inventory_repo

    def execute(self, dto: InventoryCreateDTO) -> Inventory:
        existing = self.inventory_repo.get_by_product_id(dto.product_id)
        if existing:
            raise ValueError("Inventory already exists for this product")
        inventory = Inventory(
            product_id=dto.product_id,
            quantity=dto.quantity,
            min_stock=dto.min_stock,
        )
        return self.inventory_repo.create(inventory)


class AdjustStockCommand:
    def __init__(self, inventory_repo: InventoryRepository):
        self.inventory_repo = inventory_repo

    def execute(self, product_id: int, delta: int) -> Inventory:
        inventory = self.inventory_repo.adjust_stock(product_id, delta)
        if not inventory:
            raise ValueError("Inventory not found")
        return inventory