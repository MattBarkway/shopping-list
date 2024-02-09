from sqlalchemy import select, Result, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.schema import ShoppingList, User, Collaborator, Item


async def _get_owned_shopping_list(session: AsyncSession, sl_id: int, user_id: int):
    stmt = (
        select(ShoppingList)
        .select_from(ShoppingList)
        .join(User, User.id == ShoppingList.user_id)
        .outerjoin(Collaborator, Collaborator.list_id == ShoppingList.id)
        .where(
            and_(
                ShoppingList.id == sl_id,
                (User.id == user_id) | (Collaborator.user_id == user_id),
            )
        )
    )
    return await session.execute(stmt)


async def get_shopping_list(
    session: AsyncSession,
    sl_id: int,
    user_id: int,
    require_ownership: bool = False,
) -> Result[tuple[ShoppingList]]:
    if require_ownership:
        return await _get_owned_shopping_list(session, sl_id, user_id)
    return await session.execute(select(ShoppingList).where(ShoppingList.id == sl_id))


async def get_collaborators(
    session: AsyncSession, sl_id: int
) -> Result[tuple[Collaborator, str]]:
    return await session.execute(
        (
            select(Collaborator, User.username)
            .select_from(Collaborator)
            .join(User, User.id == Collaborator.user_id)
            .where(Collaborator.list_id == sl_id)
        )
    )


async def get_items(session: AsyncSession, sl_id: int) -> Result[tuple[Item]]:
    return await session.execute(select(Item).where(Item.sl_id == sl_id))


async def get_item(
    session: AsyncSession, sl_id: int, item_id: int
) -> Result[tuple[Item]]:
    return await session.execute(
        select(Item).where((Item.sl_id == sl_id) & (Item.id == item_id))
    )
