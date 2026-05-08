from dataclasses import dataclass


@dataclass
class Category:
    id: int | None = None
    name: str = ""
    description: str | None = None


@dataclass
class Product:
    id: int | None = None
    name: str = ""
    description: str | None = None
    price: float = 0.0
    category_id: int = 0
    sku: str = ""
    is_active: bool = True
    category: Category | None = None