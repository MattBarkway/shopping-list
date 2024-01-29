import typing
from typing import Any

from fastapi import Depends
from pydantic import BaseSettings, validator
from utils import assemble_mysql_connection


class Settings(BaseSettings):
    DIALECT: str = ""
    DATABASE: str = ""
    DB_USER: str = ""
    DB_PASSWORD: str = ""
    DB_HOST: str = ""
    DB_PORT: int = 0
    ASYNC_DRIVER: str = ""
    DRIVER: str = ""

    ASYNC_DB_URL: str = ""
    DB_URL: str = ""

    SALT: str = ""
    SECRET_KEY: str = ""
    MAX_VERIFY_AGE_SECONDS: int = 0
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 0
    ALGORITHM: str = ""

    SENDGRID_KEY: str = ""
    FROM_EMAIL: str = ""

    ALLOWED_HOST: str = ""
    HOST: str = ""
    FRONTEND_HOST: str = ""

    @validator("ASYNC_DB_URL", pre=True)
    def assemble_async_connection_string(
        cls, v: str | None, values: dict[str, Any]
    ) -> str:  # pragma: no cover
        """
        Create sql connection string.

        Args:
            v: Variable to validate.
            values: Other variable values in the Settings class.

        Returns:
            Connection string.
        """
        return assemble_mysql_connection(
            values["DIALECT"],
            values["ASYNC_DRIVER"],
            values["DB_USER"],
            values["DB_PASSWORD"],
            values["DB_HOST"],
            values["DB_PORT"],
            values["DATABASE"],
        )

    @validator("DB_URL", pre=True)
    def assemble_connection_string(
        cls, v: str | None, values: dict[str, Any]
    ) -> str:  # pragma: no cover
        """
        Create sql connection string.

        Args:
            v: Variable to validate.
            values: Other variable values in the Settings class.

        Returns:
            Connection string.
        """
        return assemble_mysql_connection(
            values["DIALECT"],
            values["DRIVER"],
            values["DB_USER"],
            values["DB_PASSWORD"],
            values["DB_HOST"],
            values["DB_PORT"],
            values["DATABASE"],
        )

    class Config:
        env_file = ".env"


def get_settings() -> Settings:
    return Settings()


CurrentSettings = typing.Annotated[Settings, Depends(get_settings)]
