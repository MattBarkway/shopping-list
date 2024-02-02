import json
import os
from contextlib import suppress
from pathlib import Path
from subprocess import PIPE, Popen

import pytest
from settings import Settings
from sqlalchemy import create_engine, text
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import Session
from src.models.schema import SLBase


@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig) -> str:
    """Load Docker Compose file for running services."""
    return str(Path.cwd() / ".." / "docker-compose.yml")


@pytest.fixture(scope="session")
def app_settings():
    return Settings()


@pytest.fixture
def app_url():
    return "http://0.0.0.0:8000"


@pytest.fixture(scope="session")
def database_container(docker_ip, docker_services, app_settings) -> str:
    """Ensure that Postgres service is up and responsive.

    `port_for` takes a container port
    and returns the corresponding host port.
    """
    port: str = docker_services.port_for("database", int(os.getenv("DB_PORT")))
    database = f"{docker_ip}:{port}"
    docker_services.wait_until_responsive(
        timeout=300.0,
        pause=1.0,
        check=lambda: is_responsive("sl-shopping-list"),
    )
    engine = create_engine(
        app_settings.DB_URL[: -len(app_settings.DATABASE)],
        isolation_level="AUTOCOMMIT",
    )
    with engine.connect() as connection, suppress(ProgrammingError):
        connection.execute(text("CREATE DATABASE sl"))
    return database


@pytest.fixture(autouse=True)
def create_database(database_container, app_settings):
    engine = create_engine(app_settings.DB_URL)

    SLBase.metadata.create_all(engine)
    yield
    SLBase.metadata.drop_all(engine)


@pytest.fixture
def db_session(app_settings):
    engine = create_engine(app_settings.DB_URL)
    with Session(engine) as session:
        yield session


def is_responsive(service: str) -> bool:
    """Check running container service is healthy."""

    proc = Popen(
        ["docker", "inspect", service],
        stdin=PIPE,
        stdout=PIPE,
        stderr=PIPE,
    )

    output, err = proc.communicate()
    try:
        status = json.loads(output)[0]
        return status["State"]["Health"]["Status"] == "healthy"
    except Exception:
        return False
