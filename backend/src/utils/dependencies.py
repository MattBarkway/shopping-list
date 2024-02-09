import typing

from fastapi import Depends, HTTPException

from src.api.utils import DBSession, CurrentUser
from src.models.schema import User
from src.querying import querying
from src.utils import errors


async def ensure_owns_list(sl_id: int, session: DBSession, user: CurrentUser):
    if not (await querying.get_shopping_list(session, sl_id, user.id)).scalar():
        raise HTTPException(
            status_code=404,
            detail=errors.LIST_NOT_FOUND,
        )
    return user


async def ensure_owns_list_strict(sl_id: int, session: DBSession, user: CurrentUser):
    shopping_list = (
        await querying.get_shopping_list(session, sl_id, user.id)
    ).scalar_one()
    if not shopping_list:
        raise HTTPException(
            status_code=404,
            detail=errors.LIST_NOT_FOUND,
        )
    if shopping_list.owner.username != user.username:
        raise HTTPException(
            status_code=404,
            detail=errors.LIST_NOT_FOUND,
        )
    return user


EnsureOwnsList = typing.Annotated[User, Depends(ensure_owns_list)]
EnsureOwnsListStrict = typing.Annotated[User, Depends(ensure_owns_list_strict)]
