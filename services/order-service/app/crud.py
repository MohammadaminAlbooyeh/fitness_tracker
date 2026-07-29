"""Order service CRUD."""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import Order, OrderItem
from app.schemas import OrderCreate, OrderItemCreate


async def get_order(db: AsyncSession, order_id: int) -> Order | None:
    result = await db.execute(select(Order).where(Order.id == order_id))
    return result.scalar_one_or_none()


async def get_orders(db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100) -> list[Order]:
    result = await db.execute(select(Order).where(Order.user_id == user_id).offset(skip).limit(limit))
    return list(result.scalars().all())


async def create_order(db: AsyncSession, order: OrderCreate) -> Order:
    db_order = Order(user_id=order.user_id, total_amount=order.total_amount, shipping_address=order.shipping_address)
    db.add(db_order)
    await db.commit()
    await db.refresh(db_order)
    for item in order.items:
        db_item = OrderItem(order_id=db_order.id, **item.model_dump())
        db.add(db_item)
    await db.commit()
    await db.refresh(db_order)
    return db_order
