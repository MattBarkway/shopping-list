import functools
import pathlib
import typing

from fastapi import APIRouter, Depends, HTTPException
from itsdangerous import SignatureExpired, URLSafeTimedSerializer, encoding
from sendgrid import Mail, SendGridAPIClient
from settings import CurrentSettings
from sqlalchemy import select
from src.api.payloads import CreateCollaborator, ExistingCollaborator
from src.api.utils import CurrentUser, DBSession
from src.api.v1.auth import get_sendgrid_client
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
        ExistingCollaborator(id=collaborator.id, user_id=user.id, email=username)
        for collaborator, username in rows
    ]


@functools.lru_cache
def get_collaborator_template() -> str:
    with (pathlib.Path("static") / "collaborate.html").open() as f:
        return f.read()


@router.patch("/{sl_id}/collaborators", status_code=status.HTTP_201_CREATED)
async def add_collaborator(
    sl_id: int,
    collaborator: CreateCollaborator,
    user: CurrentUser,
    session: DBSession,
    settings: CurrentSettings,
    collaborator_template: typing.Annotated[str, Depends(get_collaborator_template)],
    sendgrid: typing.Annotated[SendGridAPIClient, Depends(get_sendgrid_client)],
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

    if collaborator.user_id:
        collaborator_inst = Collaborator(user_id=collaborator.user_id, list_id=sl_id)
        session.add(collaborator_inst)
        await session.commit()
    elif collaborator.email:
        serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
        token = serializer.dumps(collaborator.email, salt=settings.SALT)
        clean_token = encoding.base64_encode(token).decode()
        message = Mail(
            from_email=settings.FROM_EMAIL,
            to_emails=collaborator.email,
            subject="You've been invited to a shared shopping list!",
            html_content=collaborator_template.format(
                inviter=user.username,
                target=f"{settings.FRONTEND_HOST}/lists/{sl_id}/collaborator/validate/{clean_token}",
            ),
        )
        sendgrid.send(message)
        # TODO: track these requests in a table to prevent duplicates


@router.patch(
    "/{sl_id}/collaborators/validate/{token}", status_code=status.HTTP_201_CREATED
)
async def validate_collaborator(
    sl_id: int,
    token: str,
    user: CurrentUser,
    session: DBSession,
    settings: CurrentSettings,
) -> None:
    # TODO frontend flow to create acc/login, then validate
    decoded_token = encoding.base64_decode(token).decode()
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    try:
        username = serializer.loads(
            decoded_token, salt=settings.SALT, max_age=settings.MAX_VERIFY_AGE_SECONDS
        )
    except SignatureExpired:
        raise HTTPException(401, "Token has expired")
    stmt = select(User).where(User.username == username)
    cursor = await session.execute(stmt)
    expected_user = cursor.scalar()
    if expected_user.username != user.username:
        # logged in on wrong account?
        raise HTTPException(403, "Can't accept someone else's invite.")
    stmt2 = (
        select(ShoppingList)
        .where(
            (ShoppingList.id == sl_id)
            & ((ShoppingList.user_id == user.id) | (Collaborator.user_id == user.id))
        )
        .join(Collaborator, ShoppingList.id == Collaborator.list_id, isouter=True)
    )
    cursor = await session.execute(stmt2)
    shopping_list = cursor.scalar()
    if shopping_list:
        collaborator_inst = Collaborator(user_id=expected_user, list_id=sl_id)
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
