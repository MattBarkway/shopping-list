from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from src.api.payloads import CreatedResponse, CreateItem, ExistingItem, UpdateItem
from src.api.utils import DBSession, CurrentUser
from src.models.schema import Collaborator, Item, ShoppingList
from starlette import status

from src.querying import querying
from src.utils import errors
from src.utils.dependencies import EnsureOwnsList

router = APIRouter()


@router.get("/{sl_id}/items")
async def get_items(
    sl_id: int,
    user: EnsureOwnsList,
    session: DBSession,
) -> list[ExistingItem]:
    if not (await querying.get_shopping_list(session, sl_id, user.id)).scalar():
        raise HTTPException(404, errors.LIST_NOT_FOUND)
    items = (await querying.get_items(session, sl_id)).scalars()
    return [
        ExistingItem(
            id=item.id,
            name=item.name,
            description=item.description,
            quantity=item.quantity,
        )
        for item in items
    ]


@router.get("/{sl_id}/items/{item_id}")
async def get_item(
    sl_id: int,
    item_id: int,
    user: CurrentUser,
    session: DBSession,
) -> list[ExistingItem]:
    stmt = (
        select(Item)
        .join(ShoppingList, Item.sl_id == ShoppingList.id)
        .join(
            Collaborator,
            (Collaborator.list_id == ShoppingList.id)
            & (Collaborator.user_id == user.id),
            isouter=True,
        )
        .where((ShoppingList.user_id == user.id) | (Collaborator.user_id == user.id))
        .where(ShoppingList.id == sl_id)
        .where(Item.id == item_id)
    )
    cursor = await session.execute(stmt)
    return [
        ExistingItem(
            id=item.id,
            name=item.name,
            description=item.description,
            quantity=item.quantity,
        )
        for item in cursor.scalars()
    ]


@router.post("/{sl_id}/items", status_code=status.HTTP_201_CREATED)
async def add_item(
    sl_id: int,
    item: CreateItem,
    _: EnsureOwnsList,
    session: DBSession,
) -> CreatedResponse:
    new_item = Item(
        name=item.name,
        quantity=item.quantity,
        description=item.description,
        sl_id=sl_id,
    )
    session.add(new_item)
    await session.commit()
    return CreatedResponse(id=new_item.id)


@router.patch("/{sl_id}/items/{item_id}")
async def update_item(
    sl_id: int,
    item_id: int,
    item: UpdateItem,
    _: EnsureOwnsList,
    session: DBSession,
) -> None:

    item_inst = (await querying.get_item(session, sl_id, item_id)).scalar_one()
    if item.name:
        item_inst.name = item.name
    if item.quantity:
        item_inst.quantity = item.quantity
    if item.description:
        item_inst.description = item.description
    session.add(item_inst)

    await session.commit()


@router.delete("/{sl_id}/items/{item_id}")
async def remove_item(
    sl_id: int,
    item_id: int,
    user: CurrentUser,
    session: DBSession,
) -> None:
    stmt = (
        select(Item)
        .join(ShoppingList, Item.sl_id == ShoppingList.id)
        .join(
            Collaborator,
            (Collaborator.list_id == ShoppingList.id)
            & (Collaborator.user_id == user.id),
            isouter=True,
        )
        .where((ShoppingList.user_id == user.id) | (Collaborator.user_id == user.id))
        .where(ShoppingList.id == sl_id)
        .where(Item.id == item_id)
    )
    cursor = await session.execute(stmt)
    item = cursor.scalar()

    await session.delete(item)
    await session.commit()
