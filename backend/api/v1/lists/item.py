from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.payloads import ExistingItem, CreateItem, CreatedResponse, UpdateItem
from api.utils import get_current_user, get_session
from api.v1.lists.router import router
from models.schema import User, Item, ShoppingList, Collaborator


@router.get("/{sl_id}/items")
async def get_items(
    sl_id: int,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> list[ExistingItem]:
    stmt = (
        select(Item)
        .join(ShoppingList)
        .where(
            (ShoppingList.user_id == user.id) | (Collaborator.user_id == user.id),
            ShoppingList.id == sl_id,
        )
    )
    cursor = await session.execute(stmt)
    return [
        ExistingItem(
            id=item.id, name=item.name, description=item.description, quantity=item.quantity
        )
        for item in cursor.scalars()
    ]


@router.get("/{sl_id}/items/{item_id}")
async def get_item(
    sl_id: int,
    item_id: int,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> list[ExistingItem]:
    stmt = (
        select(Item)
        .join(ShoppingList)
        .where(
            (ShoppingList.user_id == user.id) | (Collaborator.user_id == user.id),
            ShoppingList.id == sl_id,
            Item.id == item_id
        )
    )
    cursor = await session.execute(stmt)
    return [
        ExistingItem(
            id=item.id, name=item.name, description=item.description, quantity=item.quantity
        )
        for item in cursor.scalars()
    ]


@router.post("/{sl_id}/items")
async def add_item(
    sl_id: int,
    item: CreateItem,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
) -> CreatedResponse:
    stmt = (
        select(Item)
        .join(ShoppingList)
        .where(
            (ShoppingList.user_id == user.id) | (Collaborator.user_id == user.id),
            ShoppingList.id == sl_id,
        )
    )
    cursor = await session.execute(stmt)
    shopping_list = cursor.scalar()
    new_item = Item(name=item.name, quantity=item.quantity, description=item.description, sl_id=shopping_list.id)
    session.add(new_item)
    await session.commit()
    return CreatedResponse(id=new_item.id)


@router.patch("/{sl_id}/items/{item_id}")
async def update_item(
    sl_id: int,
    item_id: int,
    item: UpdateItem,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    if not any(attr for attr in (item.name, item.quantity, item.description)):
        raise HTTPException(status_code=422, detail="Can't set everything to null")
    stmt = (
        select(Item)
        .join(ShoppingList)
        .where(
            (ShoppingList.user_id == user.id) | (Collaborator.user_id == user.id),
            ShoppingList.id == sl_id,
            Item.id == item_id
        )
    )
    cursor = await session.execute(stmt)
    item_inst = cursor.scalar()
    if item.name:
        item_inst.name = item.name
    if item.quantity:
        item_inst.quantity = item.quantity
    if item.description:
        item_inst.description = item.description

    await session.commit()


@router.delete("/{sl_id}/items/{item_id}")
async def remove_item(
    sl_id: int,
    item_id: int,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    stmt = (
        select(Item)
        .join(ShoppingList)
        .where(
            (ShoppingList.user_id == user.id) | (Collaborator.user_id == user.id),
            ShoppingList.id == sl_id,
            Item.id == item_id,
        )
    )
    cursor = await session.execute(stmt)
    item = cursor.scalar()

    await session.delete(item)
    await session.commit()
