"""Cart service CRUD."""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import Cart, CartItem
from app.schemas import CartItemCreate


async def get_cart(db: AsyncSession, user_id: int) -> Cart | None:
    result = await db.execute(select(Cart).where(Cart.user_id == user_id, Cart.is_active == True))
    return result.scalar_one_or_none()


async def get_cart_items(db: AsyncSession, cart_id: int) -> list[CartItem]:
    result = await db.execute(select(CartItem).where(CartItem.cart_id == cart_id))
    return list(result.scalars().all())


async def add_item(db: AsyncSession, cart_id: int, item: CartItemCreate) -> CartItem:
    db_item = CartItem(cart_id=cart_id, **item.model_dump())
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item


async def create_cart(db: AsyncSession, user_id: int) -> Cart:
    db_cart = Cart(user_id=user_id)
    db.add(db_cart)
    await db.commit()
    await db.refresh(db_cart)
    return db_cart
