import json
import os
from contextlib import suppress
from pathlib import Path
from subprocess import PIPE, Popen

import httpx
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
    port: str = docker_services.port_for(
        "database", int(os.getenv("POSTGRES_PORT", -1))
    )
    database = f"{docker_ip}:{port}"
    docker_services.wait_until_responsive(
        timeout=300.0,
        pause=1.0,
        check=lambda: is_responsive("sl-database"),
    )
    engine = create_engine(
        app_settings.DB_URL[: -len(app_settings.DATABASE)],
        isolation_level="AUTOCOMMIT",
    )
    with engine.connect() as connection, suppress(ProgrammingError):
        connection.execute(text("CREATE DATABASE sl"))
    return database


@pytest.fixture
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
        health = status["State"]["Health"]
    except Exception:
        return False
    return health["Status"] == "healthy"


@pytest.fixture(scope="session")
def kc_container(docker_ip, docker_services, docker_compose_command):
    kc_port = os.getenv("KEYCLOAK_PORT")

    def kc_healthcheck():
        try:
            httpx.get(f"http://{docker_ip}:{kc_port}/health/ready")
            return True
        except Exception:
            return False
        # print(response)
        # return response.status_code == 200

    kc = f"{docker_ip}:{kc_port}"
    docker_services.wait_until_responsive(
        timeout=300.0,
        pause=1.0,
        check=kc_healthcheck,
    )
    return kc
