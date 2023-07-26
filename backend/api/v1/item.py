import fastapi
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.payloads import ExistingItem, CreateItem, CreatedResponse
from api.utils import get_current_user, get_session
from models.schema import ShoppingList, User, Item, Collaborator

router = fastapi.APIRouter()


@router.get("/{sl_id}")
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


@router.post("/{sl_id}")
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


async def remove_item()