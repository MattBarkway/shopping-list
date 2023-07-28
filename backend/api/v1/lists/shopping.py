from fastapi import Depends, APIRouter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.payloads import (
    CreateShoppingList,
    UpdateShoppingList,
    CreatedResponse,
    ExistingShoppingList,
)
from api.utils import get_session, get_current_user
from models.schema import ShoppingList, User

router = APIRouter()


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
