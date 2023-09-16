from asyncio import Future

import pytest
from fastapi.testclient import TestClient
from itsdangerous import encoding
from sqlalchemy import select, create_engine

from main import app
from models.schema import User


@pytest.fixture
def read_user_token(kc_client):
    return kc_client.token("readuser", "password")["access_token"]


@pytest.fixture
def write_user_token(kc_client):
    return kc_client.token("writeuser", "password")["access_token"]


@pytest.fixture
def delete_user_token(kc_client):
    return kc_client.token("deleteuser", "password")["access_token"]


@pytest.fixture
def create_dummy_lists(create_database, db_session):
    db_session.commit()


@pytest.fixture
def mock_sendgrid(mocker):
    mock = mocker.MagicMock()
    mock2 = mocker.MagicMock()
    mock.return_value = mock2
    mock2.send.return_value = None
    mocker.patch("api.v1.auth.SendGridAPIClient", mock)
    return mock2


@pytest.fixture
def dummy_user(create_database, db_session):
    user = User(username="test-user", pw_hash="not-real", salt="", verified=False)
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def mock_serializer(mocker, dummy_user):
    mock = mocker.MagicMock()
    mock2 = mocker.MagicMock()
    mock.return_value = mock2
    mock2.loads.return_value = dummy_user.username
    mocker.patch("api.v1.auth.URLSafeTimedSerializer", mock)
    return mock2


@pytest.fixture
def mock_authenticate_user(mocker):
    mock = mocker.MagicMock()
    fut = Future()
    fut.set_result(User(username="foo", pw_hash="foo"))
    mock.return_value = fut
    mocker.patch("api.v1.auth.authenticate_user", mock)
    return mock


@pytest.mark.integration
@pytest.mark.asyncio
class TestAuth:
    test_client = TestClient(app)

    async def test_register_user(
        self, create_database, db_session, mock_sendgrid, app_url
    ):
        username = "test_user@test.com"

        response = self.test_client.post(
            f"{app_url}/api/v1/auth/register",
            data={"username": username, "password": "very-secure"},
        )
        assert response.status_code == 201
        mock_sendgrid.send.assert_called_once()

        stmt = select(User).where(User.username == username)
        cursor = db_session.execute(stmt)
        user = cursor.scalar()

        assert user is not None
        assert user.verified is False

    async def test_validate_user(
        self,
        create_database,
        db_session,
        dummy_user,
        mock_serializer,
        app_settings,
        app_url,
    ):
        token = encoding.base64_encode("1234.5678").decode()

        response = self.test_client.get(f"{app_url}/api/v1/auth/validate/{token}")

        assert response.status_code == 200

        engine = create_engine(app_settings.DB_URL)
        stmt = select(User).where(User.username == dummy_user.username)
        with engine.connect() as conn:
            cursor = conn.execute(stmt)
            user = cursor.all()[0]

        assert user is not None
        assert user.verified is True

        mock_serializer.loads.assert_called_once()

    async def test_login(self, create_database, mock_authenticate_user, app_url):
        response = self.test_client.post(
            f"{app_url}/api/v1/auth/token", data={"username": "foo", "password": "bar"}
        )

        assert response.status_code == 200

        mock_authenticate_user.assert_called_once()
