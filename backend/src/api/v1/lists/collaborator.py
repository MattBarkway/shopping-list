from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from src.api.payloads import CreateCollaborator, ExistingCollaborator
from src.api.utils import CurrentUser, DBSession
from src.models.schema import Collaborator, ShoppingList, User
from starlette import status

router = APIRouter()


@router.get("/{sl_id}/collaborators")
async def get_collaborators(
    sl_id: int,
    user: CurrentUser,
    session: DBSession,
) -> list[ExistingCollaborator]:
    stmt = (
        select(Collaborator, User.username)
        .join(User, Collaborator.user_id == User.id)
        .where(
            (Collaborator.list_id == sl_id)
            & ((Collaborator.user_id == user.id) | (ShoppingList.user_id == user.id))
        )
        .join(ShoppingList, ShoppingList.id == sl_id)
    )
    cursor = await session.execute(stmt)
    rows = cursor.all()
    return [
        ExistingCollaborator(id=collaborator.id, user_id=user.id, username=username)
        for collaborator, username in rows
    ]


@router.patch("/{sl_id}/collaborators", status_code=status.HTTP_201_CREATED)
async def add_collaborator(
    sl_id: int,
    collaborator: CreateCollaborator,
    user: CurrentUser,
    session: DBSession,
) -> None:
    stmt = (
        select(ShoppingList)
        .where(
            (ShoppingList.id == sl_id)
            & ((ShoppingList.user_id == user.id) | (Collaborator.user_id == user.id))
        )
        .join(Collaborator, ShoppingList.id == Collaborator.list_id, isouter=True)
    )
    cursor = await session.execute(stmt)
    shopping_list = cursor.scalar()

    if not shopping_list:
        raise HTTPException(
            status_code=403, detail="You don't have access to this list!"
        )

    collaborator_inst = Collaborator(user_id=collaborator.user_id, list_id=sl_id)
    session.add(collaborator_inst)
    await session.commit()


@router.delete("/{sl_id}/collaborators/{collaborator_id}")
async def remove_collaborator(
    sl_id: int,
    collaborator_id: int,
    user: CurrentUser,
    session: DBSession,
) -> None:
    stmt = (
        select(Collaborator)
        .join(
            ShoppingList,
            (
                (ShoppingList.id == Collaborator.list_id)
                & (Collaborator.id == collaborator_id)
            ),
            isouter=True,
        )
        .where(
            (ShoppingList.id == sl_id)
            & ((ShoppingList.user_id == user.id) | (Collaborator.id == collaborator_id))
        )
    )
    cursor = await session.execute(stmt)
    collaborator = cursor.scalar()

    if not collaborator:
        raise HTTPException(
            status_code=404, detail="No collaborator matching that ID Found!"
        )
    await session.delete(collaborator)
    await session.commit()
