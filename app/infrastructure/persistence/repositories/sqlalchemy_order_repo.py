from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.domain.entities.order import Order, OrderItem, OrderStatus
from app.domain.repositories.order_repository import OrderRepository
from app.infrastructure.persistence.models import OrderModel, OrderItemModel


class SQLAlchemyOrderRepository(OrderRepository):
    def __init__(self, db: Session):
        self.db = db

    def _to_order_entity(self, model: OrderModel) -> Order:
        return Order(
            id=model.id,
            user_id=model.user_id,
            status=OrderStatus(model.status),
            total=model.total,
            notes=model.notes,
            created_at=model.created_at,
            updated_at=model.updated_at,
            items=[],
        )

    def _to_item_entity(self, model: OrderItemModel) -> OrderItem:
        return OrderItem(
            id=model.id,
            order_id=model.order_id,
            product_id=model.product_id,
            quantity=model.quantity,
            unit_price=model.unit_price,
        )

    def create_order(self, order: Order) -> Order:
        model = OrderModel(
            user_id=order.user_id,
            status=order.status.value,
            total=order.total,
            notes=order.notes,
            created_at=order.created_at,
            updated_at=order.updated_at,
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)

        for item in order.items:
            item_model = OrderItemModel(
                order_id=model.id,
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=item.unit_price,
            )
            self.db.add(item_model)
        self.db.commit()

        return self._to_order_entity(model)

    def get_order_by_id(self, order_id: int) -> Order | None:
        model = self.db.query(OrderModel).filter(OrderModel.id == order_id).first()
        if not model:
            return None
        entity = self._to_order_entity(model)
        items = self.db.query(OrderItemModel).filter(OrderItemModel.order_id == order_id).all()
        entity.items = [self._to_item_entity(i) for i in items]
        return entity

    def list_orders(self, user_id: int | None = None) -> list[Order]:
        q = self.db.query(OrderModel)
        if user_id:
            q = q.filter(OrderModel.user_id == user_id)
        models = q.order_by(OrderModel.created_at.desc()).all()
        orders = []
        for m in models:
            entity = self._to_order_entity(m)
            items = self.db.query(OrderItemModel).filter(OrderItemModel.order_id == m.id).all()
            entity.items = [self._to_item_entity(i) for i in items]
            orders.append(entity)
        return orders

    def update_order_status(self, order_id: int, status: OrderStatus) -> Order | None:
        model = self.db.query(OrderModel).filter(OrderModel.id == order_id).first()
        if not model:
            return None
        model.status = status.value
        model.updated_at = datetime.now(timezone.utc)
        self.db.commit()
        self.db.refresh(model)
        return self._to_order_entity(model)

    def add_order_item(self, item: OrderItem) -> OrderItem:
        model = OrderItemModel(
            order_id=item.order_id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.unit_price,
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._to_item_entity(model)

    def get_order_items(self, order_id: int) -> list[OrderItem]:
        models = self.db.query(OrderItemModel).filter(OrderItemModel.order_id == order_id).all()
        return [self._to_item_entity(m) for m in models]