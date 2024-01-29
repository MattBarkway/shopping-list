"""Security helpers."""
import typing
from datetime import timedelta

import fastapi
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from itsdangerous import URLSafeTimedSerializer, encoding
from sendgrid import Mail, SendGridAPIClient
from settings import settings
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from src.api.utils import (
    DBSession,
    Token,
    authenticate_user,
    create_access_token,
    hash_pw,
)
from src.models.schema import User

router = fastapi.APIRouter()


@router.post("/token", response_model=Token)
async def login(
    form_data: typing.Annotated[OAuth2PasswordRequestForm, Depends()],
    session: DBSession,
) -> dict[str, str]:
    """Login endpoint.

    Args:
        form_data: Login form data.
        session: Session with the DB.

    Returns:
        Token.
    """
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)},  # type: ignore
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    form_data: typing.Annotated[OAuth2PasswordRequestForm, Depends()],
    session: DBSession,
) -> None:
    """Register endpoint.

    Args:
        form_data: Login form data.
        session: Session with the DB.

    Returns:
        Token.
    """
    user = User(
        username=form_data.username,
        pw_hash=hash_pw(form_data.password),
        salt=settings.SALT,
    )
    session.add(user)
    try:
        await session.commit()
    except IntegrityError as e:
        raise HTTPException(422, "User already exists") from e

    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    token = serializer.dumps(form_data.username, salt=settings.SALT)
    clean_token = encoding.base64_encode(token).decode()
    sendgrid = SendGridAPIClient(settings.SENDGRID_KEY)
    message = Mail(
        from_email=settings.FROM_EMAIL,
        to_emails=form_data.username,
        subject="Verify your shopping list account",
        html_content=(
            f'<a href="{settings.HOST}/api/v1/auth/validate/{clean_token}">'
            f"click here</a> to verify your account"
        ),
    )
    sendgrid.send(message)


@router.get("/validate/{token}/", status_code=status.HTTP_200_OK)
async def validate(token: str, session: DBSession) -> dict[str, str]:
    """Validate endpoint.

    Args:
        token: The token to decode.
        session: Session with the DB.
    """
    decoded_token = encoding.base64_decode(token).decode()
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    username = serializer.loads(
        decoded_token, salt=settings.SALT, max_age=settings.MAX_VERIFY_AGE_SECONDS
    )
    stmt = select(User).where(User.username == username)
    cursor = await session.execute(stmt)
    user = cursor.scalar()
    if user.verified:
        return {"message": "Already verified"}
    user.verified = True
    await session.commit()
    return {"message": "Successfully verified!"}
