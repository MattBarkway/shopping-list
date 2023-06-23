from peewee import Model, CharField, ForeignKeyField, IntegerField, MySQLDatabase

from settings import settings

database = MySQLDatabase(
    settings.DATABASE,
    user=settings.DB_USER,
    password=settings.DB_PASSWORD,
    host=settings.DB_HOST,
    port=settings.DB_PORT,
)


class BaseModel(Model):
    class Meta:
        database = database


class User(BaseModel):
    username = CharField()
    hash_pw = CharField()


class ShoppingList(BaseModel):
    owner = ForeignKeyField(User, backref="lists")


class Item(BaseModel):
    name = CharField()
    description = CharField()
    quantity = IntegerField()
    shopping_list = ForeignKeyField(ShoppingList, backref="items")
