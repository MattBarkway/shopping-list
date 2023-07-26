"""Utilities for the API."""
from collections.abc import Generator
from datetime import datetime, timedelta
from typing import Any, TypeVar

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from starlette import status

from models.schema import User
from settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # noqa: S106
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
JWTData = dict[str, int | datetime]

CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


async def get_session() -> Generator[AsyncSession, None, None]:
    engine = create_async_engine(settings.ASYNC_DB_URL, echo=True)
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


async def get_user(session: AsyncSession, username: int) -> User | None:
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


async def get_current_user(
    token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)
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
        username = payload["sub"]
    except KeyError as e:
        raise CREDENTIALS_EXCEPTION from e
    user = await get_user(session, username)
    if user is None:
        raise CREDENTIALS_EXCEPTION
    return user


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
