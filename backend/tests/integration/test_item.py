import pytest
from fastapi.testclient import TestClient
from main import app
from sqlalchemy import select
from src.api.utils import get_current_user
from src.models.schema import Item, ShoppingList, User


@pytest.mark.integration
class TestItem:
    test_client = TestClient(app)

    @pytest.fixture
    def dummy_items(self, db_session, dummy_shopping_list):
        item1 = Item(
            sl_id=dummy_shopping_list.id, name="carrot", description="", quantity=1
        )
        item2 = Item(
            sl_id=dummy_shopping_list.id, name="potato", description="", quantity=1
        )
        item3 = Item(
            sl_id=dummy_shopping_list.id, name="cabbage", description="", quantity=1
        )
        item4 = Item(
            sl_id=dummy_shopping_list.id, name="courgette", description="", quantity=1
        )
        db_session.add(item1)
        db_session.add(item2)
        db_session.add(item3)
        db_session.add(item4)
        db_session.commit()
        db_session.flush()
        return item1, item2, item3, item4

    @pytest.fixture
    def dummy_items2(self, db_session, dummy_shopping_list2):
        item1 = Item(
            sl_id=dummy_shopping_list2.id, name="strawberry", description="", quantity=1
        )
        item2 = Item(
            sl_id=dummy_shopping_list2.id, name="banana", description="", quantity=1
        )
        item3 = Item(
            sl_id=dummy_shopping_list2.id, name="raspberry", description="", quantity=1
        )
        item4 = Item(
            sl_id=dummy_shopping_list2.id,
            name="pomegranate",
            description="",
            quantity=1,
        )
        db_session.add(item1)
        db_session.add(item2)
        db_session.add(item3)
        db_session.add(item4)
        db_session.commit()
        db_session.flush()
        return item1, item2, item3, item4

    @pytest.fixture
    def dummy_shopping_list(self, db_session, dummy_user):
        sl = ShoppingList(user_id=dummy_user.id, name="sl")
        db_session.add(sl)
        db_session.commit()
        return sl

    @pytest.fixture
    def dummy_shopping_list2(self, db_session, dummy_user):
        sl2 = ShoppingList(user_id=dummy_user.id, name="sl2")
        db_session.add(sl2)
        db_session.commit()
        return sl2

    @pytest.fixture
    def dummy_user(self, db_session):
        user = User(
            username="foo", pw_hash="something", salt="something-else", verified=True
        )
        db_session.add(user)
        db_session.commit()
        return user

    @pytest.fixture
    def override_auth(self, dummy_user):
        app.dependency_overrides[get_current_user] = lambda: dummy_user
        yield dummy_user
        app.dependency_overrides = {}

    def test_get_items(self, app_url, override_auth, dummy_items, dummy_items2):
        sl_id = 1
        response = self.test_client.get(
            f"{app_url}/api/v1/shopping/{sl_id}/items",
            headers={"Authorization": "Bearer foo"},
        )
        assert response.status_code == 200
        assert response.json() == [
            {"description": "", "id": 1, "name": "carrot", "quantity": 1},
            {"description": "", "id": 2, "name": "potato", "quantity": 1},
            {"description": "", "id": 3, "name": "cabbage", "quantity": 1},
            {"description": "", "id": 4, "name": "courgette", "quantity": 1},
        ]

    def test_get_item(self, app_url, override_auth, dummy_items, dummy_items2):
        sl_id = 1
        item_id = 1
        response = self.test_client.get(
            f"{app_url}/api/v1/shopping/{sl_id}/items/{item_id}",
            headers={"Authorization": "Bearer foo"},
        )
        assert response.status_code == 200
        assert response.json() == [
            {"description": "", "id": 1, "name": "carrot", "quantity": 1}
        ]

    def test_create_item(
        self, app_url, override_auth, db_session, app_settings, dummy_shopping_list
    ):
        response = self.test_client.post(
            f"{app_url}/api/v1/shopping/{dummy_shopping_list.id}/items",
            headers={"Authorization": "Bearer foo"},
            json={
                "name": "A carrot",
                "description": "yep it sure is",
                "quantity": 800,
            },
        )
        assert response.status_code == 201
        assert response.json() == {"id": 1}

        stmt = select(Item).where(ShoppingList.id == dummy_shopping_list.id)
        cursor = db_session.execute(stmt)
        items = cursor.scalars().all()
        assert len(items) == 1
        item = items[0]
        assert item.name == "A carrot"
        assert item.description == "yep it sure is"
        assert item.quantity == 800

    def test_update_item(
        self,
        app_url,
        override_auth,
        db_session,
        app_settings,
        dummy_shopping_list,
        dummy_items,
    ):
        response = self.test_client.patch(
            f"{app_url}/api/v1/shopping/{dummy_shopping_list.id}/items/{dummy_items[0].id}",
            headers={"Authorization": "Bearer foo"},
            json={
                "quantity": 2,
            },
        )
        assert response.status_code == 200
        stmt = select(Item).where(Item.id == dummy_items[0].id)
        cursor = db_session.execute(stmt)
        item = cursor.scalar_one()

        db_session.refresh(item)

        assert item.name == "carrot"
        assert item.description == ""
        assert item.quantity == 2

    def test_remove_item(
        self,
        app_url,
        override_auth,
        db_session,
        app_settings,
        dummy_shopping_list,
        dummy_items,
    ):
        response = self.test_client.delete(
            f"{app_url}/api/v1/shopping/{dummy_shopping_list.id}/items/{dummy_items[0].id}",
            headers={"Authorization": "Bearer foo"},
        )
        assert response.status_code == 200

        stmt = select(Item).where(Item.id == dummy_items[0].id)
        cursor = db_session.execute(stmt)
        item = cursor.scalar()
        assert item is None
