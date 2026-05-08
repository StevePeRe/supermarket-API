from pydantic import BaseModel


class TopProduct(BaseModel):
    product_id: int
    product_name: str
    total_sold: int


class DailySummary(BaseModel):
    date: str
    total_orders: int
    total_revenue: float
