import pytest
from fastapi.testclient import TestClient
from main import app
from sqlalchemy import select
from src.api.utils import get_current_user
from src.models.schema import ShoppingList, User


@pytest.mark.integration
class TestShopping:
    test_client = TestClient(app)

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
        self, app_url, override_auth, dummy_shopping_list, dummy_shopping_list2
    ):
        response = self.test_client.get(
            f"{app_url}/api/v1/shopping", headers={"Authorization": "Bearer foo"}
        )
        assert response.status_code == 200
        response = response.json()
        cleaned_response = {"lists": [], "shared_lists": []}
        for i in response.get("lists"):
            del i["last_updated"]
            cleaned_response["lists"].append(i)
        for i in response.get("shared_lists"):
            del i["last_updated"]
            cleaned_response["shared_lists"].append(i)
        assert cleaned_response == {
            "lists": [
                {"id": 1, "name": "sl", "owner": "foo"},
                {"id": 2, "name": "sl2", "owner": "foo"},
            ],
            "shared_lists": [],
        }

    def test_get_shopping_list(
        self, app_url, override_auth, dummy_shopping_list, dummy_shopping_list2
    ):
        response = self.test_client.get(
            f"{app_url}/api/v1/shopping/1", headers={"Authorization": "Bearer foo"}
        )
        assert response.status_code == 200
        payload = response.json()
        del payload["last_updated"]
        assert payload == {
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
