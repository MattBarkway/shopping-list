"""Security helpers."""
from datetime import timedelta

import fastapi
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from itsdangerous import URLSafeTimedSerializer, encoding
from sendgrid import Mail, SendGridAPIClient
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from sentinel.api_utils import (
    SentinelOAuth2,
    Token,
    analytics_db,
    authenticate_hub,
    create_access_token,
    hash_pw,
    validate_email,
    validate_username,
)
from sentinel.config import settings
from sentinel.database.models import Hub

router = fastapi.APIRouter(prefix="/auth", tags=["authorisation"])


@router.post("/token", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(analytics_db),
) -> dict[str, str]:
    """Login endpoint.

    Args:
        form_data: Login form data.
        session: Session with the DB.

    Returns:
        Token.
    """
    hub = await authenticate_hub(session, form_data.username, form_data.password)
    if not hub:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(hub.id)},  # type: ignore
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    form_data: SentinelOAuth2 = Depends(),
    session: AsyncSession = Depends(analytics_db),
) -> None:
    """Register endpoint.

    Args:
        form_data: Login form data.
        session: Session with the DB.

    Returns:
        Token.
    """
    username = validate_username(form_data.username)
    validate_email(form_data.email)

    hub = Hub(id=username, pw_hash=hash_pw(form_data.password))
    session.add(hub)
    try:
        await session.commit()
    except IntegrityError:
        raise ValidationError("User already exists") from None

    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    token = serializer.dumps(username, salt=settings.SALT)
    clean_token = encoding.base64_encode(token).decode()
    sendgrid = SendGridAPIClient(settings.SENDGRID_KEY)
    message = Mail(
        from_email=settings.FROM_EMAIL,
        to_emails=form_data.email,
        subject="Verify your sentinel account",
        html_content=(
            f'<a href="{settings.HOST}/v1/auth/validate/{clean_token}/">click here</a> to verify your Sentinel account'
        ),
    )
    sendgrid.send(message)


@router.get("/validate/{token}/", status_code=status.HTTP_200_OK)
async def validate(
    token: str, session: AsyncSession = Depends(analytics_db)
) -> dict[str, str]:
    """Validate endpoint.

    Args:
        token: The token to decode.
        session: Session with the DB.
    """
    decoded_token = encoding.base64_decode(token).decode()
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    hub_number = serializer.loads(
        decoded_token, salt=settings.SALT, max_age=settings.MAX_VERIFY_AGE_SECONDS
    )
    hub_number = validate_username(hub_number)
    stmt = select(Hub).filter_by(id=hub_number)
    cursor = await session.execute(stmt)
    hub = cursor.scalar()
    if hub.verified:
        return {}
    hub.verified = True
    await session.commit()
    return {"message": "Successfully verified!"}
