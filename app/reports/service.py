from sqlalchemy import func
from sqlalchemy.orm import Session

from app.orders.models import Order, OrderItem, OrderStatus
from app.products.models import Product


class ReportService:
    def __init__(self, db: Session):
        self.db = db

    def top_products(self, limit: int = 10) -> list[dict]:
        results = (
            self.db.query(
                Product.id,
                Product.name,
                func.sum(OrderItem.quantity).label("total_sold"),
            )
            .join(OrderItem, OrderItem.product_id == Product.id)
            .join(Order, Order.id == OrderItem.order_id)
            .filter(Order.status == OrderStatus.DELIVERED)
            .group_by(Product.id, Product.name)
            .order_by(func.sum(OrderItem.quantity).desc())
            .limit(limit)
            .all()
        )
        return [
            {"product_id": r.id, "product_name": r.name, "total_sold": int(r.total_sold)}
            for r in results
        ]

    def daily_summary(self) -> list[dict]:
        results = (
            self.db.query(
                func.date(Order.created_at).label("date"),
                func.count(Order.id).label("total_orders"),
                func.sum(Order.total).label("total_revenue"),
            )
            .filter(Order.status.in_([OrderStatus.DELIVERED, OrderStatus.SHIPPED]))
            .group_by(func.date(Order.created_at))
            .order_by(func.date(Order.created_at).desc())
            .all()
        )
        return [
            {"date": str(r.date), "total_orders": int(r.total_orders), "total_revenue": float(r.total_revenue)}
            for r in results
        ]
