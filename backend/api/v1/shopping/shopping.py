import fastapi
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from starlette import status

from api.payloads import (
    CreateItem,
    CreateShoppingList,
    UpdateShoppingList,
    CreatedResponse,
    ExistingShoppingList, ExistingItem, UpdateItem,
)
from api.utils import get_session, get_current_user
from models.schema import ShoppingList, User, Item, Collaborator

router = fastapi.APIRouter()


@router.get("/")
async def get_shopping_lists(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> list[ExistingShoppingList]:
    stmt = select(ShoppingList).join(User).where(User.username == user.username)
    cursor = await session.execute(stmt)
    lists = cursor.scalars()
    return [
        ExistingShoppingList(
            id=shopping_list.id,
            name=shopping_list.name,
            owner=user.username,
        )
        for shopping_list in lists
    ]


@router.get("/{sl_id}")
async def get_shopping_list(
    sl_id: int,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> ExistingShoppingList:
    stmt = (
        select(ShoppingList)
        .join(User)
        .where(User.username == user.username)
        .where(ShoppingList.id == sl_id)
    )
    cursor = await session.execute(stmt)
    shopping_list = cursor.scalar()
    return ExistingShoppingList(
        id=shopping_list.id, name=shopping_list.name, owner=user.username
    )


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_shopping_list(
    shoppping_list: CreateShoppingList,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> CreatedResponse:
    sl_inst = ShoppingList(user_id=user.id, name=shoppping_list.name)
    session.add(sl_inst)
    await session.commit()
    return CreatedResponse(id=sl_inst.id)


@router.patch("/")
async def update_shopping_list(
    shoppping_list: UpdateShoppingList,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> None:
    sl_inst = ShoppingList(user_id=user.id, name=shoppping_list.name)
    session.add(sl_inst)
    await session.commit()


@router.delete("/{sl_id}")
async def delete_shopping_list(
    sl_id: int,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    stmt = (
        select(ShoppingList)
        .join(ShoppingList.owner)
        .where(User.username == user.username)
        .where(ShoppingList.id == sl_id)
    )
    cursor = (await session.execute(stmt)).unique()
    shopping_list = cursor.scalar()
    await session.delete(shopping_list)
    await session.commit()


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
    await session.execute()
    return CreatedResponse(id=new_item.id)


@router.patch("/{sl_id}/items/{item_id}")
async def update_item(
    sl_id: int,
    item_id: int,
    item: UpdateItem,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
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
    await session.execute()
    return CreatedResponse(id=new_item.id)


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
        )
    )
    cursor = await session.execute(stmt)
    shopping_list = cursor.scalar()
    new_item = Item(name=item.name, quantity=item.quantity, description=item.description, sl_id=shopping_list.id)
    session.add(new_item)
    await session.execute()
    return CreatedResponse(id=new_item.id)
