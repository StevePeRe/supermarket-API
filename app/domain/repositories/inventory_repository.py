from abc import ABC, abstractmethod

from app.domain.entities.inventory import Inventory


class InventoryRepository(ABC):
    @abstractmethod
    def create(self, inventory: Inventory) -> Inventory: ...

    @abstractmethod
    def get_by_product_id(self, product_id: int) -> Inventory | None: ...

    @abstractmethod
    def list_all(self) -> list[Inventory]: ...

    @abstractmethod
    def update(self, inventory: Inventory) -> Inventory: ...

    @abstractmethod
    def adjust_stock(self, product_id: int, delta: int) -> Inventory | None: ...

    @abstractmethod
    def get_low_stock(self) -> list[Inventory]: ...