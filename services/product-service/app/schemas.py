"""Product service schemas."""

from pydantic import BaseModel, ConfigDict


class CategoryBase(BaseModel):
    name: str
    description: str | None = None


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class ProductBase(BaseModel):
    name: str
    description: str | None = None
    price: float
    stock: int = 0
    category_id: int
    image_url: str | None = None


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    is_active: bool
    category: Category | None = None
