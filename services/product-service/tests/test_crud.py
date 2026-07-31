"""Tests for product-service CRUD operations."""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas


@pytest.mark.asyncio
async def test_create_category(db_session: AsyncSession):
    cat_data = schemas.CategoryCreate(name="Electronics", description="Electronic items")
    category = await crud.create_category(db_session, cat_data)
    assert category.id is not None
    assert category.name == "Electronics"


@pytest.mark.asyncio
async def test_get_categories(db_session: AsyncSession):
    cat1 = schemas.CategoryCreate(name="Books", description="Books and media")
    cat2 = schemas.CategoryCreate(name="Clothing", description="Fashion items")
    await crud.create_category(db_session, cat1)
    await crud.create_category(db_session, cat2)
    categories = await crud.get_categories(db_session)
    assert len(categories) >= 2


@pytest.mark.asyncio
async def test_create_product(db_session: AsyncSession):
    category = schemas.CategoryCreate(name="TestCat", description="Test")
    cat = await crud.create_category(db_session, category)
    product_data = schemas.ProductCreate(
        name="Test Product",
        description="A test product",
        price=99.99,
        stock=10,
        category_id=cat.id
    )
    product = await crud.create_product(db_session, product_data)
    assert product.id is not None
    assert product.name == "Test Product"
    assert product.price == 99.99


@pytest.mark.asyncio
async def test_get_product(db_session: AsyncSession):
    category = schemas.CategoryCreate(name="TestCat2", description="Test")
    cat = await crud.create_category(db_session, category)
    product_data = schemas.ProductCreate(
        name="Get Test Product",
        description="A product to fetch",
        price=49.99,
        stock=5,
        category_id=cat.id
    )
    created = await crud.create_product(db_session, product_data)
    fetched = await crud.get_product(db_session, created.id)
    assert fetched is not None
    assert fetched.name == "Get Test Product"


@pytest.mark.asyncio
async def test_get_product_not_found(db_session: AsyncSession):
    result = await crud.get_product(db_session, 99999)
    assert result is None


@pytest.mark.asyncio
async def test_get_products(db_session: AsyncSession):
    category = schemas.CategoryCreate(name="TestCat3", description="Test")
    cat = await crud.create_category(db_session, category)
    for i in range(3):
        product_data = schemas.ProductCreate(
            name=f"Product {i}",
            description="desc",
            price=10.0 + i,
            stock=5,
            category_id=cat.id
        )
        await crud.create_product(db_session, product_data)
    products = await crud.get_products(db_session, skip=0, limit=100)
    assert len(products) >= 3
