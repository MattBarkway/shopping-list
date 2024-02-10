import functools
import typing
from typing import Any

from fastapi import Depends
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import model_validator


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

    SENTRY_DSN: str = ""

    ALLOWED_HOST: str = ""
    HOST: str = ""
    FRONTEND_HOST: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        use_enum_values=True,
        env_file_encoding="utf-8",
    )

    @model_validator(mode="before")
    @classmethod
    def build_database_urls(cls, values: dict[str, Any]) -> dict[str, Any]:
        values["DB_URL"] = get_generic_connection_builder(values)(
            driver=values["DRIVER"]
        )
        values["ASYNC_DB_URL"] = get_generic_connection_builder(values)(
            driver=values["ASYNC_DRIVER"]
        )

        return values


def get_generic_connection_builder(values: dict[str, Any]) -> functools.partial:
    """Generates a partial function, to simplify building connection strings."""

    return functools.partial(
        assemble_db_connection_str,
        dialect=values["DIALECT"],
        username=values["DB_USER"],
        password=values["DB_PASSWORD"],
        address=values["DB_HOST"],
        port=values["DB_PORT"],
        database=values["DATABASE"],
    )


def assemble_db_connection_str(
    dialect: str,
    driver: str,
    username: str,
    password: str,
    address: str,
    port: int,
    database: str,
) -> str:
    """Create PostgreSQL database connection path.

    Args:
        dialect: SQL dialect.
        driver: SQL driver.
        username: Username for the database.
        password: Password for the database.
        address: Database address.
        port: Port number for database.
        database: Database name.

    Returns:
        Database connection path.
    """

    return f"{dialect}+{driver}://{username}:{password}@{address}:{port}/{database}"


def get_settings() -> Settings:
    return Settings()


CurrentSettings = typing.Annotated[Settings, Depends(get_settings)]
