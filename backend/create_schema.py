from settings import Settings
from sqlalchemy import create_engine, text

settings = Settings()

name_length = len(settings.DATABASE)

# Create a SQLAlchemy engine
engine = create_engine(settings.DB_URL[:-name_length])


def create_database_schema():
    query = text(f"SELECT 1 FROM pg_database WHERE datname = '{settings.DATABASE}'")
    with engine.connect() as connection:
        result = connection.execute(query)

        if not result.fetchone():
            connection.execute(
                text(f"CREATE DATABASE IF NOT EXISTS {settings.DATABASE}")
            )


if __name__ == "__main__":
    create_database_schema()
