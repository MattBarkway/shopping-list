from fastapi import APIRouter
from sqlalchemy import select
from src.api.payloads import (
    CreatedResponse,
    CreateShoppingList,
    ExistingShoppingList,
    UpdateShoppingList,
)
from src.api.utils import CurrentUser, DBSession
from src.models.schema import ShoppingList, User
from starlette import status

router = APIRouter()


@router.get("/")
async def get_shopping_lists(
    session: DBSession,
    user: CurrentUser,
) -> list[ExistingShoppingList]:
    stmt = select(ShoppingList).join(User).where(User.username == user.username)
    cursor = await session.execute(stmt)
    lists = cursor.scalars()
    return [
        ExistingShoppingList(
            id=shopping_list.id,
            name=shopping_list.name,
            owner=user.username,
            last_updated=shopping_list.updated_at,
        )
        for shopping_list in lists
    ]


@router.get("/{sl_id}")
async def get_shopping_list(
    sl_id: int,
    user: CurrentUser,
    session: DBSession,
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
        id=shopping_list.id,
        name=shopping_list.name,
        owner=user.username,
        last_updated=shopping_list.updated_at,
    )


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_shopping_list(
    shopping_list: CreateShoppingList,
    user: CurrentUser,
    session: DBSession,
) -> CreatedResponse:
    sl_inst = ShoppingList(user_id=user.id, name=shopping_list.name)
    session.add(sl_inst)
    await session.commit()
    return CreatedResponse(id=sl_inst.id)


@router.patch("/")
async def update_shopping_list(
    shopping_list: UpdateShoppingList,
    user: CurrentUser,
    session: DBSession,
) -> None:
    sl_inst = ShoppingList(user_id=user.id, name=shopping_list.name)
    session.add(sl_inst)
    await session.commit()


@router.delete("/{sl_id}")
async def delete_shopping_list(
    sl_id: int,
    user: CurrentUser,
    session: DBSession,
) -> None:
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
