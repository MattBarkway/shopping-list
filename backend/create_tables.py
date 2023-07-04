from models.schema import database, User, ShoppingList, Item


def create_tables():
    with database:
        database.create_tables([User, ShoppingList, Item])


if __name__ == "__main__":
    create_tables()
