"""Utilities for the API."""
import typing
from datetime import datetime, timedelta
from typing import TypeVar

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from settings import CurrentSettings
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from src.models.schema import User
from starlette import status

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # noqa: S106
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
JWTData = dict[str, int | datetime]

CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


async def get_session(
    settings: CurrentSettings,
) -> typing.AsyncGenerator[AsyncSession, None]:
    engine = create_async_engine(f"{settings.ASYNC_DB_URL}?client_encoding=utf8")
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session


def hash_pw(password: str) -> str:
    """Hash a password.

    Args:
        password: The password to hash.

    Returns:
        The hashed password.
    """
    return pwd_context.hash(password)


class Token(BaseModel):
    """Token response model.

    Attributes:
        access_token: The token.
        token_type: Type of token.
    """

    access_token: str
    token_type: str


async def get_user(session: AsyncSession, username: str) -> User | None:
    """Get a user.

    Args:
        session: The DB session.
        username: Username.

    Returns:
        The User object or None.
    """
    stmt = select(User).where(User.username == username)
    cursor = await session.execute(stmt)
    return cursor.scalar()


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    """Get a user.

    Args:
        session: The DB session.
        user_id: User ID.

    Returns:
        The User object or None.
    """
    stmt = select(User).where(User.id == user_id)
    cursor = await session.execute(stmt)
    return cursor.scalar()


async def authenticate_user(
    session: AsyncSession, username: str, password: str
) -> User:
    """Authenticate a user.

    Args:
        session: The DB connection.
        username: Username.
        password: Password.

    Returns:
        The user object.
    """
    user = await get_user(session, username)
    if not user:
        raise CREDENTIALS_EXCEPTION
    if not pwd_context.verify(password, user.pw_hash):
        raise CREDENTIALS_EXCEPTION
    if not user.verified:
        raise CREDENTIALS_EXCEPTION
    return user


def create_access_token(
    data: JWTData, expires_delta: timedelta | None, secret_key: str, algorithm: str
) -> str:
    """Create an access token.

    Args:
        data: Data payload.
        expires_delta: expiry period.
        algorithm: Cryptographic algorithm.
        secret_key: Secret key.

    Returns:
        Access token.
    """
    to_encode = data.copy()
    expire = (
        datetime.utcnow() + expires_delta
        if expires_delta
        else datetime.utcnow() + timedelta(minutes=180)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret_key, algorithm=algorithm)


DBSession = typing.Annotated[AsyncSession, Depends(get_session)]


async def get_current_user(
    settings: CurrentSettings,
    token: typing.Annotated[str, Depends(oauth2_scheme)],
    session: DBSession,
) -> User:
    """Get the current user.

    Args:
        token: The user's token.
        session: DB session.

    Returns:
        The User object.
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
    except JWTError as je:
        raise CREDENTIALS_EXCEPTION from je
    try:
        user_id = int(payload["sub"])
    except KeyError as e:
        raise CREDENTIALS_EXCEPTION from e
    user = await get_user_by_id(session, user_id)
    if user is None:
        raise CREDENTIALS_EXCEPTION
    return user


CurrentUser = typing.Annotated[User, Depends(get_current_user)]
T = TypeVar("T")
