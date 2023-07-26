import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select

from api.utils import get_current_user
from main import app
from models.schema import User, ShoppingList, Item, SLBase
from settings import Settings


@pytest.mark.integration
class TestShopping:
    test_client = TestClient(app)

    @pytest.fixture(autouse=True)
    def create_database_cls(self):
        engine = create_engine(Settings().DB_URL)

        SLBase.metadata.create_all(engine)
        yield
        SLBase.metadata.drop_all(engine)

    @pytest.fixture
    def dummy_shopping_list(self, db_session, dummy_user):
        sl = ShoppingList(user_id=dummy_user.id, name="sl")
        db_session.add(sl)
        db_session.commit()
        db_session.flush(sl)
        return sl

    @pytest.fixture
    def dummy_shopping_list2(self, db_session, dummy_user):
        sl2 = ShoppingList(user_id=dummy_user.id, name="sl2")
        db_session.add(sl2)
        db_session.commit()
        db_session.flush(sl2)
        return sl2

    @pytest.fixture
    def dummy_user(self, db_session):
        user = User(
            username="foo", pw_hash="something", salt="something-else", verified=True
        )
        db_session.add(user)
        db_session.commit()
        db_session.flush(user)
        return user

    @pytest.fixture
    def override_auth(self, dummy_user):
        app.dependency_overrides[get_current_user] = lambda: dummy_user
        yield dummy_user
        app.dependency_overrides = {}

    def test_get_shopping_lists(
        self, app_url, override_auth, dummy_items, dummy_items2
    ):
        response = self.test_client.get(
            f"{app_url}/api/v1/shopping", headers={"Authorization": "Bearer foo"}
        )
        assert response.status_code == 200
        assert response.json() == [
            {"id": 1, "name": "sl", "owner": "foo"},
            {"id": 2, "name": "sl2", "owner": "foo"},
        ]

    def test_get_shopping_list(self, app_url, override_auth, dummy_items, dummy_items2):
        response = self.test_client.get(
            f"{app_url}/api/v1/shopping/1", headers={"Authorization": "Bearer foo"}
        )
        assert response.status_code == 200
        assert response.json() == {
            "id": 1,
            "name": "sl",
            "owner": "foo",
        }

    def test_create_shopping_list(
        self, app_url, override_auth, db_session, app_settings
    ):
        response = self.test_client.post(
            f"{app_url}/api/v1/shopping",
            headers={"Authorization": "Bearer foo"},
            json={
                "name": "groceries",
                "items": [],
            },
        )
        assert response.status_code == 201
        assert response.json() == {"id": 1}

        stmt = select(ShoppingList)
        cursor = db_session.execute(stmt)
        shopping_list = cursor.scalar()
        assert shopping_list.id == 1
