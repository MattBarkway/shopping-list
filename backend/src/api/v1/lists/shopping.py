from fastapi import APIRouter
from sqlalchemy import select
from src.api.payloads import (
    CreatedResponse,
    CreateShoppingList,
    ExistingShoppingList,
    UpdateShoppingList,
)
from src.api.utils import DBSession, CurrentUser
from src.models.schema import ShoppingList, User, Collaborator
from starlette import status

from src.querying import querying

router = APIRouter()


@router.get("/")
async def get_shopping_lists(
    session: DBSession,
    user: CurrentUser,
) -> dict[str, list[ExistingShoppingList]]:
    collaborator_stmt = (
        select(ShoppingList)
        .join(Collaborator, Collaborator.list_id == ShoppingList.id)
        .filter(Collaborator.user_id == user.id)
    )
    collaborator_cursor = await session.execute(collaborator_stmt)

    owned_stmt = select(ShoppingList).join(User).where(User.username == user.username)
    owned_cursor = await session.execute(owned_stmt)
    return {
        "lists": [
            ExistingShoppingList(
                id=shopping_list.id,
                name=shopping_list.name,
                owner=user.username,
                last_updated=shopping_list.updated_at,
            )
            for shopping_list in owned_cursor.scalars()
        ],
        "shared_lists": [
            ExistingShoppingList(
                id=shopping_list.id,
                name=shopping_list.name,
                owner=shopping_list.owner.username,
                last_updated=shopping_list.updated_at,
            )
            for shopping_list in collaborator_cursor.scalars()
        ],
    }


@router.get("/{sl_id}")
async def get_shopping_list(
    sl_id: int,
    user: CurrentUser,
    session: DBSession,
) -> ExistingShoppingList:
    shopping_list = (
        await querying.get_shopping_list(session, sl_id, user.id)
    ).scalar_one()
    return ExistingShoppingList(
        id=shopping_list.id,
        name=shopping_list.name,
        owner=shopping_list.owner.username,
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
