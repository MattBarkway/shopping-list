import pytest
from api.utils import get_current_user
from fastapi.testclient import TestClient
from main import app
from models.schema import Collaborator, Item, ShoppingList, SLBase, User
from settings import Settings
from sqlalchemy import create_engine, select


@pytest.mark.integration
class TestCollaborators:
    test_client = TestClient(app)

    @pytest.fixture(autouse=True)
    def create_database_cls(self):
        engine = create_engine(Settings().DB_URL)

        SLBase.metadata.create_all(engine)
        yield
        SLBase.metadata.drop_all(engine)

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
    def dummy_user3(self, db_session):
        user = User(
            username="bar", pw_hash="something", salt="something-else", verified=True
        )
        db_session.add(user)
        db_session.commit()
        return user

    @pytest.fixture
    def dummy_user4(self, db_session):
        user = User(
            username="wiz", pw_hash="something", salt="something-else", verified=True
        )
        db_session.add(user)
        db_session.commit()
        return user

    @pytest.fixture
    def dummy_collaborator(self, db_session, dummy_user3, dummy_shopping_list):
        colab = Collaborator(user_id=dummy_user3.id, list_id=dummy_shopping_list.id)
        db_session.add(colab)
        db_session.commit()
        return colab

    @pytest.fixture
    def dummy_collaborator2(self, db_session, dummy_user4, dummy_shopping_list2):
        colab = Collaborator(user_id=dummy_user4.id, list_id=dummy_shopping_list2.id)
        db_session.add(colab)
        db_session.commit()
        return colab

    @pytest.fixture
    def override_auth(self, dummy_user):
        app.dependency_overrides[get_current_user] = lambda: dummy_user
        yield dummy_user
        app.dependency_overrides = {}

    def test_get_collaborators(
        self, app_url, override_auth, dummy_shopping_list, dummy_collaborator
    ):
        response = self.test_client.get(
            f"{app_url}/api/v1/shopping/{dummy_shopping_list.id}/collaborators",
            headers={"Authorization": "Bearer foo"},
        )
        assert response.status_code == 200
        assert response.json() == [{"id": 1, "user_id": 1, "username": "bar"}]

    def test_add_collaborator(
        self, app_url, override_auth, dummy_shopping_list, dummy_user3
    ):
        response = self.test_client.patch(
            f"{app_url}/api/v1/shopping/{dummy_shopping_list.id}/collaborators/",
            headers={"Authorization": "Bearer foo"},
            json={"user_id": dummy_user3.id},
        )
        assert response.status_code == 201

    def test_remove_collaborator(
        self,
        app_url,
        override_auth,
        db_session,
        app_settings,
        dummy_shopping_list,
        dummy_collaborator,
        dummy_user3,
    ):
        response = self.test_client.delete(
            f"{app_url}/api/v1/shopping/{dummy_shopping_list.id}/collaborators/{dummy_collaborator.id}",
            headers={"Authorization": "Bearer foo"},
        )
        assert response.status_code == 200

        stmt = select(Collaborator).where(Collaborator.id == dummy_collaborator.id)
        cursor = db_session.execute(stmt)
        items = cursor.scalar()
        assert items is None
