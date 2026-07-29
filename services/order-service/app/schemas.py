"""Order service schemas."""

from pydantic import BaseModel, ConfigDict


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    price: float


class OrderItemCreate(OrderItemBase):
    pass


class OrderItem(OrderItemBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    order_id: int


class OrderBase(BaseModel):
    user_id: int
    shipping_address: str
    total_amount: float


class OrderCreate(OrderBase):
    items: list[OrderItemCreate]


class Order(OrderBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    status: str
    items: list[OrderItem] = []
