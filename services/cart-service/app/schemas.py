"""Cart service schemas."""

from pydantic import BaseModel, ConfigDict


class CartItemBase(BaseModel):
    product_id: int
    quantity: int = 1
    price: float


class CartItemCreate(CartItemBase):
    pass


class CartItem(CartItemBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    cart_id: int


class Cart(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    is_active: bool
    items: list[CartItem] = []
