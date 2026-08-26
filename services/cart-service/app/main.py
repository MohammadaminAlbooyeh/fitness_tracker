"""Cart service FastAPI app."""

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from shared_lib.database import get_db
from shared_lib.security import get_current_user
from app import models, schemas, crud

app = FastAPI(title="Cart Service", version="1.0.0")


@app.post("/carts/", response_model=schemas.Cart, status_code=201)
async def create_cart(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return await crud.create_cart(db, user_id)


@app.get("/carts/{user_id}", response_model=schemas.Cart)
async def get_cart(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    cart = await crud.get_cart(db, user_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    items = await crud.get_cart_items(db, cart.id)
    return schemas.Cart(**cart.__dict__, items=items)


@app.post("/carts/{user_id}/items", response_model=schemas.CartItem, status_code=201)
async def add_item(
    user_id: int,
    item: schemas.CartItemCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    cart = await crud.get_cart(db, user_id)
    if not cart:
        cart = await crud.create_cart(db, user_id)
    return await crud.add_item(db, cart.id, item)
