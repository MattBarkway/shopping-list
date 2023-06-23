"""Utilities for the API."""
import re
from datetime import datetime, timedelta
from typing import Any, TypeVar

from fastapi import Depends, Form, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from starlette import status

import exceptions

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # noqa: S106
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
JWTData = dict[str, int | datetime]

CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def hash_pw(password: str) -> str:
    """Hash a password.

    Args:
        password: The password to hash.

    Returns:
        The hashed password.
    """
    return pwd_context.hash(password)


def validate_username(username: str) -> int:
    """Validate a username.

    Args:
        username: The username to validate.

    Returns:
        The validated username
    """
    try:
        return int(username)
    except ValueError:
        raise exceptions.ValidationError("Username must be an integer value") from None


def validate_email(email: str) -> str:
    """
    Validate an email.

    Args:
        email: The email to validate.

    Returns:
        The validated email.
    """
    pattern = re.compile(r"^[a-zA-Z.0-9]+@huboo\.(co|com|co\.uk)$")
    if not pattern.match(email):
        raise exceptions.ValidationError(
            "Invalid email, must be a valid huboo email address."
        )
    return email


class Token(BaseModel):
    """Token response model.

    Attributes:
        access_token: The token.
        token_type: Type of token.
    """

    access_token: str
    token_type: str


class HubModel(BaseModel):
    """Hub model.

    Attributes:
        number: The hub number.
    """

    number: str


async def get_hub(session: AsyncSession, hub_number: int) -> Hub | None:
    """Get a hub.

    Args:
        session: The DB session.
        hub_number: Hub number.

    Returns:
        The Hub object or None.
    """
    stmt = select(Hub).where(Hub.id == hub_number)
    cursor = await session.execute(stmt)
    return cursor.scalar()


async def authenticate_hub(
    session: AsyncSession, hub_number: str, password: str
) -> Hub:
    """Authenticate a hub.

    Args:
        session: The DB connection.
        hub_number: Hub number.
        password: Password.

    Returns:
        The Hub object.
    """
    try:
        hub_number_int = int(hub_number)
    except ValueError as ve:
        raise CREDENTIALS_EXCEPTION from ve
    hub = await get_hub(session, hub_number_int)
    if not hub:
        raise CREDENTIALS_EXCEPTION
    if not pwd_context.verify(password, hub.pw_hash):
        raise CREDENTIALS_EXCEPTION
    if not hub.verified:
        raise CREDENTIALS_EXCEPTION
    return hub


def create_access_token(data: JWTData, expires_delta: timedelta | None = None) -> str:
    """Create an access token.

    Args:
        data: Data payload.
        expires_delta: expiry period.

    Returns:
        Access token.
    """
    to_encode = data.copy()
    expire = (
        datetime.utcnow() + expires_delta
        if expires_delta
        else datetime.utcnow() + timedelta(minutes=15)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


async def get_current_hub(
    token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(analytics_db)
) -> Hub:
    """Get the current hub.

    Args:
        token: The hub's token.
        session: DB session.

    Returns:
        The Hub object.
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
    except JWTError as je:
        raise CREDENTIALS_EXCEPTION from je
    try:
        hub_number = payload["sub"]
    except KeyError as e:
        raise CREDENTIALS_EXCEPTION from e
    hub = await get_hub(session, hub_number)
    if hub is None:
        raise CREDENTIALS_EXCEPTION
    return hub


T = TypeVar("T")


async def get_or_create(session: AsyncSession, model: type[T], **kwargs: Any) -> T:
    """Get or create a record.

    Args:
        session: DB session.
        model: The model to get/create.
        kwargs: Args to search for existing records with.

    Returns:
        The model instance.
    """
    stmt = select(model).filter_by(**kwargs)
    cursor = await session.execute(stmt)
    instance = cursor.first()
    if instance:
        return instance[0]
    instance = model(**kwargs)
    session.add(instance)
    await session.flush()
    return instance


class SentinelOAuth2(OAuth2PasswordRequestForm):
    """OAuth2 Form data, with an email attribute."""

    def __init__(
        self,
        grant_type: str = Form(default=None, regex="password"),
        username: str = Form(),
        email: str = Form(),
        password: str = Form(),
        scope: str = Form(default=""),
        client_id: str | None = Form(default=None),
        client_secret: str | None = Form(default=None),
    ):
        super().__init__(
            grant_type, username, password, scope, client_id, client_secret
        )
        self.email = email
